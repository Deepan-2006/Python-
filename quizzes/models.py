from django.db import models
from users.models import User

class Category(models.Model):
    CATEGORY_TYPES = (
        ('technical', 'Technical'),
        ('non-technical', 'Non-Technical'),
        ('entertainment', 'Entertainment'),
    )

    name_en = models.CharField(max_length=100)
    name_ta = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    category_type = models.CharField(max_length=20, choices=CATEGORY_TYPES, default='technical')
    icon = models.ImageField(upload_to='categories/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name_en} ({self.get_category_type_display()})"

    class Meta:
        verbose_name_plural = "Categories"

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    name_en = models.CharField(max_length=100)
    name_ta = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_premium = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category.name_en} - {self.name_en}"

    class Meta:
        verbose_name_plural = "Subcategories"

class Question(models.Model):
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='questions', null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='questions', null=True, blank=True)
    text_en = models.TextField()
    text_ta = models.TextField()
    ai_explanation = models.TextField(blank=True, null=True)
    difficulty_choices = (
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    )
    difficulty = models.CharField(max_length=10, choices=difficulty_choices, default='medium')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text_en[:50]

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text_en = models.CharField(max_length=255)
    text_ta = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text_en

class QuizSession(models.Model):
    """Tracks an ongoing or incomplete quiz session."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_sessions')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    difficulty = models.CharField(max_length=10, default='medium')
    current_question_index = models.IntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    lives = models.IntegerField(default=1) # "Spin the wheel" chance
    started_at = models.DateTimeField(auto_now_add=True)
    
    questions = models.ManyToManyField(Question)

    def __str__(self):
        return f"{self.user.username} - {self.subcategory.name_en} ({'Completed' if self.is_completed else 'In Progress'})"

class QuizResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_results')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    score = models.IntegerField()
    total_questions = models.IntegerField()
    correct_answers = models.IntegerField()
    difficulty = models.CharField(max_length=10, default='medium')
    duration_seconds = models.IntegerField()
    completed_at = models.DateTimeField(auto_now_add=True)
    
    # Strengths & Weaknesses analysis (AI summary) / Reference links
    ai_summary = models.TextField(blank=True, null=True)
    ai_recommendations = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.score}%"

class Certificate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certificates')
    quiz_result = models.OneToOneField(QuizResult, on_delete=models.CASCADE, related_name='certificate')
    certificate_number = models.CharField(max_length=20, unique=True)
    issued_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Certificate {self.certificate_number} - {self.user.username}"


