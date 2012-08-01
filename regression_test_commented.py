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

# the file path of all the test result reports of those CTS testings done in
# this program will be stored in the variable report_list
# which these report files are used to generate the consolidated report
report = run_test()
report_list.append(report)
plan = cts_report_filter(report)
while (regression_count < max_regression) and (plan != None):
    # if test plan is '' meaning that there's no failed test cases found
    # thus no regression test will be done
    print 'Finished generating regression test plan and start running regression test\n'
    report = run_test(plan) 
    report_list.append(report)
    plan = cts_report_filter(report)
    regression_count += 1

consolidate_report(report_list, sys.argv[2])

print "Finished!!!"
