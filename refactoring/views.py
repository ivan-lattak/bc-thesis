from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import login

from .forms import RefactoringForm, UserForm


def _form_submitted(request):
    return request.method == 'POST' and 'reset' not in request.POST


def index(request):
    form = RefactoringForm()
    output = None

    if _form_submitted(request):
        form = RefactoringForm(request.POST)
        if form.is_valid():
            output = form.execute()

    return render(
        request,
        'refactoring/index.html',
        {
            'form': form, 
            'output': output,
        }
    )


def register(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            login(new_user)
            return HttpResponseRedirect('refactoring/')

    return render(request, 'refactoring/register.html', {'form': form})
