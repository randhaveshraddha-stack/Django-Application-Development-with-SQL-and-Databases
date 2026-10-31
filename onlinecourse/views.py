from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Course, Enrollment, Submission, Question, Choice

@login_required
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        enrollment, created = Enrollment.objects.get_or_create(user=request.user, course=course)
        submission = Submission.objects.create(enrollment=enrollment)
        
        for question in course.question_set.all():
            for choice in question.choice_set.all():
                if f"choice_{choice.id}" in request.POST:
                    submission.choices.add(choice)
        
        submission.save()
        return redirect('onlinecourse:show_exam_result', course_id=course.id, submission_id=submission.id)
    
    return render(request, 'onlinecourse/course_details_bootstrap.html', {'course': course})

@login_required
def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    
    total_questions = course.question_set.count()
    correct_answers = 0
    
    for question in course.question_set.all():
        selected_choices = submission.choices.filter(question=question)
        correct_choices = question.choice_set.filter(is_correct=True)
        
        if set(selected_choices) == set(correct_choices):
            correct_answers += 1
            
    score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
    
    context = {
        'course': course,
        'submission': submission,
        'score': score,
    }
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
