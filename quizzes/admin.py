from django.contrib import admin
from .models import Category, SubCategory, Question, Choice, QuizResult, QuizSession, Certificate

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'name_ta', 'created_at')
    search_fields = ('name_en', 'name_ta')

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'category', 'created_at')
    list_filter = ('category',)
    search_fields = ('name_en', 'name_ta')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text_en', 'subcategory', 'difficulty', 'created_at')
    list_filter = ('subcategory', 'difficulty')
    search_fields = ('text_en', 'text_ta')
    inlines = [ChoiceInline]

@admin.register(QuizSession)
class QuizSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'subcategory', 'difficulty', 'is_completed', 'started_at')
    list_filter = ('is_completed', 'difficulty')

@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'subcategory', 'score', 'completed_at')
    list_filter = ('subcategory', 'completed_at')
    readonly_fields = ('completed_at',)

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('user', 'certificate_number', 'issued_at')
    search_fields = ('certificate_number', 'user__username')


