from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserLoginForm,CustomPasswordResetForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail,  EmailMultiAlternatives, EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse,reverse_lazy

from Uziapp.models import Base

User = get_user_model()

# Create your views here.

def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # creating user without activating yet
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            
            # generating verification code
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            # building verication url(more robust than string formatting)
            current_site = get_current_site(request)
            protocol = 'https' if request.is_secure() else 'http'
            verification_path = reverse('activate_user', kwargs={'uidb64': uid, 'token': token})
            verification_link = f'{protocol}://{current_site.domain}{verification_path}'

            # sending my verifcation mail
            base = Base.objects.first()
            subject = 'Welcome! Please, verify your email'
            message = render_to_string('pages/auth/email-verification.html', {
                'user': user, 
                'verification_link' : verification_link,
                'site_name' : current_site.name,
                'company_name' : base.company_name,
            })
            
            try:
                email = EmailMessage(
                    subject=subject,
                    body=message,
                    from_email=settings.EMAIL_HOST_USER,
                    to=[user.email]
                )

                email.content_subtype = 'html'
                email.send(fail_silently=False)

                messages.success(request, 'Registration almost done, please check your email to verify your account.')
                return redirect('login')
            
            except Exception as e:
                # to clean up the user from db since verification cant ber sent
                user.delete()  
                messages.error(request, 'Error sending verification email. Please try again')
                print(f'Email error : {e}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else: 
        form = UserRegistrationForm()

    return render(request, 'pages/auth/register.html',{'form': form})


def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user= None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()

        # Auto login user after activation (skippping manual login)
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')

        messages.success(request, f'Welcome {user.first_name} Your account has been successfully activated!')
        return redirect('landing')
    else:
        messages.error(request, 'invalid or expired activation link. Please register again')
        return redirect('register')
    


class CustomLoginView(LoginView):
    # class handles login
    
    form_class = UserLoginForm
    template_name = 'pages/auth/login.html'
    redirect_authenticated_user = True      

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        # for a Personalized welcome message
        messages.success(self.request, f'Welcome back, {user.first_name}!')
        return redirect('landing') 

    def form_invalid(self, form):
        # To show error message on failed login
        messages.error(self.request, 'Invalid email or password. Please try again.')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        # Passing extra context to template if needed
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login'
        return context
    



def logout_view(request):
    logout(request)
    # messages.success(request, 'You have been logged out successfully ')
    return redirect('landing')

class CustomPasswordResetView(PasswordResetView):
    template_name = 'pages/auth/password_reset.html'
    email_template_name = 'pages/auth/password_reset_email.html'
    subject_template_name = 'pages/auth/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'pages/auth/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'pages/auth/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'pages/auth/password_reset_complete.html'