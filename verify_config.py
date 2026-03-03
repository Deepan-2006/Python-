import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_pro.settings')
django.setup()

from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp

try:
    s = Site.objects.get(id=1)
    print(f"SITE_DOMAIN: '{s.domain}'")
    print(f"SITE_NAME: '{s.name}'")
except Site.DoesNotExist:
    print("SITE ID 1 NOT FOUND")

# Check social apps
apps = SocialApp.objects.all()
if apps.exists():
    for app in apps:
        print(f"SocialApp in DB: {app.name} ({app.provider})")
else:
    print("No SocialApps found in Database.")
