#!/usr/bin/env python
import os
import sys
import ReportLib

failcase = {}
message = {}


if len(sys.argv) != 3:
    raise NameError("usage : ConsolidatedReport.py reports_folder output_csv")

if os.path.exists(sys.argv[1]) == False:
    raise NameError("folder doesn't exists")

file_list = ReportLib.list_files(sys.argv[1])
for each_file in file_list:
    failcase, message = ReportLib.find_fail_case(each_file, failcase, message)
    print "Finished processing file " + each_file
ReportLib.write_to_output(sys.argv[2], failcase, message, len(file_list))

print "Finished!!!"

