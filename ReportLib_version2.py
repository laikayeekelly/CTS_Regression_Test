import os
from xml.etree.ElementTree import ElementTree
from xml.dom.minidom import parse
def find_parent_list(child):
    parentList = []
    parent = child.parentNode
    parentList.append(parent)
    while parent.nodeName != 'TestPackage':
        parent = parent.parentNode
        parentList.append(parent)    

    return parentList

def combine_elements(list):
    result = ""
    if len(list) != 0 :
        result = list[len(list)-1].getAttribute("name")
        for i in range(len(list)-2, -1, -1):
            result = result + '.' + str(list[i].getAttribute("name"))
    return result 

def list_files(folder):
    file_list = []
    for r,d,f in os.walk(folder):
        for files in f:
            if files.endswith(".xml"):
                file_list.append(os.path.join(r,files))
    return file_list

def find_fail_case(file, failcase): 
    
    dom = parse(file) 
    for node in dom.getElementsByTagName('Test'):
        if node.getAttribute("result") == 'fail':
            case_name = node.getAttribute("name")  
            parent_list = find_parent_list(node)
            suite_name = combine_elements(parent_list[0:len(parent_list)-1])
            package_name = parent_list[len(parent_list)-1].getAttribute("appPackageName")
            if failcase.has_key(package_name+','+suite_name+','+case_name):
                failcase[package_name+','+suite_name+','+case_name] += 1
            else:
                failcase[package_name+','+suite_name+','+case_name] = 1

    return failcase

def write_to_output(output_file, failcase, no_of_files):
    output = open(output_file, 'w')

    for chances in range(no_of_files+1, 0, -1):
        sorted_output = []
        if chances in failcase.values() :
            for each_case in failcase:
                if failcase[each_case] == chances :
                    sorted_output.append(each_case)

            sorted_output = sorted(sorted_output)
            for each_output in sorted_output:
                output.write(str(chances)+','+str(no_of_files)+',')
                output.write(each_output+'\n')
    output.close()


def print_list(list):
    outputList = []
    for i in range(0, len(list)):
        outputList.append(list[i].getAttribute("name"))
    print outputList