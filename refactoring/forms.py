import os
from subprocess import check_output, STDOUT, CalledProcessError

from django import forms

from .util import file_read, file_write, ORIGINAL, TESTS, CODE, RUN_SCRIPT


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

    def execute(self):
        try:
            os.makedirs(os.path.dirname(CODE))
        except OSError:
            pass
        file_write(CODE, self.cleaned_data['code'])

        try:
            return check_output(RUN_SCRIPT, stderr=STDOUT)
        except CalledProcessError as e:
            return "ERROR, error code = {}\n".format(e.returncode) + e.output.decode('utf-8')
