# CTS Regression Test Plan Generating System
# Prepared by Kelly Lai

input = open('testResult.xml', 'r')
output = open('ctsRegression.xml', 'w')
output.write('<?xml version="1.0" encoding="UTF-8"?>\n')
output.write('<TestPlan version="1.0">\n')

line = ''
package = ''
xml_text = ''
start_a_new_package = True  

while not('</TestResult>' in line):
    if ('<TestPackage' in line):
        package = line.split('"')[3]
        start_a_new_package = True                 
        
    if ('result="fail"' in line): 
        if (start_a_new_package == True):
            start_a_new_package = False            
            xml_text = '  <Entry uri="' + package + '"/>\n'
            output.write(xml_text)
                
    line = input.readline()

output.write('</TestPlan>\n')
input.close()
output.close()
