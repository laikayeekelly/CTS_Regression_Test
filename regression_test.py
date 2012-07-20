#!/usr/bin/env python
import os
import sys
import subprocess
import regressionLib
from time import sleep

report_file_list =[]

#subprocess.call( ["cts-tradefed"])
#subprocess.call( ["run", "cts", "--plan", "CTS"])

regression_done = 0
(report_file_list, fail) = regressionLib.generate_regression_plan(report_file_list)

while (regression_done != 5) and (fail):
    print 'run regression test\n'
    #subprocess.call( ["cts-tradefed"])
    #subprocess.call( ["run", "cts", "--plan", "regressionCTS"])
    (report_file_list, fail) = regressionLib.generate_regression_plan(report_file_list)
    regression_done += 1

regressionLib.generate_consolidated_report(sys.argv[1], report_file_list)

print "Finished!!!"

