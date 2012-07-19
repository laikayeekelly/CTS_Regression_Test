import os
import sys
import ReportLib
from lxml import etree


def generate_regression_plan():

    def get_latest_result():
        folder = "../repository/results" 
        last_modified_file = ""
        latest_time = 0
        for r,d,f in os.walk(folder):
            for files in f:
                if files.endswith(".xml"):
                    filepath = os.path.join(r,files)
                    mtime = os.stat(filepath).st_mtime
                    if mtime > latest_time:
                        last_modified_file = filepath
                        latest_time = mtime
        print last_modified_file
        return last_modified_file


    file = get_latest_result()
    fail_found = False
    with open('ctsRegression.xml', 'w') as output:
        prev_package_name = ''

        output.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        output.write('<TestPlan version="1.0">\n')

        tree = etree.parse(file)

        find = etree.XPath("//Test[@result='fail']")
        for node in find(tree):
            while node.getparent().tag != 'TestResult':
                node = node.getparent()
            new_package_name = node.values()[1]
            if new_package_name != prev_package_name: 
                prev_package_name = new_package_name
                xml_text = '  <Entry uri="' + new_package_name + '"/>\n'
                output.write(xml_text)
                fail_found = True

        output.write('</TestPlan>\n')


    print "finished generating regression test plan"
    return fail_found


def generate_consolidated_report(report_path):

    failcase = [{},{}]

    file_list = ReportLib.list_files("../repository/results")
    for each_file in file_list:
        failcase = ReportLib.find_fail_case(each_file, failcase)
        print "Finished processing file " + each_file
    ReportLib.write_to_output(report_path, failcase, len(file_list))

