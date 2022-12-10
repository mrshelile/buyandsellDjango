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
router.register(r'list_users', UserViewSet)
router.register(r'auth_user', CreateUserView)
router.register(r'banners', BannerViewSet)
router.register(r'featured-ads', FeaturedAdsViewSet)
router.register(r'product', ProductViewSet)
# router.register(r'user-product', UserProductViewset)


urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
#    path('api-token-auth/', views.obtain_auth_token, name='api_token_auth'),
   path('auth/', include('rest_authtoken.urls')),
   path('sendEmail/',SendEmailViewset.as_view()),
   re_path('user-product/(?P<owner>.+)',UserProductViewset.as_view())
    # path('auth/', include('rest_authtoken.urls')),
    # path('api-auth/', include('rest_framework.urls'))
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
