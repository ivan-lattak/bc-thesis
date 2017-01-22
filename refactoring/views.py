import os
from subprocess import (
    STDOUT, CalledProcessError, check_output
)
from operator import attrgetter

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .util import file_read, file_write, copy_anything, COMMON_DIR, TESTS_HEADER, ExercisePaths
from .forms import RefactoringForm, RegisterForm
from .models import Exercise


def _form_submitted(request):
    return request.method == 'POST' and 'reset' not in request.POST


def _prepare_exercise_dir(exercise_dir):
    for item in os.listdir(COMMON_DIR):
        src_abspath = os.path.join(COMMON_DIR, item)
        dst_abspath = os.path.join(exercise_dir, item)
        copy_anything(src_abspath, dst_abspath)


def _execute_exercise(form, ep):
    try:
        os.makedirs(ep.exercise_dir())
        _prepare_exercise_dir(ep.exercise_dir())
    except FileExistsError:
        pass

    os.makedirs(ep.include_dir(), exist_ok=True)
    file_write(ep.code_file(), form.cleaned_data['code'])
    file_write(ep.tests_file(), form.cleaned_data['tests'])

    try:
        if settings.DEBUG:
            return check_output(ep.run_script(), stderr=STDOUT)
        return check_output(ep.run_script())
    except CalledProcessError as e:
        return "ERROR, return code = {}\n".format(e.returncode) + e.output.decode('utf-8')


def _original_code(exercise):
    return exercise.original_code


def _original_tests(exercise):
    header = file_read(TESTS_HEADER)
    test_cases = map(attrgetter('code'), exercise.testcase_set.all())
    return header + '\n\n'.join(test_cases)


def _user_tests(exercise):
    return ''


def _all_tests(exercise):
    return _original_tests(exercise) + '\n\n' + _user_tests(exercise)


@login_required
def index(request):
    return HttpResponse("Welcome to the index.")


@login_required
def detail(request, exercise_id):
    exercise = get_object_or_404(Exercise, id=exercise_id)
    original_code = _original_code(exercise)
    original_tests = _all_tests(exercise)

    form = RefactoringForm(initial={
        'code': original_code,
        'tests': original_tests,
    })
    output = None

    if _form_submitted(request):
        form = RefactoringForm(request.POST, initial={
            'code': original_code,
            'tests': original_tests,
        })
        if form.is_valid():
            ep = ExercisePaths(request.user.username, exercise_id)
            output = _execute_exercise(form, ep)

    return render(
        request,
        'refactoring/detail.html',
        {
            'exercise_id': exercise.id,
            'exercise_text': exercise.exercise_text,
            'form': form, 
            'output': output,
        }
    )


def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            new_user.save()
            login(request, new_user)
            return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)

    return render(request, 'registration/register.html', {'form': form})
