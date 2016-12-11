#!/bin/bash

[ -d include ] || mkdir include
cat solution/sol1 from_browser solution/sol2 > include/solution.h

make -s -j 4 || exit

./main

# make -s clean
