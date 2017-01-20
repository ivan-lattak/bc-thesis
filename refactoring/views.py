from django.shortcuts import render
from django.http import HttpResponse

from .forms import RefactoringForm


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
