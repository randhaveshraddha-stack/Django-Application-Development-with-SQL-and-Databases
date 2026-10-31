from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Course, Enrollment, Submission, Question, Choice

# --- Starter Code Views (Keeps your app running) ---
def registration_request(request):
    if request.method == 'POST':
        user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'])
        login(request, user)
        return redirect('onlinecourse:index')
    return render(request, 'onlinecourse/registration.html')

def login_request(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('onlinecourse:index')
    return render(request, 'onlinecourse/login.html')

def logout_request(request):
    logout(request)
    return redirect('onlinecourse:index')

class CourseListView(generic.ListView):
    template_name = 'onlinecourse/course_list_bootstrap.html'
    context_object_name = 'course_list'
    def get_queryset(self):
        return Course.objects.all()

class CourseDetailView(generic.DetailView):
    model = Course
    template_name = 'onlinecourse/course_details_bootstrap.html'

def enroll(request, course_id):
    if request.method == 'POST':
        course = get_object_or_404(Course, pk=course_id)
        Enrollment.objects.get_or_create(user=request.user, course=course)
        return HttpResponseRedirect(reverse('onlinecourse:course_details', args=(course.id,)))

# --- Final Project Assessment Views (For Tasks 5 and 7) ---
@login_required
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        enrollment, _ = Enrollment.objects.get_or_create(user=request.user, course=course)
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
    selected_ids = [choice.id for choice in submission.choices.all()]
    total_questions = course.question_set.count()
    correct_answers = 0
    for question in course.question_set.all():
        if question.is_get_score(selected_ids):
            correct_answers += 1
    grade = 0
    if total_questions > 0:
        grade = int((correct_answers / total_questions) * 100)
    context = {'course': course, 'selected_ids': selected_ids, 'grade': grade}
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
