from base64 import urlsafe_b64encode

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import authenticate, user_logged_in
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone

from django.conf import settings
from django.utils.module_loading import import_string

from content.models import Promotion, FeaturedAd, MultiImage, User
from content.serializers import PromotionFlyerSerializer
from rest_authtoken import settings as rat_settings
from rest_authtoken.models import AuthToken


class LoginView(APIView):
    def _get_user_serializer(self):
        serializer_class = getattr(rat_settings, 'USER_SERIALIZER', None)
        return import_string(serializer_class) if isinstance(serializer_class, str) else serializer_class
    permission_classes = []

    def post(self, request, format=None):
        username = request.data.get('username', '')
        email = request.data.get('email', '')
        password = request.data.get('password', '')

        user = None
        if username and password:
            user = authenticate(request, username=username, password=password)

        if not user and email and password:
            try:
                email_user = User.objects.get(email=email)
            except User.DoesNotExist:
                email_user = None
            if email_user:
                user = authenticate(request, username=email_user.username, password=password)

        if not user:
            return Response('invalid credentials', status=status.HTTP_401_UNAUTHORIZED)

        token = AuthToken.create_token_for_user(user)
        data = {'token': urlsafe_b64encode(token)}

        user_serializer = self._get_user_serializer()
        if user_serializer:
            data['user'] = user_serializer(instance=user, read_only=True).data

        user_logged_in.send(sender=user.__class__, request=request, user=user)
        return Response(data)


class PromotionFlyersView(APIView):
    def get(self, request, format=None):
        flyers = []

        promotions = Promotion.objects.filter(expire_date__gte=timezone.now()).order_by('-created')
        for promotion in promotions:
            image_url = ''
            if getattr(promotion.display, 'image', None):
                image_url = request.build_absolute_uri(promotion.display.image.url)
            image_urls = [
                request.build_absolute_uri(image.image.url)
                for image in promotion.displays.all()
                if getattr(image, 'image', None)
            ]
            if not image_urls and image_url:
                image_urls = [image_url]

            flyers.append({
                'id': promotion.id,
                'type': 'promotion',
                'title': promotion.title or promotion.owner or 'Promotion',
                'promotion_type': promotion.promotion_type,
                'link': promotion.link or '',
                'image_url': image_url,
                'image_urls': image_urls,
                'splashscreen': promotion.splashscreen,
                'home': promotion.home,
                'owner': promotion.owner or '',
                'expire_date': promotion.expire_date,
            })

        featured_ads = FeaturedAd.objects.filter(expire_date__gte=timezone.now()).order_by('-created')
        for ad in featured_ads:
            image_url = ''
            if getattr(ad.display, 'image', None):
                image_url = request.build_absolute_uri(ad.display.image.url)

            flyers.append({
                'id': ad.id,
                'type': 'promotion',
                'title': ad.title or ad.owner or 'Featured Ad',
                'link': ad.link or '',
                'image_url': image_url,
                'owner': ad.owner or '',
                'expire_date': ad.expire_date,
            })

        serializer = PromotionFlyerSerializer(flyers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


def handler404(request):
    return HttpResponseNotFound('<h1>500 Internal server error</h1>')

# Create your views here.
