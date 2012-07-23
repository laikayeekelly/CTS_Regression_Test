#!/usr/bin/env python
import os
import sys
import subprocess
import regressionLib
from time import sleep

# This executable python file should be put in the folder android-cts/tools

report_file_list = []


if len(sys.argv) != 3:
    raise NameError("usage: regression.py no_of_regression output_csv")

#subprocess.call( ["cts-tradefed"])
#subprocess.call( ["run", "cts", "--plan", "CTS"])

no_of_regression = int(sys.argv[1])
regression_done = 0
(report_file_list, fail) = regressionLib.generate_regression_plan(report_file_list)

while (regression_done != no_of_regression) and (fail):
    print 'run regression test\n'
    #subprocess.call( ["cts-tradefed"])
    #subprocess.call( ["run", "cts", "--plan", "regressionCTS"])
    (report_file_list, fail) = regressionLib.generate_regression_plan(report_file_list)
    regression_done += 1

regressionLib.generate_consolidated_report(sys.argv[2], report_file_list)

print "Finished!!!"

