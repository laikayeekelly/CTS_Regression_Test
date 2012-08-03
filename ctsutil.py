import os
import sys
import subprocess
import codecs
import time
from lxml import etree
from re import sub


result_folder_path = "../repository/results"
regression_plan_file_path = "../repository/plan/ctsRegression.xml"
tool_to_run_cts = "./cts-tradefed"
regression_plan_name = "ctsRegression"
sec_for_test_finish = 6*60*60

def run_test(plan_name = 'CTS'):

    process = subprocess.Popen(tool_to_run_cts + " run cts --plan " + plan_name, 
                             shell = True)
    time.sleep(sec_for_test_finish)
    subprocess.Popen.kill(process)

    print "finish running test"

    file_list = [[os.path.join(r,files) for files in f 
                if files.endswith(".xml")]
                for r,d,f in os.walk(result_folder_path)]
    file_list = sum(file_list, [])
    file_list.sort(key=lambda x: os.path.getmtime(x))
    last_modified_file = file_list[-1]

    return last_modified_file


def cts_report_filter(report_file):


    plan = None

    with open(regression_plan_file_path, 'w') as output:
        prev_package_name = ''

        output.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        output.write('<TestPlan version="1.0">\n')

        tree = etree.parse(report_file)
        find = etree.XPath("//Test[@result='fail']")
        for node in find(tree):
            plan = regression_plan_name
            while node.getparent().tag != 'TestResult':
                node = node.getparent()
            new_package_name = node.get("appPackageName")
            if new_package_name != prev_package_name: 
                prev_package_name = new_package_name
                output.write('  <Entry uri="' + new_package_name + '"/>\n')

        output.write('</TestPlan>\n')


    return plan


def consolidate_report(file_list, output_file_path):


    def find_fail_case(file):


        def buildkey(node):
            key_list = []
            while node.getparent().tag != 'TestResult':
                key_list.append(node.get("name"))
                node = node.getparent()
            key_list.append(node.get("appPackageName"))
            key_list.reverse()
            key = key_list[0]
            if len(key_list) >= 2:
                key += '\t' + '.'.join(key_list[1:-1])
            key += '\t' + key_list[-1]

            return key


        tree = etree.parse(file)
        find = etree.XPath("//Test[@result='fail']")
        for node in find(tree):
            key = buildkey(node)
            failedScene_node = node.find("FailedScene")
            if failedScene_node != None:
                fail_message = sub('\r\n|\r', ' ', 
                                   failedScene_node.get("message"))
            else:
                fail_message = ' '
            if key in failcase.keys():
                failcase[key] += 1
            else:
                failcase[key] = 1
                message[key] = set()

            message[key].add(fail_message)


    def write_to_output(no_of_files, output_file_path):


        def group_failcase(no_of_files):

            failcase_dict = {}

            for case, chance in failcase.iteritems():
                failcase_dict.setdefault(chance, [])
                failcase_dict[chance].append(case)

            chance_list = reversed(failcase_dict.keys())

            output_list = []
            for chance in chance_list:
                for case in sorted(failcase_dict[chance]):
                    output_list.append(str(chance)+'\t'+str(no_of_files)+'\t'+ 
                                       case +'\t'+ '\t'.join(message[case]))

            return output_list

        with codecs.open(output_file_path, encoding='utf-8', mode='w') as f:
            f.write('\n'.join(group_failcase(no_of_files)))  


    print "\nGenerating Consolidated Report\n"

    failcase = {}
    message = {}

    for each_file in file_list:
        find_fail_case(each_file)
        print "Finished processing file " + each_file
    write_to_output(len(file_list), output_file_path)