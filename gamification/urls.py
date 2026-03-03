from django.urls import path
from . import views

urlpatterns = [
    path('daily-spin/', views.daily_spin, name='daily_spin'),
    path('spin-api/', views.spin_api, name='spin_api'),
]
