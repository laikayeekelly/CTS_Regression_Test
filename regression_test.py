#!/usr/bin/env python
import os
import sys
import regressionLib
from time import sleep

# This executable python file should be put in the folder android-cts/tools

if len(sys.argv) != 3:
    print "usage: regression.py no_of_regression output_csv"
    exit()

report_file_list = []
regression_done = 0
no_of_regression = int(sys.argv[1])

report_file_list, fail = regressionLib.run_test("CTS", report_file_list)
while (regression_done != no_of_regression) and (fail):
    print 'run regression test\n'
    report_file_list, fail = regressionLib.run_test("regressionCTS", report_file_list) 
    regression_done += 1

print "report_file_list: " 
print report_file_list
regressionLib.generate_consolidated_report(sys.argv[2], report_file_list)

print "Finished!!!"
