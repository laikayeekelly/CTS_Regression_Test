#!/usr/bin/env python
import os
import sys
import subprocess
import regressionLib
from time import sleep

#subprocess.call( ["cts-tradefed"])
#subprocess.call( ["run", "cts", "--plan", "CTS"])
sleep(1)
regression_done = 0
fail = regressionLib.generate_regression_plan()
sleep(1)
while (regression_done != 10) and (fail):
    print 'run regression test\n'
    #subprocess.call( ["cts-tradefed"])
    #subprocess.call( ["run", "cts", "--plan", "regressionCTS"])
    sleep(1)
    fail = regressionLib.generate_regression_plan()
    sleep(1)
    regression_done += 1

regressionLib.generate_consolidated_report(sys.argv[1])

print "Finished!!!"

