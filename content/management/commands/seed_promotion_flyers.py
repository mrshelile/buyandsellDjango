import os
from django.core.files import File
from django.core.management.base import BaseCommand
from django.utils import timezone
from content.models import Banner, FeaturedAd, MultiImage


class Command(BaseCommand):
    help = 'Seed promotion flyers from existing uploaded images'

    def handle(self, *args, **options):
        image_dir = os.path.join('uploads')
        candidates = [
            'maraka_flyer.jpg',
            'flyerdesign_26012023_193505.png',
            'flyer_20230212033741.jpeg',
            'page-1.png',
            'page-2.png',
        ]

        for filename in candidates:
            path = os.path.join(image_dir, filename)
            if not os.path.exists(path):
                continue

            image_obj, created = MultiImage.objects.get_or_create(image=filename)
            if not created and Banner.objects.filter(display=image_obj).exists() and FeaturedAd.objects.filter(display=image_obj).exists():
                continue

            if not Banner.objects.filter(display=image_obj).exists():
                Banner.objects.create(
                    title=f'{filename.replace(".jpg", "").replace(".png", "").replace(".jpeg", "").replace("_", " ").title()} Promo',
                    owner='Maraka',
                    link='https://maraka.co.ls',
                    display=image_obj,
                    expire_date=timezone.now() + timezone.timedelta(days=30),
                    splashscreen=True,
                    home=True,
                )

            if not FeaturedAd.objects.filter(display=image_obj).exists():
                FeaturedAd.objects.create(
                    title=f'{filename.replace(".jpg", "").replace(".png", "").replace(".jpeg", "").replace("_", " ").title()} Offer',
                    owner='Maraka',
                    link='https://maraka.co.ls',
                    display=image_obj,
                    expire_date=timezone.now() + timezone.timedelta(days=30),
                )

        self.stdout.write(self.style.SUCCESS('Promotion flyers seeded successfully'))
