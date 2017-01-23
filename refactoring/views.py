import os
from subprocess import (
    DEVNULL, STDOUT, CalledProcessError, check_output
)
from operator import attrgetter

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db import IntegrityError

from .util import (
        file_read, file_write, copy_anything, COMMON_DIR, TESTS_HEADER,
        ExercisePaths, ErrorCode
)
from .forms import RefactoringForm, RegisterForm
from .models import Exercise, Solution


def _refactoring_form_submitted(request):
    return request.method == 'POST' and 'compileandrun' in request.POST


def _copy_common_files(exercise_dir):
    for item in os.listdir(COMMON_DIR):
        src_abspath = os.path.join(COMMON_DIR, item)
        dst_abspath = os.path.join(exercise_dir, item)
        copy_anything(src_abspath, dst_abspath)


def _prepare_exercise_dir(form, ep):
    try:
        os.makedirs(ep.exercise_dir())
        _copy_common_files(ep.exercise_dir())
    except FileExistsError:
        pass

    os.makedirs(ep.include_dir(), exist_ok=True)
    file_write(ep.code_file(), form.cleaned_data['code'])
    file_write(ep.tests_file(), form.cleaned_data['tests'])


def _save_solution(code, creator, exercise):
    try:
        solution = Solution.objects.create(
                code=code,
                sub_date=timezone.now(),
                creator=creator,
                exercise=exercise,
        )
        solution.save()
    except IntegrityError:
        pass


def _execute_exercise(form, ep):
    _prepare_exercise_dir(form, ep)

    err_output = STDOUT if settings.DEBUG else DEVNULL

    try:
        output = check_output(ep.run_script(), stderr=err_output).decode('utf-8')
        error_code = ErrorCode.ok()
    except CalledProcessError as e:
        output = e.output.decode('utf-8')
        error_code = ErrorCode.of(e.returncode)

    return error_code.is_ok(), error_code.format(output)


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


def _user_solutions(exercise, user):
    return exercise.solution_set.filter(creator=user).order_by('-sub_date')


def _latest_solution(solutions):
    return solutions.first()


def _solution_selected(request):
    return request.method == 'GET' and 'solution' in request.GET


@login_required
def index(request):
    return HttpResponse("Welcome to the index.")


@login_required
def detail(request, exercise_id):
    exercise = get_object_or_404(Exercise, id=exercise_id)
    solutions = _user_solutions(exercise, request.user)
    if _solution_selected(request):
        selected = get_object_or_404(Solution, id=request.GET['solution'])
    else:
        selected = _latest_solution(solutions)

    initial_code = selected.code if selected else _original_code(exercise)
    initial_tests = _all_tests(exercise)

    form = RefactoringForm(initial={
        'code': initial_code,
        'tests': initial_tests,
    })
    output = None

    if _refactoring_form_submitted(request):
        form = RefactoringForm(request.POST, initial={
            'code': initial_code,
            'tests': initial_tests,
        })
        if form.is_valid():
            ep = ExercisePaths(request.user.username, exercise_id)
            execution_ok, output = _execute_exercise(form, ep)
            if execution_ok:
                _save_solution(form.cleaned_data['code'], request.user, exercise)
                solutions = _user_solutions(exercise, request.user)
                selected = _latest_solution(solutions)

    return render(
        request,
        'refactoring/detail.html',
        {
            'exercise_id': exercise.id,
            'exercise_text': exercise.exercise_text,
            'solutions': solutions,
            'selected': selected,
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
