from django.urls import path
from . import views

app_name = 'onlinecourse'
urlpatterns = [
    # Existing routes (like index, login, logout, etc.) would go here
    
    # Route for submitting the exam
    path('<int:course_id>/submit/', views.submit, name='submit'),
    
    # Route for showing the exam result
    path('course/<int:course_id>/submission/<int:submission_id>/result/', views.show_exam_result, name='show_exam_result'),
]
