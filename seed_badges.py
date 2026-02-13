import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_pro.settings')
django.setup()

from gamification.models import Badge

def seed_badges():
    badges = [
        {
            'name': 'Early Bird',
            'description': 'Completed your first quiz!',
            'criteria': {'count': 1}
        },
        {
            'name': 'Scholar',
            'description': 'Scored 100% on a quiz.',
            'criteria': {'score': 100}
        },
        {
            'name': 'Persistent',
            'description': '7 day quiz streak!',
            'criteria': {'streak': 7}
        },
        {
            'name': 'Master',
            'description': 'Completed 10 quizzes.',
            'criteria': {'count': 10}
        }
    ]

    for b_data in badges:
        Badge.objects.get_or_create(
            name=b_data['name'],
            defaults={'description': b_data['description'], 'criteria': b_data['criteria']}
        )

    print(f"Successfully seeded {Badge.objects.count()} badges.")

if __name__ == "__main__":
    seed_badges()
