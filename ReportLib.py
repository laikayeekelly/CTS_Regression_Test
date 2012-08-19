import os
import codecs
from re import sub
from operator import itemgetter
from itertools import groupby
from lxml import etree


def list_files(folder):
    """This function is used to list all the xml documents in the folder 
        requested by user and store all file names in to a list variable 
        called file_list"""

    file_list = []
    for r,d,f in os.walk(folder):
        for files in f:
            if files.endswith(".xml"):
                file_list.append(os.path.join(r,files))
    return file_list


def find_fail_case(file, failcase, message):
    """This function is used to find out all the nodes of the fail test case
        and update the variable failcase and message"""

    def buildkey(node):
        key_list = []
        while node.getparent().tag != 'TestResult':
            # get the name of the test case and test suite
            key_list.append(node.get("name"))
            node = node.getparent()
        key_list.append(node.get("appPackageName"))  # get the name of the test package
        key_list.reverse()
        key = key_list[0]
        if len(key_list) >= 2:
            key += '\t' + '.'.join(key_list[1:-1])
        # combine the test suite name together with the notation '.'
        key += '\t' + key_list[-1]

        return key

    # both failcase and message are variables of type dictionary
    # failcase: key -> name of fail cases  value -> number of failed chances
    # message : key -> name of fail cases
    #           value -> list of failure messages for the same failed test case

    # generate the key for updating the variables failcase and message

    tree = etree.parse(file)
    #find out all the nodes of the fail test case 
    find = etree.XPath("//Test[@result='fail']")
    for node in find(tree):
        key = buildkey(node)
        failedScene_node = node.find("FailedScene")
        if failedScene_node != None:
            fail_message = sub('\r\n|\r|\n', ' ', 
                               failedScene_node.get("message"))
            #replace the \r\n or \r in the failure messages with a white space
        else:
            fail_message = ' '
        if key in failcase.keys():
            failcase[key] += 1
        else:
            failcase[key] = 1
            message[key] = set()

        message[key].add(fail_message)

    return (failcase, message)


def write_to_output(file_list, failcase, message, output_file_path):
    """ Categorize the failed test cases into a dictionary according to their 
    fail chance and sort the test cases in an alphabetical way """


    def group_failcase(no_of_files, failcase, message):

        failcase_dict = {}

        for case, chance in failcase.iteritems():
            failcase_dict.setdefault(chance, [])
            failcase_dict[chance].append(case)

        # failcase_dict is a variable of type dictionary
        # failcase_dict : key -> failed chances   value : list of fail case name

        #Test cases will the most failed chances will be printed out first
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

    # Output the report as an csv document with file name defined by user
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
        #f.write("Test Failed" + '\t' + test_failed + '\n' )
        #f.write("Test Timed out" + '\t' + test_timed_out + '\n' )
        #f.write("Test Not Executed" + '\t' + test_not_execute + '\n' )
        f.write("Test Report"+'\n')
        f.write('\n'.join(file_list) + '\n')
        f.write("Chance"+'\t'+"Total"+'\t'+"Test Package"
                +'\t'+"Test Suite"+'\t'+"Test Case"+'\t'+"Error Message"+'\n')

        f.write('\n'.join(group_failcase(len(file_list), failcase, message)))  

