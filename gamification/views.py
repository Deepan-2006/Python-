import random
from datetime import date, timedelta
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from .models import DailySpinTracker, UserReward, Streak
from users.models import Profile

@login_required
def daily_spin(request):
    today = date.today()
    tracker, created = DailySpinTracker.objects.get_or_create(user=request.user, date=today)
    
    # Check for streak extra spin
    # Suppose if streak >= 5, they get 1 extra spin (total 4)
    streak_obj, _ = Streak.objects.get_or_create(user=request.user)
    max_spins = 3
    if streak_obj.current_streak >= 5:
        max_spins = 4
        
    spins_left = max_spins - tracker.spins_used
    
    # Recent rewards for context
    recent_rewards = UserReward.objects.filter(user=request.user).order_by('-awarded_at')[:5]
    
    context = {
        'spins_used': tracker.spins_used,
        'spins_left': max(0, spins_left),
        'max_spins': max_spins,
        'recent_rewards': recent_rewards,
        'current_streak': streak_obj.current_streak,
    }
    return render(request, 'gamification/spin_wheel.html', context)

@login_required
def spin_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request'}, status=400)
    
    today = date.today()
    tracker, created = DailySpinTracker.objects.get_or_create(user=request.user, date=today)
    
    streak_obj, _ = Streak.objects.get_or_create(user=request.user)
    max_spins = 3
    if streak_obj.current_streak >= 5:
        max_spins = 4
        
    if tracker.spins_used >= max_spins:
        return JsonResponse({
            'success': False,
            'message': 'Daily spin limit reached. Please come back tomorrow!'
        })
    
    # Define reward probabilities
    # Weights: Better Luck (20), 50 Points (20), +5 Marks (15), +10 Marks (10), 100 Points (10), 
    # Double Points (10), Reattempt (5), Premium Unlock (5), Surprise Unlock (5)
    rewards_pool = [
        ('better_luck', 20),
        ('points_50', 20),
        ('bonus_marks_5', 15),
        ('bonus_marks_10', 10),
        ('points_100', 10),
        ('double_points', 10),
        ('free_reattempt', 5),
        ('premium_unlock', 5),
    ]
    
    reward_type = random.choices(
        [r[0] for r in rewards_pool],
        weights=[r[1] for r in rewards_pool]
    )[0]
    
    # Create the reward
    reward = UserReward.objects.create(
        user=request.user,
        reward_type=reward_type
    )
    
    # Immediate application for points
    if reward_type == 'points_50':
        profile = request.user.profile
        profile.points += 50
        profile.save()
        reward.is_used = True
        reward.save()
    elif reward_type == 'points_100':
        profile = request.user.profile
        profile.points += 100
        profile.save()
        reward.is_used = True
        reward.save()
        
    # Increment spin count
    tracker.spins_used += 1
    tracker.save()
    
    return JsonResponse({
        'success': True,
        'reward_type': reward_type,
        'reward_display': reward.get_reward_type_display(),
        'spins_left': max_spins - tracker.spins_used
    })
