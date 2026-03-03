from django.urls import path
from . import views

urlpatterns = [
    path('', views.category_list, name='category_list'),
    path('category/<int:category_id>/subcategories/', views.subcategory_list, name='subcategory_list'),
    path('subcategory/<int:subcategory_id>/config/', views.quiz_config, name='quiz_config'),
    path('subcategory/<int:subcategory_id>/start/', views.start_quiz, name='start_quiz'),
    path('quiz/submit/', views.submit_quiz, name='submit_quiz'),
    path('result/<int:result_id>/', views.quiz_result, name='quiz_result'),
    path('result/<int:result_id>/review/', views.review_quiz, name='review_quiz'),
    path('session/<int:session_id>/resume/', views.resume_quiz, name='resume_quiz'),

    path('certificate/<str:certificate_number>/', views.view_certificate, name='view_certificate'),
    path('certificate/<str:certificate_number>/download/', views.download_certificate, name='download_certificate'),
    path('quiz/check-answer/', views.check_answer, name='check_answer'),
]



