from io import BytesIO
from datetime import timedelta

from django.contrib.auth.models import Permission
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from PIL import Image
from rest_framework import status
from rest_framework.test import APIClient

from content.models import Banner, FeaturedAd, MultiImage, Promotion, User


class AuthCompatibilityTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='thabo@maraka.co.ls',
            email='thabo@maraka.co.ls',
            password='Lekoba@1',
        )

    def test_login_accepts_username_and_email_payload(self):
        response = self.client.post(
            '/buyandsellDjango-apis/auth/login/',
            {
                'username': 'thabo@maraka.co.ls',
                'email': 'thabo@maraka.co.ls',
                'password': 'Lekoba@1',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.json())

    def test_login_accepts_local_part_fallback(self):
        response = self.client.post(
            '/buyandsellDjango-apis/auth/login/',
            {
                'username': 'thabo',
                'email': 'thabo@maraka.co.ls',
                'password': 'Lekoba@1',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.json())


class PromotionFlyerAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

        image_file = BytesIO()
        Image.new('RGB', (100, 100), color='red').save(image_file, format='PNG')
        image_file.seek(0)

        self.image = MultiImage.objects.create(
            image=SimpleUploadedFile('promo.png', image_file.read(), content_type='image/png')
        )

        Promotion.objects.create(
            title='Summer Launch Promo',
            owner='Maraka',
            link='https://example.com/promo',
            display=self.image,
            expire_date=timezone.now() + timedelta(days=7),
            splashscreen=True,
            home=True,
        )

        FeaturedAd.objects.create(
            title='Weekend Deal',
            owner='Maraka',
            link='https://example.com/offer',
            display=self.image,
            expire_date=timezone.now() + timedelta(days=7),
        )

    def test_promotion_flyers_endpoint_returns_real_data(self):
        response = self.client.get(reverse('promotion-flyers'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertGreaterEqual(len(data), 2)
        self.assertTrue(all(item['type'] == 'promotion' for item in data))
        self.assertTrue(all('image_url' in item for item in data))
        titles = {item['title'] for item in data}
        self.assertIn('Summer Launch Promo', titles)
        self.assertIn('Weekend Deal', titles)


class PromotionAuthorizationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.image = MultiImage.objects.create(
            image=SimpleUploadedFile('auth-promo.png', b'not-a-real-image')
        )
        self.user = User.objects.create_user(
            username='ordinary@example.com',
            email='ordinary@example.com',
            password='ordinary-password',
        )
        self.manager = User.objects.create_user(
            username='manager@example.com',
            email='manager@example.com',
            password='manager-password',
            is_staff=True,
            is_superuser=True,
        )

    def _promotion_payload(self):
        return {
            'title': 'Fresh stock',
            'promotion_type': 'fresh_arrivals',
            'link': 'https://example.com',
            'display': self.image.id,
            'expire_date': timezone.now() + timedelta(days=7),
            'splashscreen': False,
            'home': True,
        }

    def test_ordinary_user_cannot_create_promotion(self):
        self.client.force_authenticate(self.user)
        response = self.client.post(
            '/buyandsellDjango-apis/promotions-create',
            self._promotion_payload(),
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(Promotion.objects.filter(title='Fresh stock').exists())

    def test_promotion_manager_can_create_typed_promotion(self):
        self.client.force_authenticate(self.manager)
        response = self.client.post(
            '/buyandsellDjango-apis/promotions-create',
            self._promotion_payload(),
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['promotion_type'], 'fresh_arrivals')

    def test_promotion_manager_can_create_with_multiple_images(self):
        second_image = MultiImage.objects.create(
            image=SimpleUploadedFile('second-promo.png', b'not-a-real-image')
        )
        self.client.force_authenticate(self.manager)
        payload = self._promotion_payload()
        payload['display'] = [self.image.id, second_image.id]

        response = self.client.post(
            '/buyandsellDjango-apis/promotions-create',
            payload,
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        promotion = Promotion.objects.get(title='Fresh stock')
        self.assertEqual(
            set(promotion.displays.values_list('id', flat=True)),
            {self.image.id, second_image.id},
        )

    def test_promotions_create_endpoint_accepts_get(self):
        response = self.client.get('/buyandsellDjango-apis/promotions-create')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_public_registration_cannot_grant_superuser(self):
        response = self.client.post(
            '/buyandsellDjango-apis/auth_user',
            {
                'username': 'registered@example.com',
                'email': 'registered@example.com',
                'password': 'ordinary-password',
                'is_active': True,
                'is_superuser': True,
                'validated': False,
                'otp': '',
                'full_name': 'Registered User',
                'phone1': '0000000000',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        registered = User.objects.get(email='registered@example.com')
        self.assertFalse(registered.is_superuser)
        self.assertFalse(registered.is_staff)

    def test_authenticated_superuser_can_grant_superuser_on_registration(self):
        self.client.force_authenticate(self.manager)
        response = self.client.post(
            '/buyandsellDjango-apis/auth_user',
            {
                'username': 'adminregistered@example.com',
                'email': 'adminregistered@example.com',
                'password': 'ordinary-password',
                'is_active': True,
                'is_superuser': True,
                'validated': False,
                'otp': '',
                'full_name': 'Admin Registered User',
                'phone1': '0000000000',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        registered = User.objects.get(email='adminregistered@example.com')
        self.assertTrue(registered.is_superuser)
        self.assertTrue(registered.is_staff)

    def test_manage_promotions_permission_is_available(self):
        permission = Permission.objects.filter(codename='manage_promotions').first()

        self.assertIsNotNone(permission)
        self.assertEqual(permission.name, 'Can manage promotions')
