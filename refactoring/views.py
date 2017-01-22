import os
from subprocess import (
    STDOUT, CalledProcessError, check_output
)

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .util import file_read, file_write, ORIGINAL, TESTS, CODE, RUN_SCRIPT
from .forms import RefactoringForm, RegisterForm


def _form_submitted(request):
    return request.method == 'POST' and 'reset' not in request.POST


def _execute(form):
    try:
        os.makedirs(os.path.dirname(CODE))
    except OSError:
        pass
    file_write(CODE, form.cleaned_data['code'])

    try:
        if settings.DEBUG:
            return check_output(RUN_SCRIPT, stderr=STDOUT)
        return check_output(RUN_SCRIPT)
    except CalledProcessError as e:
        return "ERROR, return code = {}\n".format(e.returncode) + e.output.decode('utf-8')


def _original_code():
    return file_read(ORIGINAL)


def _original_tests():
    return file_read(TESTS)


@login_required
def index(request):
    form = RefactoringForm(initial = {
        'code': _original_code(),
        'tests': _original_tests(),
    })
    output = None

    if _form_submitted(request):
        form = RefactoringForm(request.POST)
        if form.is_valid():
            output = _execute(form)

    return render(
        request,
        'refactoring/index.html',
        {
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
