#!/usr/bin/env python
import os
import sys
import subprocess
import regressionLib
from time import sleep

# This executable python file should be put in the folder android-cts/tools

def run_test(plan_name, report_file_list) : 
    #subprocess.call( ["cts-tradefed"])
    #subprocess.call( ["run", "cts", "--plan", plan_name])
    subprocess.call( ["./helloworld"] )
    report_file_list, fail = regressionLib.generate_regression_plan(report_file_list)
    return (report_file_list, fail)


if len(sys.argv) != 3:
    print "usage: regression.py no_of_regression output_csv"
    exit()

report_file_list = []
regression_done = 0
no_of_regression = int(sys.argv[1])

report_file_list, fail = run_test("CTS", report_file_list)
while (regression_done != no_of_regression) and (fail):
    print 'run regression test\n'
    report_file_list, fail = run_test("regressionCTS", report_file_list) 
    regression_done += 1

regressionLib.generate_consolidated_report(sys.argv[2], report_file_list)

print "Finished!!!"

