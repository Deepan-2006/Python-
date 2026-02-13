from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from quizzes.models import Category, SubCategory, QuizResult, QuizSession
from users.models import User
from django.db.models import Sum

def home(request):
    categories = Category.objects.all()[:6]
    return render(request, 'core/home.html', {'categories': categories})

@login_required
def dashboard(request):
    results = QuizResult.objects.filter(user=request.user).order_by('-completed_at')
    total_score = results.aggregate(Sum('score'))['score__sum'] or 0
    recent_results = results[:5]
    
    # Incomplete quizzes
    incomplete_quizzes = QuizSession.objects.filter(user=request.user, is_completed=False).order_by('-started_at')
    
    # Rankings
    rankings = User.objects.all().order_by('-profile__points')[:5]
    
    # Simple Weak Area detection (Logic for AI Smart Learning)
    weak_categories = []
    if results.exists():
        weak_categories = SubCategory.objects.filter(quizresult__user=request.user, quizresult__score__lt=60).distinct()

    return render(request, 'core/dashboard.html', {
        'total_score': total_score,
        'results': results,
        'recent_results': recent_results,
        'weak_categories': weak_categories,
        'incomplete_quizzes': incomplete_quizzes,
        'rankings': rankings
    })


from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Avg, Count

@staff_member_required
def admin_dashboard(request):
    total_users = User.objects.count()
    total_quizzes = QuizResult.objects.count()
    avg_score = QuizResult.objects.aggregate(Avg('score'))['score__avg'] or 0
    most_attempted = Category.objects.annotate(attempts=Count('quizresult')).order_by('-attempts')[:5]
    
    users_performance = User.objects.annotate(
        avg_user_score=Avg('quiz_results__score'),
        total_quizzes=Count('quiz_results')
    ).order_by('-avg_user_score')

    return render(request, 'core/admin_dashboard.html', {
        'total_users': total_users,
        'total_quizzes': total_quizzes,
        'avg_score': avg_score,
        'most_attempted': most_attempted,
        'users_performance': users_performance,
    })

def leaderboard(request):
    top_users = User.objects.filter(profile__isnull=False).order_by('-profile__points')[:10]
    
    user_rank = None
    if request.user.is_authenticated:
        # Calculate rank manually if not in top 10
        all_ranks = User.objects.filter(profile__isnull=False).order_by('-profile__points')
        for i, u in enumerate(all_ranks):
            if u == request.user:
                user_rank = i + 1
                break
                
    return render(request, 'core/leaderboard.html', {
        'top_users': top_users,
        'user_rank': user_rank
    })

from gamification.models import Badge, UserBadge, Streak

@login_required
def achievements(request):
    all_badges = Badge.objects.all()
    user_badges = UserBadge.objects.filter(user=request.user).values_list('badge_id', flat=True)
    streak, _ = Streak.objects.get_or_create(user=request.user)
    
    return render(request, 'core/achievements.html', {
        'all_badges': all_badges,
        'user_badges': user_badges,
        'streak': streak
    })
