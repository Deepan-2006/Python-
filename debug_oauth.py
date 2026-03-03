import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_pro.settings')
django.setup()

from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

print("--- SOCIAL APPS ---")
for app in SocialApp.objects.all():
    sites = [s.id for s in app.sites.all()]
    print(f"ID: {app.id}, Provider: {app.provider}, Name: {app.name}, Sites: {sites}")

print("\n--- SITES ---")
for site in Site.objects.all():
    print(f"ID: {site.id}, Domain: {site.domain}, Name: {site.name}")
