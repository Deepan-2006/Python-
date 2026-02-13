from quizzes.models import Category, Question, Choice
import random

def seed_data():
    # 1. Create Categories
    categories = [
        {
            'name_en': 'Science & Technology',
            'name_ta': 'அறிவியல் மற்றும் தொழில்நுட்பம்',
            'description': 'Explore the wonders of the physical world and digital innovation.'
        },
        {
            'name_en': 'World History',
            'name_ta': 'உலக வரலாறு',
            'description': 'Travel back in time to the events that shaped our modern world.'
        },
        {
            'name_en': 'Python Programming',
            'name_ta': 'பைதான் நிரலாக்கம்',
            'description': 'Master the most popular language for AI and Data Science.'
        }
    ]
    
    cat_objs = []
    for cat in categories:
        obj, created = Category.objects.get_or_create(
            name_en=cat['name_en'],
            defaults={'name_ta': cat['name_ta'], 'description': cat['description']}
        )
        cat_objs.append(obj)
    
    # 2. Create Questions for Python
    python_cat = cat_objs[2]
    questions = [
        {
            'en': 'What is the correct file extension for Python files?',
            'ta': 'பைதான் கோப்புகளுக்கான சரியான கோப்பு நீட்டிப்பு என்ன?',
            'choices': [
                {'en': '.py', 'ta': '.py', 'correct': True},
                {'en': '.python', 'ta': '.python', 'correct': False},
                {'en': '.pt', 'ta': '.pt', 'correct': False},
                {'en': '.pyt', 'ta': '.pyt', 'correct': False},
            ],
            'explanation': 'Python files use the .py extension by convention.'
        },
        {
            'en': 'Which of these is used to define a block of code in Python?',
            'ta': 'பைதானில் ஒரு குறியீடு தொகுதியை வரையறுக்க இவற்றில் எது பயன்படுத்தப்படுகிறது?',
            'choices': [
                {'en': 'Indentation', 'ta': 'உள்தள்ளல்', 'correct': True},
                {'en': 'Curly braces', 'ta': 'நெளிப்பு அடைப்புக்குறிகள்', 'correct': False},
                {'en': 'Parentheses', 'ta': 'அடைப்புக்குறிகள்', 'correct': False},
                {'en': 'Semicolons', 'ta': 'அரைப்புள்ளிகள்', 'correct': False},
            ],
            'explanation': 'Unlike many other languages, Python uses indentation to indicate code blocks.'
        }
    ]
    
    for q in questions:
        q_obj, created = Question.objects.get_or_create(
            category=python_cat,
            text_en=q['en'],
            defaults={'text_ta': q['ta'], 'ai_explanation': q['explanation']}
        )
        for c in q['choices']:
            Choice.objects.get_or_create(
                question=q_obj,
                text_en=c['en'],
                text_ta=c['ta'],
                is_correct=c['correct']
            )

if __name__ == "__main__":
    seed_data()
    print("Seed data created successfully.")
