#!/usr/bin/env python
import os
import django
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todo_project.settings')
django.setup()

from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
from django.conf import settings

def setup_google_oauth():
    """Setup Google OAuth application with credentials from .env file"""
    
    # Get the default site
    site = Site.objects.get(id=settings.SITE_ID)
    
    # Check if Google app already exists
    google_apps = SocialApp.objects.filter(provider='google')
    
    if google_apps.exists():
        print(f"Found {google_apps.count()} existing Google OAuth apps. Cleaning up...")
        google_apps.delete()
    
    # Get Google OAuth credentials from environment
    client_id = os.getenv('GOOGLE_CLIENT_ID')
    client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
    
    print(f"Client ID from env: {client_id[:20]}..." if client_id else "Client ID: Not found")
    print(f"Client Secret from env: {client_secret[:20]}..." if client_secret else "Client Secret: Not found")
    
    if not client_id or not client_secret:
        print("ERROR: GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET must be set in environment variables.")
        print("Please check your .env file.")
        return None
    
    # Create new Google OAuth app
    google_app = SocialApp.objects.create(
        provider='google',
        name='Google',
        client_id=client_id.strip(),
        secret=client_secret.strip(),
    )
    
    # Add the site to the app
    google_app.sites.add(site)
    
    print(f"✅ Successfully created Google OAuth app with ID: {google_app.id}")
    print(f"Client ID: {client_id[:20]}...")
    print(f"Associated with site: {site.domain}")
    
    return google_app

if __name__ == "__main__":
    try:
        setup_google_oauth()
        print("\n🚀 Google OAuth setup completed successfully!")
        print("You can now test the login functionality.")
    except Exception as e:
        print(f"❌ Error setting up Google OAuth: {e}")
