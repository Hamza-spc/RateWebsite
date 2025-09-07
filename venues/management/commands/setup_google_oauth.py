from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Set up Google OAuth social application'

    def handle(self, *args, **options):
        # Load environment variables
        from dotenv import load_dotenv
        load_dotenv()
        
        # Update site domain
        site = Site.objects.get_current()
        site.domain = '127.0.0.1:8000'
        site.name = 'TourInsight'
        site.save()
        self.stdout.write(self.style.SUCCESS('Updated site domain'))

        # Get Google OAuth credentials
        client_id = os.getenv('GOOGLE_CLIENT_ID', '')
        client_secret = os.getenv('GOOGLE_CLIENT_SECRET', '')
        
        if not client_id or not client_secret:
            self.stdout.write(
                self.style.ERROR('Google OAuth credentials not found in environment variables')
            )
            self.stdout.write('Please set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET in your .env file')
            return

        # Create or update Google social app
        google_app, created = SocialApp.objects.get_or_create(
            provider='google',
            defaults={
                'name': 'Google OAuth',
                'client_id': client_id,
                'secret': client_secret,
            }
        )
        
        if not created:
            google_app.client_id = client_id
            google_app.secret = client_secret
            google_app.save()
            self.stdout.write(self.style.SUCCESS('Updated Google OAuth app'))
        else:
            self.stdout.write(self.style.SUCCESS('Created Google OAuth app'))

        # Add site to the app
        google_app.sites.add(site)
        self.stdout.write(self.style.SUCCESS('Added site to Google OAuth app'))
        
        self.stdout.write(self.style.SUCCESS('Google OAuth setup complete!'))
        self.stdout.write('You can now test Google OAuth at: http://127.0.0.1:8000/accounts/login/')
