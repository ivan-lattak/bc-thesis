import os
import shutil
import errno

from django.conf import settings

COMMON_DIR = os.path.join(settings.BASE_DIR, 'refactoring', 'exercise_common')

TESTS_HEADER = os.path.join(COMMON_DIR, 'tests_header')


def file_read(path):
    with open(path) as file:
        return file.read()


def file_write(path, contents):
    with open(path, 'w') as file:
        file.write(contents)


def copy_anything(src, dst):
    try:
        shutil.copytree(src, dst)
    except NotADirectoryError:
        shutil.copy2(src, dst)


class ExercisePaths:
    def __init__(self, username, exercise_id):
        self._exercise_dir = os.path.join(settings.BASE_DIR, 'refactoring',
                                          'exercises', username, exercise_id)

    def exercise_dir(self):
        return self._exercise_dir

    def include_dir(self):
        return os.path.join(self.exercise_dir(), 'include')

    def code_file(self):
        return os.path.join(self.include_dir(), 'solution.h')

    def tests_file(self):
        return os.path.join(self.exercise_dir(), 'tests.cc')

    def run_script(self):
        return os.path.join(self.exercise_dir(), 'run.py')
