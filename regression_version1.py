# CTS Regression Test Plan Generating System (Version 1)
# Prepared by Kelly Lai

with open('ctsRegression.xml', 'w') as output:
    with open('testResult.xml', 'r') as input:

        output.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        output.write('<TestPlan version="1.0">\n')

        package = ''
        inside_a_package = False  

        for line in input:
            if ('</TestResult>' in line):
                break

            if ('<TestPackage' in line):
                package = line.split('"')[3]
                inside_a_package = False                 
        
            if ('result="fail"' in line): 
                if (inside_a_package == False):
                    inside_a_package = True            
                    output.write('  <Entry uri="' + package + '"/>\n')
                
        output.write('</TestPlan>\n')

