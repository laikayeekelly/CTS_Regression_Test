import os
from lxml import etree

def buildkey(node):
    list = []
    while node.getparent().tag != 'TestResult':
        list.append(node.values()[0])
        node = node.getparent()
    list.append(node.values()[1])

    key = list.pop()
    no_of_elements = len(list)
    for i in range(0, no_of_elements):
        if ((i == 0) or (i == no_of_elements-1)):
            key = key + ',' + str(list.pop())
        else:
            key = key + '.' + str(list.pop())
    return key


def list_files(folder):
    file_list = []
    for r,d,f in os.walk(folder):
        for files in f:
            if files.endswith(".xml"):
                file_list.append(os.path.join(r,files))
    return file_list


def find_fail_case(file, failcase):
    tree = etree.parse(file)
    find = etree.XPath("//Test[@result='fail']")
    for node in find(tree):
            key = buildkey(node)
            if failcase.has_key(key):
                failcase[key] += 1
            else:
                failcase[key] = 1
    return failcase


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


def write_to_output(output_file_name, failcase, no_of_files):
    output = sort_fail_cases_into_desired_format(failcase, no_of_files)
    with open(output_file_name, 'w') as output_file:
        output_file.write(output)

