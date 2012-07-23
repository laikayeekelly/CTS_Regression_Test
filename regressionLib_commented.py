import os
import sys
import ReportLib
from lxml import etree


def generate_regression_plan(report_file_list):

    #This function is used to find the location of the CTS report created by 
    # the latest CTS done
    def get_latest_result():
        folder = "../repository/result" 
        last_modified_file = ""
        latest_time = 0
        for r,d,f in os.walk(folder):
            for files in f:
                if files.endswith(".xml"):
                    filepath = os.path.join(r,files)
                    mtime = os.stat(filepath).st_mtime  
                    # get the file's latest modified time and stored in 'mtime'
                    if mtime > latest_time:
                        last_modified_file = filepath
                        latest_time = mtime

        return last_modified_file


    file = get_latest_result()
    report_file_list.append(file)
    # all the locations of the CTS report to be considered is stored in the 
    # variable report_file_list
    fail_found = False
    # fail_found is True if any failed test case is found in the CTS Report

    # The following is used to create a regression test plan based on the latest 
    # CTS done
    with open('ctsRegression.xml', 'w') as output:
        prev_package_name = ''

        output.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        output.write('<TestPlan version="1.0">\n')

        tree = etree.parse(file)
        find = etree.XPath("//Test[@result='fail']")
        for node in find(tree):
            while node.getparent().tag != 'TestResult':
                node = node.getparent()
            new_package_name = node.get("appPackageName")
            if new_package_name != prev_package_name: 
                prev_package_name = new_package_name
                xml_text = '  <Entry uri="' + new_package_name + '"/>\n'
                output.write(xml_text)
                fail_found = True

        output.write('</TestPlan>\n')

    print "finished generating regression test plan"
    return (report_file_list, fail_found)
    # fail_found is returned so that regression CTS test will not be done if no
    # failed test cases found


# The following function is used to generate the consolidated report 
def generate_consolidated_report(report_path, file_list):

    print "\nGenerating Consolidated Report\n"

    failcase = [{},{}]

    for each_file in file_list:
        failcase = ReportLib.find_fail_case(each_file, failcase)
        print "Finished processing file " + each_file
    ReportLib.write_to_output(report_path, failcase, len(file_list))

