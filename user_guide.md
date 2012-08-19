## Program user guide

### installing the lxml package into python

1.	apt-get install libxml2-dev libxslt-dev

2.	apt-get install python-lxml


### run the regression_test.py on Ubuntu device

1.	Put regression_test.py and ctsutil.py into android-cts/tools folder

2.	Follow the instruction for running a CTS except the step for running the CTS

3.	Open the terminal and change directory to android-cts/tools

4.	Run regression_test.py using the following command

1.	chmod 544 regression_test.py

2.	regression_test.py (no_of_regression) (output csv report filename)

(In case if the program is run on CTS of version 3.0 to 2.0, download ctsutil_cts2_0 .py and change its name to ctsutil.py)

### run the consolidatedReport.py

1.	Make sure  you have both ConsolidatedReport.py and ReportLib.py in the same folder

2.	Put all the CTS result folder into one folder

3.	Using the command line prompt and type the following command
	‘ConsolidatedReport.py (report_folder_name) (output_file_name) ’