from django.contrib import admin
from content.models import *
from django.core.mail import send_mail
from django.conf import settings
admin.site.site_header = "Maraka Administration Site"
admin.site.register(Banner)
admin.site.register(FeaturedAd)
admin.site.register(Visitor)
admin.site.register(Product)
admin.site.register(MultiImage)
admin.site.register(Car)
admin.site.register(Viewer)

# Register your models here.
@admin.action(description='Send OTP')
def make_published(modeladmin, request, queryset):
    # users=[]
    for element in queryset.values():
        if element["otp"]:
            email = element['email']
            subject= "OTP CODE"
            body = "go to the app and add this otp code " +element['otp']
        
            send_mail(
                subject,
                body,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            print(element)
    
class UserAdmin(admin.ModelAdmin):
    # list_display = ['title', 'status']
    # ordering = ['title']
    actions = [make_published]

admin.site.register(User, UserAdmin)