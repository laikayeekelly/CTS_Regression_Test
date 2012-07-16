import os
<<<<<<< HEAD
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
=======
import operator
import itertools
from lxml import etree
>>>>>>> 882083efb866674f4a3493f2783d9d9a6d25dabd


def list_files(folder):
    file_list = []
    for r,d,f in os.walk(folder):
        for files in f:
            if files.endswith(".xml"):
                file_list.append(os.path.join(r,files))
    return file_list


def find_fail_case(file, failcase):
<<<<<<< HEAD
=======

    def buildkey(node):
        list = []
        while node.getparent().tag != 'TestResult':
            list.append(node.values()[0])
            node = node.getparent()
        list.append(node.values()[1])
        list.reverse()
        key = list[0]
        if len(list) >= 2:
            key = key + ',' 
            key = key + '.'.join(list[1:len(list)-1])
        key = key + ',' + list[len(list)-1]

        return key


>>>>>>> 882083efb866674f4a3493f2783d9d9a6d25dabd
    tree = etree.parse(file)
    find = etree.XPath("//Test[@result='fail']")
    for node in find(tree):
            key = buildkey(node)
            if failcase.has_key(key):
                failcase[key] += 1
            else:
                failcase[key] = 1
    return failcase

def write_to_output(output_file_name, failcase, no_of_files):

    def sort_fail_cases_into_desired_format(failcase, no_of_files):

        output_string = ""
        groups =[]

        sorted_failcase = sorted(failcase.items(), key=operator.itemgetter(1))
        for chance, testcases in itertools.groupby(sorted_failcase, lambda x:x[1]):
            groups.append(list(testcases))

        for i in range(len(groups)-1, -1, -1):
            groups[i].sort()
            for j in range(0, len(groups[i])):
                output_string = output_string + str(groups[i][j][1])+','+ str(no_of_files)+','
                output_string = output_string + groups[i][j][0]+'\n'

        return output_string


    output = sort_fail_cases_into_desired_format(failcase, no_of_files)
    with open(output_file_name, 'w') as output_file:
        output_file.write(output)

