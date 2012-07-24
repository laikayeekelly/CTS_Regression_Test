import os
from re import sub
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


def find_fail_case(file, failcase, message):

    def buildkey(node):
        key_list = []
        while node.getparent().tag != 'TestResult':
            key_list.append(node.get("name"))
            node = node.getparent()
        key_list.append(node.get("appPackageName"))
        key_list.reverse()
        key = key_list[0]
        if len(key_list) >= 2:
            key += '\t' + '.'.join(key_list[1:len(key_list)-1])
        key = key + '\t' + key_list[len(key_list)-1]

        return key


    tree = etree.parse(file)
    find = etree.XPath("//Test[@result='fail']")
    for node in find(tree):
        key = buildkey(node)
        if node.find("FailedScene") != None:
            fail_message = sub('\r\n|\r', ' ', node.find("FailedScene").get("message").encode('ascii', 'ignore'))
        else:
            fail_message = ' '
        if failcase.has_key(key):
            failcase[key] += 1
            if fail_message not in message[key]:
                message[key].append(fail_message)
        else:
            failcase[key] = 1
            message[key] = [fail_message]

    return (failcase, message)


def write_to_output(output_file_name, failcase, message, no_of_files):

    def sort_fail_cases_into_desired_format(failcase, message, no_of_files):

        failcase_dict = {}

        for case, chance in failcase.iteritems():
            failcase_dict.setdefault(chance, [])
            failcase_dict[chance].append(case)

        chance_list = reversed(failcase_dict.keys())
        output_list = [[str(chance)+'\t'+str(no_of_files)+'\t'+ case +'\t'+ \
        '\t'.join(message[case])+'\n' for case in sorted(failcase_dict[chance])\
        ] for chance in chance_list]
        return output_list


    output_list = sort_fail_cases_into_desired_format(failcase, message, no_of_files)
    with open(output_file_name, 'w') as output_file:
        for chance in output_list:
            for case in chance:
                output_file.write(case)

