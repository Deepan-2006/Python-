from django.db import models
from users.models import User

class Badge(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='badges/')
    criteria = models.JSONField(help_text="JSON object defining requirement, e.g. {'score': 90, 'count': 5}")

    def __str__(self):
        return self.name

class UserBadge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    awarded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'badge')

class Streak(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='streak_info')
    current_streak = models.IntegerField(default=0)
    max_streak = models.IntegerField(default=0)
    last_activity_date = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.current_streak} days"

class DailySpinTracker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='spin_tracks')
    date = models.DateField(auto_now_add=True)
    spins_used = models.IntegerField(default=0)

    class Meta:
        unique_together = ('user', 'date')

    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.spins_used} spins"

class UserReward(models.Model):
    REWARD_TYPES = (
        ('bonus_marks_5', '+5 Bonus Marks'),
        ('bonus_marks_10', '+10 Bonus Marks'),
        ('free_reattempt', '1 Free Reattempt Token'),
        ('premium_unlock', 'Unlock Premium Topic (1 Day)'),
        ('points_50', '50 Reward Points'),
        ('points_100', '100 Reward Points'),
        ('double_points', 'Double Points in Next Quiz'),
        ('surprise_unlock', 'Surprise Quiz Unlock'),
        ('better_luck', 'Better Luck Next Time'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rewards')
    reward_type = models.CharField(max_length=50, choices=REWARD_TYPES)
    is_used = models.BooleanField(default=False)
    awarded_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_reward_type_display()}"
