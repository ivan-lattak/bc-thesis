import os
import sys
import shutil

from django.conf import settings

sys.dont_write_bytecode = True # prevent creation of __pycache__ in exercise_common
from .exercise_common import run

COMMON_DIR = os.path.join(settings.BASE_DIR, 'refactoring', 'exercise_common')


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


class ErrorCode:
    def __init__(self):
        raise NotImplementedError

    def format(self, output):
        raise NotImplementedError

    def is_ok(self):
        raise NotImplementedError

    @staticmethod
    def of(error_code):
        if error_code == run.OK:
            return _ErrorCodeOK()
        elif error_code == run.COMPILATION_FAILED:
            return _ErrorCodeCompFail()
        elif error_code == run.EXCEPTION:
            return _ErrorCodeException()
        elif error_code == run.TIME_LIMIT_EXCEEDED:
            return _ErrorCodeTLE()

    @staticmethod
    def ok():
        return _ErrorCodeOK()


class _ErrorCodeOK(ErrorCode):
    def __init__(self):
        pass

    def format(self, output):
        return "SUCCESS\n\n" + \
               "----- BEGIN OUTPUT -----\n" + \
               output + \
               "----- END OUTPUT -----"

    def is_ok(self):
        return True


class _ErrorCodeCompFail(ErrorCode):
    def __init__(self):
        pass

    def format(self, output):
        return "ERROR: The program failed to compile\n\n" + \
               "----- BEGIN OUTPUT -----\n" + \
               output + \
               "----- END OUTPUT -----"

    def is_ok(self):
        return False


class _ErrorCodeException(ErrorCode):
    def __init__(self):
        pass

    def format(self, output):
        return "ERROR: Errors occurred during program execution\n\n" + \
               "----- BEGIN OUTPUT -----\n" + \
               output + \
               "----- END OUTPUT -----"

    def is_ok(self):
        return False


class _ErrorCodeTLE(ErrorCode):
    def __init__(self):
        pass

    def format(self, output):
        return "ERROR: Time limit exceeded during execution\n\n" + \
               "----- BEGIN OUTPUT -----\n" + \
               output + \
               "----- TIME LIMIT EXCEEDED -----"

    def is_ok(self):
        return False
