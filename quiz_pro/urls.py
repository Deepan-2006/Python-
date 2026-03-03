from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('users/', include('users.urls')),
    path('quizzes/', include('quizzes.urls')),
    path('gamification/', include('gamification.urls')),
    path('accounts/', include('allauth.urls')),

    # Convenience redirects
    path('login/', lambda r: redirect('/users/login/')),
    path('register/', lambda r: redirect('/users/register/')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
