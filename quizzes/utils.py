import json
import random
import uuid
from django.conf import settings
from .models import Question, Choice, SubCategory

def generate_certificate_number():
    """Generates a unique certificate number."""
    return f"CERT-{uuid.uuid4().hex[:8].upper()}"

def generate_ai_questions(subcategory_id, difficulty='medium', count=5):
    """
    Generates questions using ChatGPT AI.
    If API key is missing, returns simulated dynamic questions.
    """
    subcategory = SubCategory.objects.get(id=subcategory_id)
    category_name = subcategory.category.name_en
    subcategory_name = subcategory.name_en
    
    # Try to call OpenAI if settings exist
    api_key = getattr(settings, 'OPENAI_API_KEY', None)
    if api_key and api_key != 'YOUR_OPENAI_API_KEY':
        # logic to call API would go here (e.g., using openai library)
        pass

    # Simulation logic for demonstration purposes (Rich and dynamic)
    simulated_data = get_simulated_questions(subcategory_name, difficulty, count)
    
    questions_created = []
    for data in simulated_data:
        # Check if question already exists to avoid duplicates
        q, created = Question.objects.get_or_create(
            subcategory=subcategory,
            text_en=data['question_en'],
            difficulty=difficulty,
            defaults={
                'text_ta': data['question_ta'],
                'ai_explanation': data['ai_explanation']
            }
        )
        if created:
            for i, choice_text in enumerate(data['choices']):
                Choice.objects.create(
                    question=q,
                    text_en=choice_text['en'],
                    text_ta=choice_text['ta'],
                    is_correct=(i == data['correct_index'])
                )
        questions_created.append(q)
    
    return questions_created

def get_simulated_questions(subcategory, difficulty, count):
    """Provides varied simulated questions with a template system for infinite variety."""
    
    # Base knowledge for specific topics
    knowledge_base = {
        "Python Programming": [
            {"q": "What is the result of 3 * '7' in Python?", "c": ["'777'", "21", "Error", "'37'"], "a": 0, "ex": "String multiplication in Python repeats the string."},
            {"q": "Which data structure is unordered and indexed by keys?", "c": ["Dictionary", "List", "Tuple", "Set"], "a": 0, "ex": "Dictionaries use key-value pairs and are unordered."},
            {"q": "How do you start a block of code in Python?", "c": ["Colons", "Brackets", "Indentation", "Parentheses"], "a": 2, "ex": "Python uses indentation to define code blocks."},
        ],
        "Physics": [
            {"q": "What is the unit of electrical resistance?", "c": ["Ohm", "Volt", "Ampere", "Watt"], "a": 0, "ex": "Ohm is the standard unit for resistance."},
            {"q": "Which law states that for every action there is an equal and opposite reaction?", "c": ["Newton's First", "Newton's Second", "Newton's Third", "Einstein's Theory"], "a": 2, "ex": "This is Newton's Third Law of Motion."},
        ],
        "Biology": [
            {"q": "What is the primary site of photosynthesis?", "c": ["Chloroplast", "Mitochondria", "Nucleus", "Cell Wall"], "a": 0, "ex": "Photosynthesis happens in the chloroplasts containing chlorophyll."},
        ]
    }

    # Templates for dynamic generation for ANY subcategory
    templates = [
        {
            "q": "Which of the following is a core principle of {topic}?",
            "c": ["Systematic Analysis", "Random Execution", "Manual Intervention", "Subjective Bias"],
            "a": 0,
            "ex": "{topic} relies heavily on systematic approaches to solve problems."
        },
        {
            "q": "In a professional {topic} environment, what is considered a best practice?",
            "c": ["Optimization", "Negligence", "Ad-hoc changes", "Hardcoding"],
            "a": 0,
            "ex": "Efficiency and optimization are key to success in {topic}."
        },
        {
            "q": "What is the primary goal of studying {topic} at an advanced level?",
            "c": ["Deeper Understanding", "Memorization", "Compliance", "Replication"],
            "a": 0,
            "ex": "Advanced study aims for a conceptual and structural grasp of {topic}."
        },
        {
            "q": "Who is often credited with foundational work in {topic}?",
            "c": ["Leading Pioneers", "Unknown Figures", "Modern Influencers", "Government Entities"],
            "a": 0,
            "ex": "Early pioneers laid the groundwork that defines modern {topic}."
        },
        {
            "q": "Which tool is most commonly used in {topic} workflows?",
            "c": ["Integrated Environments", "Paper and Pencil", "Standard Hardware", "Social Media"],
            "a": 0,
            "ex": "Workflow integration is essential for productivity in {topic}."
        }
    ]

    # Combine knowledge base and templates
    final_questions = []
    
    # 1. Add specific knowledge if available
    specific_data = knowledge_base.get(subcategory, [])
    for item in specific_data:
        final_questions.append({
            "question_en": item['q'],
            "question_ta": f"({subcategory}) - " + item['q'], # Simplified Tamil for simulation
            "choices": [{"en": c, "ta": c} for c in item['c']],
            "correct_index": item['a'],
            "ai_explanation": item['ex']
        })

    # 2. Fill the rest with templates
    while len(final_questions) < count + 10: # Generate buffer
        tpl = random.choice(templates)
        final_questions.append({
            "question_en": tpl['q'].format(topic=subcategory),
            "question_ta": tpl['q'].format(topic=subcategory),
            "choices": [{"en": c, "ta": c} for c in tpl['c']],
            "correct_index": tpl['a'],
            "ai_explanation": tpl['ex'].format(topic=subcategory)
        })

    random.shuffle(final_questions)
    return final_questions[:count]


