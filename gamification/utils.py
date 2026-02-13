from .models import Badge, UserBadge, Streak
from quizzes.models import QuizResult

def check_and_award_badges(user):
    """
    Checks if the user meets criteria for any locked badges and awards them.
    """
    unlocked_badge_ids = UserBadge.objects.filter(user=user).values_list('badge_id', flat=True)
    locked_badges = Badge.objects.exclude(id__in=unlocked_badge_ids)
    
    results = QuizResult.objects.filter(user=user)
    total_quizzes = results.count()
    highest_score = results.order_by('-score').first().score if results.exists() else 0
    
    try:
        streak = user.streak_info.current_streak
    except:
        streak = 0

    new_badges = []

    for badge in locked_badges:
        criteria = badge.criteria
        is_eligible = False
        
        # Check criteria (simple logic based on our seed data)
        # criteria: {'count': 1}, {'score': 100}, {'streak': 7}, {'count': 10}
        
        if 'count' in criteria:
            if total_quizzes >= criteria['count']:
                is_eligible = True
                
        if 'score' in criteria:
            if highest_score >= criteria['score']:
                is_eligible = True
                
        if 'streak' in criteria:
            if streak >= criteria['streak']:
                is_eligible = True
                
        if is_eligible:
            UserBadge.objects.get_or_create(user=user, badge=badge)
            new_badges.append(badge)
            
    return new_badges
