from django.conf import settings
from django.shortcuts import render,redirect
from django.core.mail import send_mail
from .forms import ContactForm
from django.contrib import messages
from .models import Base, About , Team, Testimonial, Service, Project,  Contact, ChooseUs

# Create your views here.
def landing_page(request):
    base = Base.objects.first()
    about = About.objects.first()
    chooseus = ChooseUs.objects.all()
    project = Project.objects.all()
    service = Service.objects.all()
    team = Team.objects.all()
    testimonial = Testimonial.objects.all()
    context = {
        'company_name' : base.company_name,
        'footer_text' : base.footer_text,
        'hero_img1' : base.hero_img1,
        'hero_img2' : base.hero_img2,
        'hero_img3' : base.hero_img3,
        'newsletter_img' : base.newsletter_img,

        'history' : about.history,
        'about_img1' : about.about_img1,
        'about_img2' : about.about_img2,

        'chooseus' : chooseus,

        'project' : project,

        'service' : service,

        'team' : team,

        'testimonial' : testimonial,
    }
    return render(request, 'pages/web/index.html', context)

def about_page(request):
    about = About.objects.first()
    team = Team.objects.all()
    chooseus = ChooseUs.objects.all()
    base = Base.objects.first()
    context = {
        'history' : about.history,
        'about_img1' : about.about_img1,
        'about_img2' : about.about_img2,

        'team' : team,

        'chooseus' : chooseus,

        'newsletter_img' : base.newsletter_img,
        'company_name' : base.company_name,
        'footer_text' : base.footer_text,
    }
    return render(request, 'pages/web/about.html', context)

def services_page(request):
    service = Service.objects.all()
    testimonial = Testimonial.objects.all()
    base = Base.objects.first()
    context = {
        'service' : service,

        'testimonial' : testimonial,

        'newsletter_img' : base.newsletter_img,
        'company_name' : base.company_name,
        'footer_text' : base.footer_text,
    }
    return render(request, 'pages//web/services.html', context)

def projects_page(request):
    project = Project.objects.all()
    testimonial = Testimonial.objects.all()
    base = Base.objects.first()
    context = {
        'project' : project,

        'testimonial' : testimonial,

        'base' : base.newsletter_img,
        'company_name' : base.company_name,
        'footer_text' : base.footer_text,
    }
    return render(request, 'pages/web/projects.html', context)

def contact_page(request):
    base, created = Base.objects.get_or_create(pk=1)

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
        
            try:
                send_mail(
                    subject=f'Feedback from {contact.name} - {contact.subject}',
                    message=f'From: {contact.name} ({contact.email})\n\nSubject : {contact.subject}\n\nMessaage:\n{contact.message} : ',
                    from_email= settings.EMAIL_HOST_USER,
                    recipient_list=[settings.EMAIL_HOST_USER],
                    fail_silently=False,
                )
                messages.success(request, "Thank you for contacting us. We'll get back to you")

            except Exception as e:
                # cause i want to keep the contact but notify the user email failed
                messages.warning(request,"Your message was saved, but we could'nt but we could'nt send a confirmation mail")
                print(f"Email error: {e}")
            return redirect('contact')  # to redirect back to my contact page with success message
        else:
            messages.error(request, 'Please correct the errors below')
    else: 
        form = ContactForm()

    context = {
        'footer_text' : base.footer_text,
        'company_name' : base.company_name,
        'newsletter_img' : base.newsletter_img, 
        'form' : form

    }
    
    return render(request, 'pages/web/contact.html', context)