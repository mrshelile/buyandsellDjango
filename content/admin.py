from django.contrib import admin
from content.models import *
admin.site.site_header = "Maraka Administration Site"
admin.site.register(Banner)
admin.site.register(FeaturedAd)
admin.site.register(Visitor)
admin.site.register(User)
admin.site.register(Product)
# Register your models here.
