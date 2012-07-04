# CTS Regression Test Plan Generating System (Version 2)
# (Using the library Element Tree)
# Prepared by Kelly Lai
from xml.etree.ElementTree import ElementTree
tree = ElementTree()
tree.parse("testResult.xml")
package = tree.findall("TestPackage")

output = open('ctsRegression.xml', 'w')
output.write('<?xml version="1.0" encoding="UTF-8"?>\n')
output.write('<TestPlan version="1.0">\n')

for each_package in package:
	testcases = list(each_package.iter("Test"))
	for each_testcases in testcases:
		if(each_testcases.attrib["result"]=='fail'):
			output.write('  <Entry uri="' + each_package.attrib["appPackageName"] + '"/>\n')
			break
               
output.write('</TestPlan>\n')
output.close()