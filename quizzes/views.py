from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, SubCategory, Question, Choice, QuizResult, QuizSession, Certificate
from django.utils import timezone
from .utils import generate_ai_questions, generate_certificate_number
from core.utils import get_ai_explanation, generate_performance_summary, generate_ai_recommendations
from gamification.models import Badge
from users.models import Profile
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.units import inch
import io
import os
from django.conf import settings


def category_list(request):
    technical_categories = Category.objects.filter(category_type='technical')
    non_technical_categories = Category.objects.filter(category_type='non-technical')
    entertainment_categories = Category.objects.filter(category_type='entertainment')
    return render(request, 'quizzes/category_list.html', {
        'technical_categories': technical_categories,
        'non_technical_categories': non_technical_categories,
        'entertainment_categories': entertainment_categories
    })


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
    
    # Premium check
    if subcategory.is_premium:
        from gamification.models import UserReward
        # Check if user has an active premium_unlock reward
        # For simplicity, we assume premium_unlock works for all topics for 1 day
        has_unlock = UserReward.objects.filter(
            user=request.user, 
            reward_type='premium_unlock',
            is_used=False
        ).exists()
        
        if not has_unlock:
            # You could redirect to a "Premium Required" page or show a message
            # For now, let's just add a flag to the context
            return render(request, 'quizzes/quiz_config.html', {
                'subcategory': subcategory,
                'premium_locked': True
            })

    return render(request, 'quizzes/quiz_config.html', {
        'subcategory': subcategory,
        'premium_locked': False
    })

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

    # Get topic-specific questions for this subcategory
    # First, try to get questions with the selected difficulty
    questions_query = Question.objects.filter(subcategory=subcategory, difficulty=difficulty)
    
    # If not enough questions with specific difficulty, get any questions from this topic
    if questions_query.count() < 10:
        questions_query = Question.objects.filter(subcategory=subcategory)
    
    # If still not enough questions, generate via AI until we have at least 10
    current_count = questions_query.count()
    if current_count < 10:
        needed = 10 - current_count
        generate_ai_questions(subcategory.id, difficulty, count=needed)
        # Refresh the query after generation
        questions_query = Question.objects.filter(subcategory=subcategory)
    
    # Randomly select exactly 10 questions
    questions = list(questions_query.order_by('?'))[:10]

    # Create a new session
    session = QuizSession.objects.create(
        user=request.user,
        subcategory=subcategory,
        difficulty=difficulty
    )
    
    # Check for Free Reattempt Reward (extra life)
    from gamification.models import UserReward
    reattempt_reward = UserReward.objects.filter(
        user=request.user, 
        reward_type='free_reattempt', 
        is_used=False
    ).first()
    
    if reattempt_reward:
        session.lives += 1 # Give an extra life
        session.save()
        # We don't mark as used yet, only on submit? 
        # Actually, it's safer to mark as used when it's consumed by a session.
        reattempt_reward.is_used = True
        reattempt_reward.save()

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
        
        # APPLY REWARDS (Daily Spin)
        from gamification.models import UserReward
        bonus_marks = 0
        point_multiplier = 1
        
        # Check for unused rewards
        active_rewards = UserReward.objects.filter(user=request.user, is_used=False).order_by('awarded_at')
        
        # We apply one of each type if available
        # Bonus Marks
        bonus_reward = active_rewards.filter(reward_type__startswith='bonus_marks_').first()
        if bonus_reward:
            bonus_val = 5 if bonus_reward.reward_type == 'bonus_marks_5' else 10
            bonus_marks = bonus_val
            bonus_reward.is_used = True
            bonus_reward.save()
            
        # Double Points
        double_reward = active_rewards.filter(reward_type='double_points').first()
        if double_reward:
            point_multiplier = 2
            double_reward.is_used = True
            double_reward.save()

        final_score = min(100, int(score_val) + bonus_marks)

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
            score=final_score,
            total_questions=total,
            correct_answers=correct_count,
            difficulty=session.difficulty,
            duration_seconds=request.POST.get('duration', 0),
            ai_summary=ai_sum,
            ai_recommendations=generate_ai_recommendations(subcategory.name_en, final_score)
        )

        
        # Add XP points to profile
        profile, created = Profile.objects.get_or_create(user=request.user)
        profile.points += int(score_val * point_multiplier)
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

@login_required
def download_certificate(request, certificate_number):
    try:
        certificate = Certificate.objects.get(certificate_number=certificate_number, user=request.user)
    except Certificate.DoesNotExist:
        return redirect('dashboard')

    # Create the PDF object, using the response object as its "file."
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Certificate_{certificate.certificate_number}.pdf"'

    # Create the PDF object, using the buffer as its "file."
    c = canvas.Canvas(response, pagesize=landscape(letter))
    width, height = landscape(letter)

    # --- CERTIFICATE DESIGN ---

    # Background
    c.setStrokeColor(colors.HexColor('#4F46E5')) # Primary color
    c.setLineWidth(5)
    c.rect(0.5*inch, 0.5*inch, width-1*inch, height-1*inch)
    
    c.setStrokeColor(colors.HexColor('#E5E7EB')) # Light border
    c.setLineWidth(2)
    c.rect(0.6*inch, 0.6*inch, width-1.2*inch, height-1.2*inch)

    # Title
    c.setFillColor(colors.HexColor('#111827'))
    c.setFont("Helvetica-Bold", 40)
    c.drawCentredString(width / 2, height - 2 * inch, "Certificate of Completion")

    # Subtitle
    c.setFont("Helvetica", 18)
    c.setFillColor(colors.HexColor('#6B7280'))
    c.drawCentredString(width / 2, height - 2.6 * inch, "This certificate is proudly presented to")

    # User Name
    c.setFont("Helvetica-BoldOblique", 32)
    c.setFillColor(colors.HexColor('#4F46E5'))
    user_name = f"{request.user.first_name} {request.user.last_name}" if request.user.first_name else request.user.username.upper()
    c.drawCentredString(width / 2, height - 3.5 * inch, user_name)
    
    c.setFillColor(colors.HexColor('#374151'))
    c.setFont("Helvetica", 16)
    c.drawCentredString(width / 2, height - 4.2 * inch, "For successfully completing the quiz in")

    # Quiz Topic
    quiz_name = certificate.quiz_result.subcategory.name_en if certificate.quiz_result.subcategory else "General Knowledge"
    c.setFont("Helvetica-Bold", 26)
    c.setFillColor(colors.black)
    c.drawCentredString(width / 2, height - 4.8 * inch, quiz_name)

    # Score & Date
    c.setFont("Helvetica", 16)
    c.setFillColor(colors.HexColor('#4B5563'))
    score_text = f"Achieving a score of {certificate.quiz_result.score}%"
    date_text = f"Awarded on {certificate.issued_at.strftime('%B %d, %Y')}"
    
    c.drawCentredString(width / 2, height - 5.8 * inch, score_text)
    c.drawCentredString(width / 2, height - 6.2 * inch, date_text)

    # Footer / ID
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.gray)
    c.drawString(0.8*inch, 0.8*inch, f"Certificate ID: {certificate.certificate_number}")
    c.drawRightString(width-0.8*inch, 0.8*inch, "Quiz Pro Certification Authority")

    c.showPage()
    c.save()
    return response



