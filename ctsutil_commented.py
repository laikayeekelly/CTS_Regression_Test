import os
import sys
import subprocess
from lxml import etree
from re import sub

result_folder_path = "../repository/results" 
regression_plan_file_path = "../repository/plan/ctsRegression.xml"
tool_to_run_cts = "cts-tradefed"

def run_test(plan_name = 'CTS'): 
    #subprocess.call( [tool_to_run_cts])
    #subprocess.call( ["run", "cts", "--plan", plan_name])
    #subprocess.call( ["./helloworld"])
    print "finish running test"


def generate_regression_plan():

    #The following function is used to find the location of the CTS report created 
    # by the latest CTS done
    def get_latest_result():
        folder = result_folder_path
        last_modified_file = ""
        latest_modified_time = 0
        for r,d,f in os.walk(folder):
            for files in f:
                if files.endswith(".xml"):
                    filepath = os.path.join(r,files)
                    modified_time = os.stat(filepath).st_mtime
                    # get the file's latest modified time 
                    if modified_time > latest_modified_time:
                        last_modified_file = filepath
                        latest_modified_time = modified_time

        return last_modified_file


    report_file = get_latest_result()
    fail_found = False
    # fail_found is True if any failed test case is found in the CTS Report

    # The following is used to create a regression test plan based on the latest 
    # CTS done
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
    # fail_found is returned so that regression CTS test will not be done if no
    # failed test cases found


# The following function is used to generate the consolidated report 
def generate_consolidated_report(output_file_path, file_list):

    # The following function is used to find out all the nodes of the fail test
    # case and update the variable failcase and message
    def find_fail_case(file, failcase, message):

    # The following is the description of variables 'failcase' and 'message'
    # both 'failcase' and 'message' are variables of type dictionary
    # failcase: key -> name of fail cases  value -> number of failed chances
    # message : key -> name of fail cases
    #           value -> list of failure messages for the same failed test case



        # the following function is used generate the key for updating the 
        # variables failcase and message
        def buildkey(node):
            key_list = []
            while node.getparent().tag != 'TestResult':
                # get the name of the test case and test suite
                key_list.append(node.get("name"))
                node = node.getparent()
            key_list.append(node.get("appPackageName"))   # get the name of the test package
            key_list.reverse()
            key = key_list[0]
            if len(key_list) >= 2:
                key += '\t' + '.'.join(key_list[1:len(key_list)-1])
            # combine the test suite name together with the notation '.'
            key += '\t' + key_list[len(key_list)-1]

            return key


        tree = etree.parse(file)
        #find out all the nodes of the fail test case 
        find = etree.XPath("//Test[@result='fail']")
        for node in find(tree):
            key = buildkey(node)
            failedScene_node = node.find("FailedScene")
            if failedScene_node != None:
                fail_message = sub('\r\n|\r', ' ', failedScene_node.get("message").encode('ascii', 'ignore'))
                #replace the \r\n or \r in the failure messages with a white space
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


    def write_to_output(output_file_path, failcase, message, no_of_files):

        # The following function is used to categorize the failed test cases 
        # into a dictionary according to their fail chance
        # and sort the test cases in an alphabetical way
        def sort_fail_cases_into_desired_format(failcase, message, no_of_files):

            failcase_dict = {}

            for case, chance in failcase.iteritems():
                failcase_dict.setdefault(chance, [])
                failcase_dict[chance].append(case)

            # failcase_dict is a variable of type dictionary
            # failcase_dict : key -> failed chances   
            #                 value -> list of fail case name

            #Test cases will the most failed chances will be printed out first
            chance_list = reversed(failcase_dict.keys())

            # For every test cases, print it out in the desire format
            # Testcases with same failed chances will be put into the same list
            # And all these lists will be put into a list variable output_list
            # So, output_list is a variable of type list of lists
            # (List Comprehesion is being used below)

            output_list = [[str(chance)+'\t'+str(no_of_files)+'\t'+ case +'\t'+ \
                          '\t'.join(message[case])+'\n' for case in \
                          sorted(failcase_dict[chance])] for chance in chance_list]

            # (python built-in function map cannot be used here due the limitation of
            # the input arguments)

            return output_list


        output_list = sort_fail_cases_into_desired_format(failcase, message, no_of_files)
        with open(output_file_path, 'w') as output_file:
            for chance in output_list:
                for case in chance:
                    output_file.write(case)


    print "\nGenerating Consolidated Report\n"

    failcase = {}
    message = {}

    for each_file in file_list:
        failcase, message = find_fail_case(each_file, failcase, message)
        print "Finished processing file " + each_file
    write_to_output(output_file_path, failcase, message, len(file_list))

