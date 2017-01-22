from django import forms
from django.contrib.auth.models import User

from .util import file_read, ORIGINAL, TESTS


class RefactoringForm(forms.Form):
    code = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 20, 'cols': 80}),
        initial=file_read(ORIGINAL),
        label='',
    )

    tests = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 20, 'cols': 80}),
        initial=file_read(TESTS),
        label='',
    )
    tests.disabled = True


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        widgets = {'password': forms.PasswordInput}
