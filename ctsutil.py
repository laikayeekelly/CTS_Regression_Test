import os
import sys
import subprocess
import codecs
import time
from lxml import etree
from re import sub


result_folder_path = "../repository/results"
regression_plan_file_path = "../repository/plans/ctsRegression.xml"
tool_to_run_cts = "./cts-tradefed"
regression_plan_name = "ctsRegression"


def run_test(plan_name = 'CTS'):


    def get_report_created():

        file_list = [[os.path.join(r,files) for files in f 
                    if files.endswith(".xml")]
                    for r,d,f in os.walk(result_folder_path)]
        file_list = sum(file_list, [])
        file_list.sort(key=lambda x: os.path.getmtime(x))
        last_modified_file = file_list[-1]

        return last_modified_file


    prev_report = get_report_created()
    process = subprocess.Popen(tool_to_run_cts + " run cts --plan " + plan_name, 
                               shell = True, stdout=subprocess.PIPE)

    for line in iter(process.stdout.readline, ''):
        print line.rstrip()
        if "Time:" in line:
            subprocess.Popen.kill(process)
            break

    last_modified_file = get_report_created()

    tree = etree.parse(last_modified_file)
    test_not_execute = etree.XPath("//Summary")(tree)[0].get("notExecuted")
    if int(test_not_execute) != 0:
        complete_execute = False
    else:
        complete_execute = True

    return (last_modified_file, complete_execute) 

def check_adb_connection():

    no_of_device = 0
    check_list_devices = False 
    process = subprocess.Popen("adb devices", shell=True, stdout=subprocess.PIPE)
    for line in iter(process.stdout.readline, ''):
        print line.rstrip()
        if "List" in line:
            check_list_devices = True
        if check_list_devices == True:
            no_of_device += 1
    
    no_of_device = no_of_device - 2
    if no_of_device != 0 :
        print "Test cannot be completely executed"
    else:
        print "Test cannot be completely executed and device disconnected!"


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
                fail_message = sub('\r\n|\r|\n', ' ', 
                                   failedScene_node.get("message"))
            else:
                fail_message = ' '
            if key in failcase.keys():
                failcase[key] += 1
            else:
                failcase[key] = 1
                message[key] = set()

            message[key].add(fail_message)


    def write_to_output(file_list, output_file_path):


        def group_failcase(no_of_files):

            failcase_dict = {}

            for case, chance in failcase.iteritems():
                failcase_dict.setdefault(chance, [])
                failcase_dict[chance].append(case)

            chance_list = reversed(sorted(failcase_dict.keys()))

            output_list = []
            for chance in chance_list:
                for case in sorted(failcase_dict[chance]):
                    output_list.append(str(chance)+'\t'+str(no_of_files)+'\t'+ 
                                       case +'\t'+ '\t'.join(message[case]))

            return output_list


        tree = etree.parse(file_list[0])
        build_info = etree.XPath("//BuildInfo")(tree)[0]
        build_model = build_info.get("build_model")
        build_name = build_info.get("buildName")
        build_brand = build_info.get("build_brand")
        build_manufacturer = build_info.get("build_manufacturer")
        device_id = build_info.get("deviceID")
        firmware_version = build_info.get("buildVersion")
        firmware_build = build_info.get("buildID")
        build_fingerprint = build_info.get("build_fingerprint")
        CTS_version = etree.XPath("//Cts")(tree)[0].get("version")
        result_info = etree.XPath("//Summary")(tree)[0]
        test_failed = result_info.get("failed")
        test_timed_out = result_info.get("timeout")
        test_not_execute = result_info.get("notExecuted")


        with codecs.open(output_file_path, encoding='utf-8', mode='w') as f:

            f.write("Build Model" + '\t' + build_model + '\n')
            f.write("Build Name" + '\t' + build_name + '\n' )
            f.write("Build Brand" + '\t' + build_brand + '\n' )
            f.write("Build Manufacturer" + '\t' + build_manufacturer + '\n' )
            f.write("Device ID" + '\t' + device_id + '\n' )
            f.write("Firmware Version" + '\t' + firmware_version + '\n' )
            f.write("Firmware Build Number" + '\t' + firmware_build + '\n' )
            f.write("Build Fingerprint" + '\t' + build_fingerprint + '\n' )
            f.write("CTS Version" + '\t' + CTS_version + '\n' )
            f.write("Test Failed" + '\t' + test_failed + '\n' )
            f.write("Test Timed out" + '\t' + test_timed_out + '\n' )
            f.write("Test Not Executed" + '\t' + test_not_execute + '\n' )
            f.write("Test Report"+'\n')
            f.write('\n'.join(file_list) + '\n')
            f.write("Chance"+'\t'+"Total"+'\t'+"Test Package"
                    +'\t'+"Test Suite"+'\t'+"Test Case"+'\t'+"Error Message"+'\n')

            f.write('\n'.join(group_failcase(len(file_list))))  


    print "\nGenerating Consolidated Report\n"

    failcase = {}
    message = {}

    for each_file in file_list:
        find_fail_case(each_file)
        print "Finished processing file " + each_file
    write_to_output(file_list, output_file_path)
