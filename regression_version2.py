# CTS Regression Test Plan Generating System
# Prepared by Kelly Lai
from bs4 import BeautifulSoup

prev_package_name = ''
package_list = []

output = open('ctsRegression.xml', 'w')
output.write('<?xml version="1.0" encoding="UTF-8"?>\n')
output.write('<TestPlan version="1.0">\n')

soup = BeautifulSoup(open("testResult.xml"))

fail_cases_list = soup.find_all(result="fail")
for fail_cases in fail_cases_list:
    package = fail_cases.find_parent("testpackage")
    new_package_name = package['apppackagename']
    if new_package_name != prev_package_name:  
        prev_package_name = new_package_name
        xml_text = '  <Entry uri="' + str(new_package_name) + '"/>\n'
        output.write(xml_text)
                
output.write('</TestPlan>\n')
output.close()
