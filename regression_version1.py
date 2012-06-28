# CTS Regression Test Plan Generating System
# Prepared by Kelly Lai

input = open('testResult.xml', 'r')
output = open('ctsRegression.xml', 'w')
output.write('<?xml version="1.0" encoding="UTF-8"?>\n')
output.write('<TestPlan version="1.0">\n')

line = ''
package = ''
xml_text = ''
package_list = []
start_a_new_package = 1
no_of_failed_test_cases = 0       

while line.find('</TestResult>') is -1 :
    if line.find('<TestPackage') != -1:
        tmp = line.split('"')  
        package = tmp[3]                         
        start_a_new_package = 1                  
        
    if (line.find('result="fail"') != -1): 
        no_of_failed_test_cases = no_of_failed_test_cases + 1
        if (start_a_new_package == 1):
            start_a_new_package = 0
            package_list.append(package)              
            xml_text = '  <Entry uri="' + package + '"/>\n'
            output.write(xml_text)
                
    line = input.readline()

if (no_of_failed_test_cases >= 1000) : 
    print 'Number of failed test cases exceeds 1000 '
    print 'regression testing is not suggested'

output.write('</TestPlan>\n')
input.close()
output.close()
