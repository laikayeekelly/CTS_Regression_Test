import os
from operator import itemgetter
from itertools import groupby
from lxml import etree


def list_files(folder):
    file_list = []
    for r,d,f in os.walk(folder):
        for files in f:
            if files.endswith(".xml"):
                file_list.append(os.path.join(r,files))
    return file_list


def find_fail_case(file, input_list):
    
    failcase = input_list[0]
    message = input_list[1]

    def replace_all(text):
        format_dict = {',':'\t', '\r\n':' ', '\r':' ', '\n':' '}
        for i, j in format_dict.iteritems():
            text = text.replace(i, j)
        return text

    def buildkey(node):
        key_list = []
        while node.getparent().tag != 'TestResult':
            key_list.append(node.values()[0])
            node = node.getparent()
        key_list.append(node.values()[1])
        key_list.reverse()
        key = key_list[0]
        if len(key_list) >= 2:
            key += ',' + '.'.join(key_list[1:len(key_list)-1])
        key = key + ',' + key_list[len(key_list)-1]

        return key


    tree = etree.parse(file)
    find = etree.XPath("//Test[@result='fail']")
    for node in find(tree):
        key = buildkey(node)
        fail_message = replace_all(node.find("FailedScene").values()[0])
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
    def sort_fail_cases_into_desired_format(input_list, no_of_files):

        output_string = ""
        failcase = input_list[0]
        message = input_list[1]
        failcase_dict = {}

        for case, chance in failcase.iteritems():
            failcase_dict.setdefault(chance, [])
            failcase_dict[chance].append(case)

        chance_list = failcase_dict.keys()
        for i in range(len(chance_list)-1, -1, -1):
            case_list = sorted(failcase_dict[chance_list[i]])
            for case in case_list:
                output_string += str(chance_list[i])+','+ str(no_of_files)+','
                output_string += case + ',' + ','.join(message[case]) +'\n'

        return output_string


    output = sort_fail_cases_into_desired_format(input_list, no_of_files)
    with open(output_file_name, 'w') as output_file:
        output_file.write(output)

