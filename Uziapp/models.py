from django.db import models

# Create your models here.
class Base(models.Model):
    company_name = models.CharField(max_length=100)
    footer_text = models.CharField(max_length=500)
    hero_img1 = models.ImageField(upload_to='index/', blank=True)
    hero_img2 = models.ImageField(upload_to='index/', blank=True)
    hero_img3 = models.ImageField(upload_to='index/', blank=True)
    newsletter_img = models.ImageField(upload_to='index/', blank=True)
    

    def __str__(self):
        return self.company_name
    
class SocialMediaLink(models.Model):
    PLATFORM_CHOICES = [
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter'),
        ('instagram','Instagram'),
        ('linkedin', 'Linkedin'),
        ('youtube', 'Youtube'),
    ]
    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES, unique=True)
    url = models.URLField()
    icon_class = models.CharField(max_length=50)  # e.g., 'fab fa-facebook-f'
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.platform
    
class About(models.Model):
    history = models.TextField()
    about_img1 = models.ImageField(upload_to='about/', blank=True)
    about_img2 = models.ImageField(upload_to='about/', blank=True)

    def __str__(self):
        return self.history


class ChooseUs(models.Model):
    icon_class = models.CharField(max_length=100)
    reason = models.CharField(max_length=50)
    reason_text = models.CharField(max_length=200)
    
    def __str__(self):
        return self.reason
    
class Team(models.Model):
    team_img = models.ImageField(upload_to='index/', blank=True)
    profession = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    fb = models.URLField()
    x = models.URLField()
    ig = models.URLField()
    ln = models.URLField()

    def __str__(self):
        return self.name
    
class Service(models.Model):
    service_intro = models.TextField(blank=True)
    service = models.CharField(max_length=50)
    service_detail = models.CharField(max_length=200)
    img = models.ImageField(upload_to='service/', blank=True)
    
    def __str__(self):
        return self.service
    
class Testimonial(models.Model):
    img = models.ImageField(upload_to='index/', blank=True)
    testimony = models.CharField(max_length=50)
    testimony_text = models.CharField(max_length=500)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.testimony
    

class Project(models.Model):
    img = models.ImageField(upload_to='projects/')
    name_of_project = models.CharField(max_length=100)
    number_of_project = models.CharField(max_length=100)

    def __str__(self):
        return self.name_of_project
    
class Contact(models.Model):
    name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=100, blank=True)
    subject = models.CharField(max_length=500, blank=True)
    message = models.TextField(blank=True)

    def __str__(self):
        return self.email


    
