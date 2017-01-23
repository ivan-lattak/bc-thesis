#!/usr/bin/env python3

import os
import sys
from subprocess import DEVNULL, \
                       CalledProcessError, TimeoutExpired, \
                       call, check_call

_RETURN_DIR = None

COMPILE_CMD = ['make', '-s', '-j4']

RUN_CMD = './main'
TIMEOUT = 10

CLEANUP_CMD = ['make', '-s', 'clean']

OK                  = 0
COMPILATION_FAILED  = 1
EXCEPTION           = 2
TIME_LIMIT_EXCEEDED = 3


def _cleanup(return_code):
    # call(CLEANUP_CMD, stdout=DEVNULL, stderr=DEVNULL) # recompile gtest lib every time
    os.chdir(_RETURN_DIR)
    return return_code


def _main():
    global _RETURN_DIR
    _RETURN_DIR = os.getcwd()
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    try:
        check_call(COMPILE_CMD)
    except CalledProcessError:
        return _cleanup(COMPILATION_FAILED)

    try:
        check_call(RUN_CMD, timeout=TIMEOUT)
    except CalledProcessError:
        return _cleanup(EXCEPTION)
    except TimeoutExpired:
        return _cleanup(TIME_LIMIT_EXCEEDED)

    return _cleanup(OK)

if __name__ == '__main__':
    sys.exit(_main())
