from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
from django.conf import settings
import os


class Command(BaseCommand):
    help = "Initializes the site and social application for production."

    def handle(self, *args, **options):
        # Get the domain from environment or use default
        domain = os.environ.get("RENDER_EXTERNAL_HOSTNAME", "localhost")
        
        # 1. Update or create the Site object
        try:
            site, site_created = Site.objects.get_or_create(
                pk=settings.SITE_ID,
                defaults={"domain": domain, "name": "Todo App"}
            )
            if not site_created:
                site.domain = domain
                site.name = "Todo App"
                site.save()
            
            self.stdout.write(self.style.SUCCESS(f"✓ Site configured: {site.domain}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"✗ Error with Site: {e}"))
            return

        # 2. Get Google credentials from environment
        google_client_id = os.environ.get("GOOGLE_CLIENT_ID", "")
        google_client_secret = os.environ.get("GOOGLE_CLIENT_SECRET", "")

        # Skip if credentials are not set
        if not google_client_id or not google_client_secret:
            self.stdout.write(self.style.WARNING("⚠ GOOGLE_CLIENT_ID or GOOGLE_CLIENT_SECRET not set. Google login will not work."))
            return

        # 3. Create or update the Google SocialApp
        try:
            # Delete any existing Google SocialApp entries first to avoid duplicates
            SocialApp.objects.filter(provider="google").delete()
            
            # Create new Google SocialApp
            social_app = SocialApp.objects.create(
                provider="google",
                name="Google",
                client_id=google_client_id,
                secret=google_client_secret,
            )
            
            # Link the SocialApp to the Site
            social_app.sites.add(site)
            
            self.stdout.write(self.style.SUCCESS("✓ Google SocialApp created and linked to site"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"✗ Error creating/updating SocialApp: {e}"))
