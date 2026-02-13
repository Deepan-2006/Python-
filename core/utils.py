import random

def get_ai_explanation(question, selected_choice, correct_choice):
    """
    Simulates AI explanation generation. 
    In a real app, this would call OpenAI/Gemini API.
    """
    explanations = [
        f"The correct answer is '{correct_choice.text_en}'. This is because it directly addresses the core concept of the question.",
        f"While '{selected_choice.text_en}' might seem plausible, it's incorrect. The right choice is '{correct_choice.text_en}' based on standard principles.",
        f"Excellent choice! '{correct_choice.text_en}' is correct. Here's why: it accurately represents the facts in this domain.",
    ]
    return random.choice(explanations)

def generate_performance_summary(results):
    """
    Generates a smart summary of user performance.
    """
    if not results:
        return "Start taking quizzes to see your AI-powered performance analysis!"
    
    avg_score = sum([r.score for r in results]) / len(results)
    
    if avg_score >= 80:
        return "You're a Master! Your understanding of these topics is exceptional. We recommend trying harder difficulties."
    elif avg_score >= 50:
        return "Solid Progress. You have a good grasp of the basics, but there's room for improvement in specific complex areas."
    else:
        return "Focused Learning Needed. Your scores suggest you're struggling with some core concepts. Try focusing on the suggested weak areas."
def generate_ai_recommendations(subcategory_name, score):
    """
    Provides specific AI growth recommendations.
    """
    if score >= 90:
        return f"Outstanding! You've mastered {subcategory_name}. Your next step is to explore more advanced practical applications or mentor others in this topic."
    elif score >= 70:
        return f"Great job in {subcategory_name}. To reach perfection, try to focus on the edge cases and more complex problem sets within this subcategory."
    elif score >= 50:
        return f"You're on the right track with {subcategory_name}. We suggest reviewing the core fundamentals again and practicing with medium-difficulty questions."
    else:
        return f"It looks like {subcategory_name} is a bit challenging. Don't worry! Start by revisiting the introductory materials and focusing on one concept at a time."
