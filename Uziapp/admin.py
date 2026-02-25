from django.contrib import admin
from .models import Base, About, Project,  Service, SocialMediaLink, Team, Testimonial, Contact, ChooseUs

# Register your models here.
admin.site.register(Base)
admin.site.register(About)
admin.site.register(Contact)
admin.site.register(ChooseUs)
admin.site.register(Project)
admin.site.register(Service)
admin.site.register(SocialMediaLink)
admin.site.register(Team)
admin.site.register(Testimonial)


# @admin.register(Service)
# class ServiceAdmin(admin.ModelAdmin):
#     list_display = ('title', 'order', 'is_active')
#     list_filter = ('is_active',)
#     search_fields = ('title', 'description')
#     ordering = ('order',)

# @admin.register(SocialMediaLink)
# class SocialMediaLinkAdmin(admin.ModelAdmin):
#     list_display = ('platform', 'url', 'is_active', 'order')
#     list_filter = ('is_active',)