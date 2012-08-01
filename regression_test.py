#!/usr/bin/env python
import os
import sys
import ctsutil
from time import sleep
from ctsutil import run_test, cts_report_filter, consolidate_report


# This executable python file should be put in the folder android-cts/tools

if len(sys.argv) != 3:
    print "usage: regression.py max_regression output_csv"
    exit()

report_list = []
regression_count = 0
max_regression = int(sys.argv[1])

report = run_test()
report_list.append(report)
plan = cts_report_filter(report)
while (regression_count < max_regression) and (plan != None):
    print 'Finished generating regression test plan and start running regression test\n'
    report = run_test(plan) 
    report_list.append(report)
    plan = cts_report_filter(report)
    regression_count += 1

consolidate_report(report_list, sys.argv[2])

print "Finished!!!"
