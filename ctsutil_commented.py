import os
import sys
import subprocess
from lxml import etree
from re import sub

result_folder_path = "../repository/results"
regression_plan_file_path = "../repository/plan/ctsRegression.xml"
tool_to_run_cts = "./cts-tradefed"

def run_test(plan_name = 'CTS'):
    """ Run the CTS or CTS regression test
        Return the path of the test result report """

    #subprocess.call( [tool_to_run_cts, "run", "cts", "--plan", plan_name])
    #subprocess.call( ["./helloworld"])
    print "finish running test"

    file_list = [[os.path.join(r,files) for files in f if files.endswith(".xml")]
                for r,d,f in os.walk(result_folder_path)]
    # Get all the test result report and store it in the list file_list
    file_list = sum(file_list, [])
    # Convert the type of file_list from list of lists to list
    file_list.sort(key=lambda x: os.path.getmtime(x))
    # Sort file_list according to the modidication date of file
    last_modified_file = file_list[len(file_list)-1]

    return last_modified_file

def cts_report_filter(report_file):
    """ Create a regression test plan based on the latest test done
        Return the test plan name """

    test_plan = ''

    with open(regression_plan_file_path, 'w') as output:
        prev_package_name = ''

        output.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        output.write('<TestPlan version="1.0">\n')

        tree = etree.parse(report_file)
        find = etree.XPath("//Test[@result='fail']")
        for node in find(tree):
            test_plan = "ctsRegression"
            while node.getparent().tag != 'TestResult':
                node = node.getparent()
            new_package_name = node.get("appPackageName")
            if new_package_name != prev_package_name: 
                prev_package_name = new_package_name
                output.write('  <Entry uri="' + new_package_name + '"/>\n')

        output.write('</TestPlan>\n')


    return test_plan


def generate_consolidated_report(output_file_path, file_list):

    """ Generate the consolidated report of the result of the CTS tests """

    def find_fail_case(file, failcase, message):

        """
        Find out all the fail test cases and the corresponding error messages
        and update the variable failcase and message

        failcase and message are variables of type dictionary
        failcase: key -> name of fail cases  
                  value -> number of failed chances
        message : key -> name of fail cases
                  value -> list of failure messages for the same failed 
                           test case
        """

        def buildkey(node):
            """generate the key for updating variables failcase and message """

            key_list = []
            while node.getparent().tag != 'TestResult':
                # get the name of the test case and test suite
                key_list.append(node.get("name"))
                node = node.getparent()
            key_list.append(node.get("appPackageName")) # get the name of the test package
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
            else:
                failcase[key] = 1
                message[key] = set()

            message[key].add(fail_message)

        return (failcase, message)


    def write_to_output(output_file_path, failcase, message, no_of_files):
        """Write the report into the csv file defined by user"""

        def group_failcase(failcase, message, no_of_files):

            """ 
            Categorize the failed test cases  into a dictionary according 
            to their fail chance and sort the test cases in an 
            alphabetical way  

            failcase_dict is a variable of type dictionary
            failcase_dict : key -> failed chances   
                            value -> list of fail case name
            """

            failcase_dict = {}

            for case, chance in failcase.iteritems():
                failcase_dict.setdefault(chance, [])
                failcase_dict[chance].append(case)

            #Test cases will the most failed chances will be printed out first
            chance_list = reversed(failcase_dict.keys())

            # For every test cases, print it out in the desire format
            # Testcases with same failed chances will be put into the same list
            # And all these lists will be put into a list variable output_list
            # So, output_list is a variable of type list of lists
            # (List Comprehesion is being used below)

            output_list = []
            for chance in chance_list:
                for case in sorted(failcase_dict[chance]):
                    output_list.append(str(chance)+'\t'+str(no_of_files)+'\t'+ 
                                       case +'\t'+ '\t'.join(message[case])+'\n')

            return output_list

        with open(output_file_path, 'w') as output_file:
            for output_list_item in group_failcase(failcase, message, no_of_files):
                output_file.write(output_list_item)


    print "\nGenerating Consolidated Report\n"

    failcase = {}
    message = {}

    for each_file in file_list:
        failcase, message = find_fail_case(each_file, failcase, message)
        print "Finished processing file " + each_file
    write_to_output(output_file_path, failcase, message, len(file_list))

