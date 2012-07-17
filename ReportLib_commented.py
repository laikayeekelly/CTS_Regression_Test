import os
from re import sub
from operator import itemgetter
from itertools import groupby
from lxml import etree

# This function is used to list all the xml documents in the folder requested by 
# user and store all file names in to a list variable called file_list
def list_files(folder):
    file_list = []
    for r,d,f in os.walk(folder):
        for files in f:
            if files.endswith(".xml"):
                file_list.append(os.path.join(r,files))
    return file_list


# This function is used to find out all the nodes of the fail test case 
# and update the variable failcase and message
def find_fail_case(file, input_list):

    failcase = input_list[0]
    message = input_list[1]

    # both failcase and message are variables of type dictionary
    # failcase: key -> name of fail cases  value -> number of failed chances
    # message : key -> name of fail cases
    #           value -> list of failure messages for the same failed test case

    # generate the key for updating the variables failcase and message
    def buildkey(node):
        key_list = []
        while node.getparent().tag != 'TestResult':
            # get the name of the test case and test suite
            key_list.append(node.values()[0])  
            node = node.getparent()
        key_list.append(node.values()[1])   # get the name of the test package
        key_list.reverse()
        key = key_list[0]
        if len(key_list) >= 2:
            key += '\t' + '.'.join(key_list[1:len(key_list)-1])
        # combine the test suite name together with the notation '.'
        key = key + '\t' + key_list[len(key_list)-1]

        return key


    tree = etree.parse(file)
    #find out all the nodes of the fail test case 
    find = etree.XPath("//Test[@result='fail']")
    for node in find(tree):
        key = buildkey(node)
        fail_message = sub('\r\n|\r', ' ', node.find("FailedScene").values()[0])
        #replace the \r\n or \r in the failure messages with a white space
        if failcase.has_key(key):
            failcase[key] += 1
            if fail_message not in message[key]:
                message[key].append(fail_message)
        else:
            failcase[key] = 1
            message[key] = [fail_message]

    output_list = [failcase, message]

    return output_list

def write_to_output(output_file_name, input_list, no_of_files):

    # Categorize the failed test cases into a dictionary according to their 
    # fail chance and sort the test cases in an alphabetical way
    def sort_fail_cases_into_desired_format(input_list, no_of_files):

        failcase = input_list[0]
        message = input_list[1]
        failcase_dict = {}

        for case, chance in failcase.iteritems():
            failcase_dict.setdefault(chance, [])
            failcase_dict[chance].append(case)

        # failcase_dict is a variable of type dictionary
        # failcase_dict : key -> failed chances   value : list of fail case name

        #Test cases will the most failed chances will be printed out first
        chance_list = reversed(failcase_dict.keys())

        # For every test cases, print it out in the desire format
        # Testcases with same failed chances will be put into the same list
        # And all these lists will be put into a list variable output_list
        # So, output_list is a variable of type list of lists
        output_list = [[str(chance)+'\t'+str(no_of_files)+'\t'+ case +'\t'+ \
        '\t'.join(message[case])+'\n' for case in sorted(failcase_dict[chance])\
        ] for chance in chance_list]

        return output_list

    # Output the report as an csv document
    output_list = sort_fail_cases_into_desired_format(input_list, no_of_files)
    with open(output_file_name, 'w') as output_file:
        for chance in output_list:
            for case in chance:
                output_file.write(case)

