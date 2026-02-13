from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('achievements/', views.achievements, name='achievements'),
]

