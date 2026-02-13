from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    email_verified = models.BooleanField(default=False)
    is_2fa_enabled = models.BooleanField(default=False)
    failed_login_attempts = models.IntegerField(default=0)
    last_login_attempt = models.DateTimeField(null=True, blank=True)
    is_locked = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    points = models.IntegerField(default=0)
    @property
    def get_rank(self):
        if self.points >= 5000: return 'Legend'
        if self.points >= 2500: return 'Diamond'
        if self.points >= 1000: return 'Platinum'
        if self.points >= 500: return 'Gold'
        if self.points >= 200: return 'Silver'
        if self.points >= 100: return 'Bronze'
        return 'Beginner'

    @property
    def rank_color(self):
        colors = {
            'Legend': '#ff3e3e', 'Diamond': '#3498db', 'Platinum': '#1abc9c',
            'Gold': '#f1c40f', 'Silver': '#bdc3c7', 'Bronze': '#cd7f32', 'Beginner': '#95a5a6'
        }
        return colors.get(self.get_rank, '#95a5a6')

    streak = models.IntegerField(default=0)

    last_quiz_date = models.DateField(null=True, blank=True)
    language_preference = models.CharField(max_length=10, default='en', choices=(('en', 'English'), ('ta', 'Tamil')))

    def __str__(self):
        return f"{self.user.username}'s Profile"
