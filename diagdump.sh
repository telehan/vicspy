#!/bin/bash
./icscandump.py -f abs |\
    GREP_COLORS='mt=01;32' egrep --color=always -i " 705| 7df| 785" -A 1 -B 1
#    GREP_COLORS='mt=01;31' egrep --color=always -i " 705| 785| 7df" -A 1
#    GREP_COLORS='mt=01;32' egrep --color=always -i " 705| 785| 7df" -A 1 |\
#    GREP_COLORS='mt=01;31' egrep --color=always -i '^|Rx'

