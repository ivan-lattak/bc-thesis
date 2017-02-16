import os
from subprocess import (
    DEVNULL, STDOUT, CalledProcessError, check_output
)
from operator import attrgetter

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db import IntegrityError

from .util import (
        file_read, file_write, copy_anything,
        COMMON_DIR,
        ExercisePaths, ErrorCode
)
from .forms import RefactoringForm, RegisterForm
from .models import Exercise, Session, Solution

User = get_user_model()


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


def _save_solution(code, tests, session, parent):
    try:
        solution = Solution.objects.create(
                code=code,
                tests=tests,
                sub_date=timezone.now(),
                session=session,
                parent=parent,
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
    return exercise.original_tests


def _solutions_by_sub_date_desc(session):
    return session.solution_set.order_by('-sub_date')


def _solutions_by_sub_date_asc(session):
    return session.solution_set.order_by('sub_date')


def _latest_solution(session):
    return session.solution_set.order_by('-sub_date').first()


def _get_session_or_create(request, exercise):
    if request.method == 'GET' and 'session_id' in request.GET.keys():
        request.session['session_id'] = request.GET['session_id']

    if 'session_id' in request.session.keys():
        try:
            return request.user.session_set.get(id=request.session['session_id'])
        except Session.DoesNotExist:
            pass

    sessions = request.user.session_set.filter(exercise=exercise).order_by('-id')
    if sessions:
        session = sessions.first()
        request.session['session_id'] = session.id
        return session

    session = Session.objects.create(user=request.user, exercise=exercise)
    session.save()
    request.session['session_id'] = session.id
    return session


def _get_exercises_in_order():
    return Exercise.objects.order_by('id')


def _get_solution_or_None(request, session):
    if request.method == 'GET' and 'solution_id' in request.GET.keys():
        request.session['solution_id'] = request.GET['solution_id']

    if 'solution_id' in request.session.keys():
        try:
            return session.solution_set.get(id=request.session['solution_id'])
        except Solution.DoesNotExist:
            pass

    solutions = session.solution_set.order_by('-sub_date')
    if solutions:
        solution = solutions.first()
        request.session['solution_id'] = solution.id
        return solution

    return None


@login_required
def index(request):
    exercises = _get_exercises_in_order()
    return render(request, 'refactoring/index.html', {'exercises': exercises})


@login_required
def detail(request, exercise_id):
    exercise = get_object_or_404(Exercise, id=exercise_id)
    session = _get_session_or_create(request, exercise)
    solutions = _solutions_by_sub_date_desc(session)
    selected_solution = _get_solution_or_None(request, session)

    initial_code = selected_solution.code if selected_solution else _original_code(exercise)
    initial_tests = selected_solution.tests if selected_solution else _original_tests(exercise)

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
                parent_solution = selected_solution
                _save_solution(form.cleaned_data['code'], form.cleaned_data['tests'], session, parent_solution)
                selected_solution = _latest_solution(session)
                request.session['solution_id'] = selected_solution.id

    return render(
        request,
        'refactoring/detail.html',
        {
            'exercise_id': exercise.id,
            'exercise_text': exercise.exercise_text,
            'session': session,
            'selected_solution': selected_solution,
            'form': form, 
            'output': output,
        }
    )


@login_required
def sessions(request, exercise_id):
    exercise = get_object_or_404(Exercise, id=exercise_id)
    selected_session = _get_session_or_create(request, exercise)
    sessions = request.user.session_set.filter(exercise=exercise).order_by('-id')

    return render(
        request,
        'refactoring/sessions.html',
        {
            'exercise_id': exercise.id,
            'sessions': sessions,
            'selected_session': selected_session,
        }
    )


@login_required
def solutions(request, exercise_id):
    exercise = get_object_or_404(Exercise, id=exercise_id)
    selected_session = _get_session_or_create(request, exercise)
    solutions = _solutions_by_sub_date_asc(selected_session)
    selected_solution = _get_solution_or_None(request, selected_session)

    return render(
        request,
        'refactoring/solutions.html',
        {
            'exercise_id': exercise.id,
            'selected_session': selected_session,
            'solutions': solutions,
            'selected_solution': selected_solution,
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
