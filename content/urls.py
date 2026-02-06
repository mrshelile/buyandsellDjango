"""buyandsellDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from rest_framework import routers
from content.viewsets import *
from django.conf import settings
from django.conf.urls.static import static
# from rest_framework.authtoken import views

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'list_users', UserViewSet, basename='list_users')
router.register(r'auth_user', CreateUserView, basename='auth_user')
router.register(r'banners', BannerViewSet, basename='banners')
router.register(r'featured-ads', FeaturedAdsViewSet, basename='featured_ads')
router.register(r'product', ProductViewSet, basename='product')
router.register(r'product-create', ProductCreateViewset, basename='product_create')
router.register(r'multi-image', MuitiImageViewset, basename='multi_image')
router.register(r'visitor', VisitorViewset, basename='visitor')
router.register(r'car', CarViewset, basename='car')
router.register(r'banners-create', BannerCreateViewSet, basename='banners_create')
router.register(r'featured-ads-create', FeaturedAdsCreateViewSet, basename='featured_ads_create')
router.register(r'product-viewer', ViewerViewSet, basename='product_viewer')
router.register(r'server-time', ServerTimeViewSet, basename='server_time')


urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
#    path('api-token-auth/', views.obtain_auth_token, name='api_token_auth'),
   path('auth/', include('rest_authtoken.urls')),
   path('sendEmail/',SendEmailViewset.as_view()),
   path('reset-password',OTPUpdateViewset.as_view()),
   path('update-password',UpdatePasswordViewset.as_view()),
   path('validate-account',ValidateAccByOTpViewset.as_view()),
   re_path('user-product/(?P<owner>.+)',UserProductViewset.as_view()),
    # path('auth/', include('rest_authtoken.urls')),
    # path('api-auth/', include('rest_framework.urls'))
]
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


