import os

from django.conf import settings

EXERCISE_DIR = os.path.join(settings.BASE_DIR, 'refactoring', 'exercise')

ORIGINAL     = os.path.join(EXERCISE_DIR, 'original'             )
TESTS        = os.path.join(EXERCISE_DIR, 'tests.cc'             )
CODE         = os.path.join(EXERCISE_DIR, 'include', 'solution.h')
RUN_SCRIPT   = os.path.join(EXERCISE_DIR, 'run.py'               )


def file_read(path):
    with open(path) as file:
        return file.read()


def file_write(path, contents):
    with open(path, 'w') as file:
        file.write(contents)
