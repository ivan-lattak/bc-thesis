#!/usr/bin/env python3

import os
import sys
from subprocess import run, PIPE, CalledProcessError

_RETURN_DIR = None

COMPILE_CMD = ['make', '-s', '-j4']a

RUN_CMD = './main'
TIMEOUT = 10

OK                  = 0
COMPILATION_FAILED  = 1
EXCEPTION           = 2
TIME_LIMIT_EXCEEDED = 3


def _print_process_output(process_obj):
    print(process_obj.stdout, end='')
    print(process_obj.stderr, end='', file=sys.stderr)


def _process_cleanup(process_obj, return_code):
    _print_process_output(process_obj)
    os.chdir(_RETURN_DIR)
    return return_code


def _main():
    global _RETURN_DIR
    _RETURN_DIR = os.getcwd()
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    try:
        process = run(COMPILE_CMD, stdout=PIPE, stderr=PIPE, check=True, encoding='utf-8')
    except CalledProcessError as error:
        return _process_cleanup(error, COMPILATION_FAILED)
    _print_process_output(process)

    try:
        process = run(RUN_CMD, stdout=PIPE, stderr=PIPE, timeout=TIMEOUT, check=True, encoding='utf-8')
    except CalledProcessError as error:
        return _process_cleanup(error, EXCEPTION)
    except TimeoutExpired as error:
        return _process_cleanup(error, TIME_LIMIT_EXCEEDED)

    return _process_cleanup(process, OK)

if __name__ == '__main__':
    sys.exit(_main())
