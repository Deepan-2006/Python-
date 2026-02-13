from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, SubCategory, Question, Choice, QuizResult, QuizSession, Certificate
from django.utils import timezone
from .utils import generate_ai_questions, generate_certificate_number
from core.utils import get_ai_explanation, generate_performance_summary, generate_ai_recommendations
from gamification.models import Badge
from users.models import Profile

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'quizzes/category_list.html', {'categories': categories})

@login_required
def view_certificate(request, certificate_number):
    certificate = get_object_or_404(Certificate, certificate_number=certificate_number, user=request.user)
    return render(request, 'quizzes/certificate.html', {'certificate': certificate})


def subcategory_list(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    subcategories = category.subcategories.all()
    return render(request, 'quizzes/subcategory_list.html', {
        'category': category,
        'subcategories': subcategories
    })

@login_required
def quiz_config(request, subcategory_id):
    subcategory = get_object_or_404(SubCategory, id=subcategory_id)
    return render(request, 'quizzes/quiz_config.html', {'subcategory': subcategory})

@login_required
def start_quiz(request, subcategory_id):
    subcategory = get_object_or_404(SubCategory, id=subcategory_id)
    difficulty = request.GET.get('difficulty', 'medium')
    
    # Check if a session already exists for this subcategory and difficulty
    existing_session = QuizSession.objects.filter(
        user=request.user, 
        subcategory=subcategory, 
        difficulty=difficulty,
        is_completed=False
    ).first()
    
    if existing_session:
        return redirect('resume_quiz', session_id=existing_session.id)

    # If no enough questions in DB, generate via AI
    questions = Question.objects.filter(subcategory=subcategory, difficulty=difficulty)
    if questions.count() < 5:
        # Generate 5 questions dynamically
        new_questions = generate_ai_questions(subcategory.id, difficulty, count=5)
        questions = Question.objects.filter(subcategory=subcategory, difficulty=difficulty)
    else:
        questions = questions.order_by('?')[:10]

    # Create a new session
    session = QuizSession.objects.create(
        user=request.user,
        subcategory=subcategory,
        difficulty=difficulty
    )
    session.questions.set(questions)
    
    return render(request, 'quizzes/quiz_play.html', {
        'subcategory': subcategory,
        'questions': questions,
        'session': session
    })

@login_required
def resume_quiz(request, session_id):
    session = get_object_or_404(QuizSession, id=session_id, user=request.user)
    if session.is_completed:
        return redirect('dashboard')
        
    return render(request, 'quizzes/quiz_play.html', {
        'subcategory': session.subcategory,
        'questions': session.questions.all(),
        'session': session
    })

@login_required
def submit_quiz(request):
    if request.method == 'POST':
        subcategory_id = request.POST.get('subcategory_id')
        session_id = request.POST.get('session_id')
        subcategory = get_object_or_404(SubCategory, id=subcategory_id)
        session = get_object_or_404(QuizSession, id=session_id, user=request.user)
        
        # Get actual questions submitted
        question_ids = [k.split('_')[1] for k in request.POST.keys() if k.startswith('question_')]
        score_val = 0
        correct_count = 0
        total = len(question_ids)
        
        results_data = [] # To store for AI analysis

        for q_id in question_ids:
            q = Question.objects.get(id=q_id)
            selected_choice_id = request.POST.get(f'question_{q_id}')
            choice = None
            if selected_choice_id:
                choice = Choice.objects.get(id=selected_choice_id)
                if choice.is_correct:
                    correct_count += 1
            
            results_data.append({
                'question': q.text_en,
                'correct': choice.is_correct if choice else False,
                'selected': choice.text_en if choice else "No Answer"
            })
        
        if total > 0:
            score_val = (correct_count / total) * 100
        
        # Mark session as completed
        session.is_completed = True
        session.save()

        # Generate AI Summary
        user_history = QuizResult.objects.filter(user=request.user)
        ai_sum = generate_performance_summary(user_history)

        result = QuizResult.objects.create(
            user=request.user,
            subcategory=subcategory,
            category=subcategory.category,
            score=int(score_val),
            total_questions=total,
            correct_answers=correct_count,
            difficulty=session.difficulty,
            duration_seconds=request.POST.get('duration', 0),
            ai_summary=ai_sum,
            ai_recommendations=generate_ai_recommendations(subcategory.name_en, int(score_val))
        )

        
        # Add XP points to profile
        profile, created = Profile.objects.get_or_create(user=request.user)
        profile.points += int(score_val)
        profile.save()


        # STREAK LOGIC
        from gamification.models import Streak
        streak, created = Streak.objects.get_or_create(user=request.user)
        today = timezone.now().date()
        
        if created:
            streak.current_streak = 1
            streak.max_streak = 1
        else:
            if streak.last_activity_date == today:
                # Already active today, no change
                pass
            elif streak.last_activity_date == today - timezone.timedelta(days=1):
                # Active yesterday, increment
                streak.current_streak += 1
                if streak.current_streak > streak.max_streak:
                    streak.max_streak = streak.current_streak
            else:
                # Break in streak
                streak.current_streak = 1
        
        streak.last_activity_date = today
        streak.save()

        # CHECK BADGES
        from gamification.utils import check_and_award_badges
        new_badges = check_and_award_badges(request.user)

        # GENERATE CERTIFICATE


        if score_val >= 75:
            Certificate.objects.get_or_create(
                user=request.user,
                quiz_result=result,
                defaults={'certificate_number': generate_certificate_number()}
            )
        
        if new_badges:
            request.session['new_badge_ids'] = [b.id for b in new_badges]
        
        return redirect('quiz_result', result_id=result.id)
    return redirect('home')

@login_required
def quiz_result(request, result_id):
    result = get_object_or_404(QuizResult, id=result_id, user=request.user)
    certificate = Certificate.objects.filter(quiz_result=result).first()
    
    new_badge_ids = request.session.pop('new_badge_ids', [])
    newly_unlocked = Badge.objects.filter(id__in=new_badge_ids)
    
    return render(request, 'quizzes/result_page.html', {
        'result': result,
        'certificate': certificate,
        'newly_unlocked': newly_unlocked
    })



@login_required
def review_quiz(request, result_id):
    result = get_object_or_404(QuizResult, id=result_id, user=request.user)
    # Get questions from the subcategory
    questions = Question.objects.filter(subcategory=result.subcategory, difficulty=result.difficulty)
    
    # In a real app, we'd store which questions were in WHICH result
    # For now, we just show the subcategory questions
    for q in questions:
        correct_choice = q.choices.filter(is_correct=True).first()
        q.explanation = q.ai_explanation or get_ai_explanation(q, correct_choice, correct_choice)

    return render(request, 'quizzes/review_page.html', {
        'result': result,
        'questions': questions
    })

from django.http import JsonResponse

@login_required
def check_answer(request):
    choice_id = request.GET.get('choice_id')
    session_id = request.GET.get('session_id')
    choice = get_object_or_404(Choice, id=choice_id)
    session = get_object_or_404(QuizSession, id=session_id, user=request.user)
    
    is_correct = choice.is_correct
    if not is_correct and session.lives > 0:
        session.lives -= 1
        session.save()
        
    return JsonResponse({
        'is_correct': is_correct,
        'explanation': choice.question.ai_explanation,
        'remaining_lives': session.lives
    })



