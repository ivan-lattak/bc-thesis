#!/bin/bash

cleanup() {
	killall sleep
	make -s clean
	exit 0
}

make -s -j4 || exit 1

(./main ; cleanup) & pid=$!
(sleep 10 && kill $pid && echo TLE)
exit 1
