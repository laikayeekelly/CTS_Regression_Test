#!/usr/bin/env python
import os
import sys
import ctsutil
from time import sleep
from ctsutil import run_test, generate_regression_plan, generate_consolidated_report


# This executable python file should be put in the folder android-cts/tools

if len(sys.argv) != 3:
    print "usage: regression.py no_of_regression output_csv"
    exit()

report_file_list = []
regression_done = 0
no_of_regression = int(sys.argv[1])

run_test()
report_file, fail = generate_regression_plan()
report_file_list.append(report_file)
while (regression_done != no_of_regression) and (fail):
    #print 'run regression test\n'
    run_test("regressionCTS") 
    report_file, fail = generate_regression_plan()
    report_file_list.append(report_file)
    regression_done += 1

generate_consolidated_report(sys.argv[2], report_file_list)

print "Finished!!!"
