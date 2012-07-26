import os
import sys
import subprocess
from lxml import etree
from re import sub
from operator import itemgetter
from itertools import groupby

report_folder_path = "../repository/results" 
regression_plan_file_path = "../repository/plan/ctsRegression.xml"
tool_to_run_cts = "cts-tradefed"

def run_test(plan_name = 'CTS'): 
    #subprocess.call( [tool_to_run_cts])
    #subprocess.call( ["run", "cts", "--plan", plan_name])
    #subprocess.call( ["./helloworld"])
    print "finish running test"

def generate_regression_plan():

    def get_latest_result():
        folder = report_folder_path
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

        return last_modified_file


    report_file = get_latest_result()
    fail_found = False

    with open(regression_plan_file_path, 'w') as output:
        prev_package_name = ''

        output.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        output.write('<TestPlan version="1.0">\n')

        tree = etree.parse(report_file)
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

    return (report_file, fail_found)


def generate_consolidated_report(report_path, file_list):

    def find_fail_case(file, failcase, message):

        def buildkey(node):
            key_list = []
            while node.getparent().tag != 'TestResult':
                key_list.append(node.get("name"))
                node = node.getparent()
            key_list.append(node.get("appPackageName"))
            key_list.reverse()
            key = key_list[0]
            if len(key_list) >= 2:
                key += '\t' + '.'.join(key_list[1:len(key_list)-1])
            key += '\t' + key_list[len(key_list)-1]

            return key


        tree = etree.parse(file)
        find = etree.XPath("//Test[@result='fail']")
        for node in find(tree):
            key = buildkey(node)
            failedScene_node = node.find("FailedScene")
            if failedScene_node != None:
                fail_message = sub('\r\n|\r', ' ', failedScene_node.get("message").encode('ascii', 'ignore'))
            else:
                fail_message = ' '
            if key in failcase.keys():
                failcase[key] += 1
                if fail_message not in message[key]:
                    message[key].append(fail_message)
            else:
                failcase[key] = 1
                message[key] = [fail_message]

        return (failcase, message)


    def write_to_output(output_file_name, failcase, message, no_of_files):

        def sort_fail_cases_into_desired_format(failcase, message, no_of_files):

            failcase_dict = {}

            for case, chance in failcase.iteritems():
                failcase_dict.setdefault(chance, [])
                failcase_dict[chance].append(case)

            chance_list = reversed(failcase_dict.keys())
            output_list = [[str(chance)+'\t'+str(no_of_files)+'\t'+ case +'\t'+ \
                          '\t'.join(message[case])+'\n' for case in \
                          sorted(failcase_dict[chance])] for chance in chance_list]
            return output_list


        output_list = sort_fail_cases_into_desired_format(failcase, message, no_of_files)
        with open(output_file_name, 'w') as output_file:
            for chance in output_list:
                for case in chance:
                    output_file.write(case)


    print "\nGenerating Consolidated Report\n"

    failcase = {}
    message = {}

    for each_file in file_list:
        failcase, message = find_fail_case(each_file, failcase, message)
        print "Finished processing file " + each_file
    write_to_output(report_path, failcase, message, len(file_list))

