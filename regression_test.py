#!/usr/bin/env python
import os
import sys
import ctsutil
from time import sleep
from ctsutil import run_test, cts_report_filter, consolidate_report, check_adb_connection


# This executable python file should be put in the folder android-cts/tools

if len(sys.argv) != 3:
    print "usage: regression.py max_regression output_csv"
    exit()

report_list = []
regression_count = 0
max_regression = int(sys.argv[1])-1

report, complete_execute = run_test()
report_list.append(report)
plan = cts_report_filter(report)
if complete_execute == False:
    check_adb_connection()
    exit()

while (regression_count < max_regression) and (plan != None):
    report, complete_execute = run_test(plan) 
    report_list.append(report)
    plan = cts_report_filter(report)
    regression_count += 1
    if complete_execute == False:
        check_adb_connection()
        exit()

consolidate_report(report_list, sys.argv[2])

print "Finished!!!"
