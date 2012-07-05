import os
import sys
failcase = {}
no_of_files = 0
from xml.etree.ElementTree import ElementTree
tree = ElementTree()

if len(sys.argv) != 3:
    print "usage : python ConsolidatedReport.py [reports folder] [output csv]"

elif os.path.exists(sys.argv[1]) == False:
    print "folder doesn't exists"

else :
    for r,d,f in os.walk(sys.argv[1]):
        for files in f:
            if files.endswith(".xml"):
                no_of_files += 1
                tree.parse(os.path.join(r,files))
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

    output = open(sys.argv[2], 'w')

    #for chances in range(no_of_files+1, 0, -1): (for reverse order)
    for chances in range(1, no_of_files+1):
        sorted_output = []
        if chances in failcase.values() :
            output.write(str(chances)+'\n')
            for each_case in failcase:
                if failcase[each_case] == chances :
                    sorted_output.append(each_case)

            sorted_output = sorted(sorted_output)
            for each_output in sorted_output:
                output.write(each_output + '\n')

    output.close()

    print "Finished!!!"
