from django import forms
from .models import User


class RefactoringForm(forms.Form):
    code = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 20, 'cols': 80}),
        label='',
    )

    tests = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 20, 'cols': 80}),
        label='',
    )


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        widgets = {'password': forms.PasswordInput}
