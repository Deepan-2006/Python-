import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_pro.settings')
django.setup()

from quizzes.models import Category, SubCategory

def seed_data():
    data = {
        'Academic': ['Physics', 'Chemistry', 'Biology', 'Mathematics', 'Computer Science'],
        'Entertainment': ['Movies', 'Music', 'Gaming', 'Anime'],
        'Sports': ['Cricket', 'Football', 'Basketball', 'Tennis'],
        'General Knowledge': ['History', 'Geography', 'Current Affairs', 'Politics'],
        'Technology': ['Python Programming', 'Artificial Intelligence', 'Web Development', 'Cybersecurity']
    }

    for cat_name, sub_names in data.items():
        cat, _ = Category.objects.get_or_create(name_en=cat_name, defaults={'name_ta': cat_name})
        for sub_name in sub_names:
            SubCategory.objects.get_or_create(category=cat, name_en=sub_name, defaults={'name_ta': sub_name})

    print(f"Successfully seeded {Category.objects.count()} categories and {SubCategory.objects.count()} subcategories.")

if __name__ == "__main__":
    seed_data()
