from django.contrib import admin
from content.models import *
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

admin.site.site_header = "Maraka Administration Site"


class PromotionManagementAdminMixin:
    """Allow a dedicated promotion permission to access promotion admin models."""

    def has_module_permission(self, request):
        if request.user.has_perm('content.manage_promotions'):
            return True
        return super().has_module_permission(request)

    def has_view_permission(self, request, obj=None):
        if request.user.has_perm('content.manage_promotions'):
            return True
        return super().has_view_permission(request, obj)

    def has_add_permission(self, request):
        if request.user.has_perm('content.manage_promotions'):
            return True
        return super().has_add_permission(request)

    def has_change_permission(self, request, obj=None):
        if request.user.has_perm('content.manage_promotions'):
            return True
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if request.user.has_perm('content.manage_promotions'):
            return True
        return super().has_delete_permission(request, obj)

    def get_model_perms(self, request):
        perms = super().get_model_perms(request)
        if request.user.has_perm('content.manage_promotions'):
            perms['add'] = True
            perms['change'] = True
            perms['delete'] = True
            perms['view'] = True
        return perms


# ===== PROMOTION FLYERS ADMIN =====
class BannerAdmin(PromotionManagementAdminMixin, admin.ModelAdmin):
    """Admin interface for managing promotion banners (promotion flyers)"""
    list_display = ['title', 'owner', 'link', 'splashscreen', 'home', 'expire_date', 'days_until_expiry', 'is_active']
    list_filter = ['splashscreen', 'home', 'expire_date', 'created']
    search_fields = ['title', 'owner', 'link']
    readonly_fields = ['universal', 'created', 'expire_date_display']
    ordering = ['-created']
    
    fieldsets = (
        ('Promotion Content', {
            'fields': ('title', 'owner', 'link', 'display')
        }),
        ('Display Options', {
            'fields': ('splashscreen', 'home'),
            'description': 'Choose where this promotion appears in the app'
        }),
        ('Expiry Settings', {
            'fields': ('expire_date', 'expire_date_display')
        }),
        ('Metadata', {
            'fields': ('universal', 'created'),
            'classes': ('collapse',)
        }),
    )
    
    def days_until_expiry(self, obj):
        """Show days until this promotion expires"""
        if obj.expire_date:
            days = (obj.expire_date.date() - timezone.now().date()).days
            if days < 0:
                return f"Expired ({abs(days)} days ago)"
            elif days == 0:
                return "Expires today"
            else:
                return f"{days} days left"
        return "No expiry"
    days_until_expiry.short_description = "Status"
    
    def is_active(self, obj):
        """Show if promotion is currently active"""
        if obj.expire_date and obj.expire_date < timezone.now():
            return "❌ Expired"
        return "✅ Active"
    is_active.short_description = "Active"
    
    def expire_date_display(self, obj):
        """Display formatted expire date"""
        if obj.expire_date:
            return obj.expire_date.strftime("%Y-%m-%d %H:%M:%S")
        return "Not set"
    expire_date_display.short_description = "Expiry Date/Time"


class PromotionAdmin(BannerAdmin):
    """Admin interface for managing promotions"""
    pass


class FeaturedAdAdmin(PromotionManagementAdminMixin, admin.ModelAdmin):
    """Admin interface for managing featured ads (promotion flyers)"""
    list_display = ['title', 'owner', 'link', 'expire_date', 'days_until_expiry', 'is_active']
    list_filter = ['expire_date', 'created']
    search_fields = ['title', 'owner', 'link']
    readonly_fields = ['universal', 'created', 'expire_date_display']
    ordering = ['-created']
    
    fieldsets = (
        ('Featured Ad Content', {
            'fields': ('title', 'owner', 'link', 'display')
        }),
        ('Expiry Settings', {
            'fields': ('expire_date', 'expire_date_display')
        }),
        ('Metadata', {
            'fields': ('universal', 'created'),
            'classes': ('collapse',)
        }),
    )
    
    def days_until_expiry(self, obj):
        """Show days until this ad expires"""
        if obj.expire_date:
            days = (obj.expire_date.date() - timezone.now().date()).days
            if days < 0:
                return f"Expired ({abs(days)} days ago)"
            elif days == 0:
                return "Expires today"
            else:
                return f"{days} days left"
        return "No expiry"
    days_until_expiry.short_description = "Status"
    
    def is_active(self, obj):
        """Show if ad is currently active"""
        if obj.expire_date and obj.expire_date < timezone.now():
            return "❌ Expired"
        return "✅ Active"
    is_active.short_description = "Active"
    
    def expire_date_display(self, obj):
        """Display formatted expire date"""
        if obj.expire_date:
            return obj.expire_date.strftime("%Y-%m-%d %H:%M:%S")
        return "Not set"
    expire_date_display.short_description = "Expiry Date/Time"


class MultiImageAdmin(admin.ModelAdmin):
    """Admin interface for managing images"""
    list_display = ['id', 'created']
    list_filter = ['created']
    readonly_fields = ['created']
    ordering = ['-created']


admin.site.register(Banner, BannerAdmin)
admin.site.register(Promotion, PromotionAdmin)
admin.site.register(FeaturedAd, FeaturedAdAdmin)
admin.site.register(MultiImage, MultiImageAdmin)

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