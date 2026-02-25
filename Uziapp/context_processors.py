from .models import SocialMediaLink, Team, Testimonial, Service, Base

def global_data(request):
    return{'social_links': SocialMediaLink.objects.filter(is_active=True),
           'team' : Team.objects.all(),
           'testimonial' : Testimonial.objects.all(),
           'service' : Service.objects.all(),
           'base': Base.objects.all()
           }

