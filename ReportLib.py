import os
from xml.etree.ElementTree import ElementTree

def list_files(folder):
    file_list = []
    for r,d,f in os.walk(folder):
        for files in f:
            if files.endswith(".xml"):
                file_list.append(os.path.join(r,files))
    return file_list

def find_fail_case(file, failcase):    
    tree = ElementTree()
    tree.parse(file)
    package = tree.findall("TestPackage")
    for each_package in package:
        package_name = each_package.attrib["appPackageName"]
        testcases = list(each_package.iter("Test"))
        for each_testcase in testcases:
            if(each_testcase.attrib["result"]=='fail'):
                case_name = each_testcase.attrib["name"]
                if failcase.has_key(package_name+','+case_name):
                    failcase[package_name+','+case_name] += 1
                else:
                    failcase[package_name+','+case_name] = 1

    return failcase

def write_to_output(output_file, failcase, no_of_files):
    output = open(output_file, 'w')

    for chances in range(no_of_files+1, 0, -1): 
        sorted_output = []
        if chances in failcase.values() :
            #output.write(str(chances)+'\n')
            for each_case in failcase:
                if failcase[each_case] == chances :
                    sorted_output.append(each_case)

            sorted_output = sorted(sorted_output)
            for each_output in sorted_output:
                output.write(str(chances)+','+str(no_of_files)+','+each_output+'\n')

    output.close()