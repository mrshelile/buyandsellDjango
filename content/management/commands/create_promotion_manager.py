from django.core.management.base import BaseCommand, CommandError
from content.models import User


class Command(BaseCommand):
    help = 'Create or update a user who can manage promotions.'

    def add_arguments(self, parser):
        parser.add_argument('email')
        parser.add_argument('--password', required=True)
        parser.add_argument('--full-name', default='')

    def handle(self, *args, **options):
        email = options['email'].strip().lower()
        if not email:
            raise CommandError('Email is required.')

        user, created = User.objects.get_or_create(
            email=email,
            defaults={'username': email, 'full_name': options['full_name']},
        )
        user.username = email
        user.full_name = options['full_name'] or user.full_name
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.validated = True
        user.set_password(options['password'])
        user.save()

        action = 'Created' if created else 'Updated'
        self.stdout.write(self.style.SUCCESS(f'{action} promotion manager: {email}'))