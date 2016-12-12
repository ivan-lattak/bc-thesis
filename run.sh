#!/bin/bash

PATH=$PATH:/usr/bin

cleanup() {
	killall sleep
	# make -s clean
	exit
}

[ -d include ] || mkdir include
cat solution/sol1 from_browser solution/sol2 > include/solution.h

#make -s -j4 || exit

(./main ; cleanup) & pid=$!
(sleep 10 && kill $pid && echo TLE)

