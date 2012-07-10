import os
from xml.dom.minidom import parse


def buildkey(node):
    list = []
    while node.parentNode.nodeName != 'TestResult':
        list.append(node.getAttribute("name")) 
        node = node.parentNode
    list.append(node.getAttribute("appPackageName"))

    # reverse the order of elements in the list using pop()
    key = list.pop() 
    no_of_elements = len(list)
    for i in range(0, no_of_elements):
        if ((i == 0) or (i == no_of_elements-1)):
            key = key + ',' + str(list.pop())
        else:
            key = key + '.' + str(list.pop())
    return key


# List all the xml documents in the folder requested by user
# Store all file names in to a list claled file_list
def list_files(folder):
    file_list = []
    for r,d,f in os.walk(folder):
        for files in f:
            if files.endswith(".xml"):
                file_list.append(os.path.join(r,files))
    return file_list


# Find out all the nodes of the fail test case 
# and update the dictionary for storing the information of the failed test case
def find_fail_case(file, failcase):
    dom = parse(file) 
    for node in dom.getElementsByTagName('Test'):
        if node.getAttribute("result") == 'fail':
            # the key should consist of the test suite and test package name
            key = buildkey(node)
            if failcase.has_key(key):   
                failcase[key] += 1    
            else:
                failcase[key] = 1
    return failcase


# Categorize the failed test cases into specific list according to their chances
# of being failed and sort each list in an alphabetical way
def sort_fail_cases_into_desired_format(failcase, no_of_files):
    output_string = ""
    list = []
    for chances in range(0, no_of_files+1):
        inner_list = []
        list.append(inner_list)

    for each_case in failcase:
        list[failcase[each_case]].append(each_case)

    for i in range(no_of_files, 0, -1):
        list[i].sort()
        if list[i]:
            for each_element in list[i]:
                output_string = output_string+str(i)+','+str(no_of_files)+','
                output_string = output_string+each_element+'\n'

    return output_string

# Output the report as an csv document
def write_to_output(output_file_name, failcase, no_of_files):
    output = sort_fail_cases_into_desired_format(failcase, no_of_files)
    with open(output_file_name, 'w') as output_file:
        output_file.write(output)

