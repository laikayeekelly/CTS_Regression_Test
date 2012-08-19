# CTS Regression Test Plan Generating System (Version 2)
# (Using the library BeautifulSoup)
# Prepared by Kelly Lai
from bs4 import BeautifulSoup

soup = BeautifulSoup(open("testResult.xml"))
fail_cases_list = soup.find_all(result="fail")

output = open('ctsRegression.xml', 'w')
output.write('<?xml version="1.0" encoding="UTF-8"?>\n')
output.write('<TestPlan version="1.0">\n')

prev_package_name = ''
for fail_cases in fail_cases_list:
    package = fail_cases.find_parent("testpackage")
    new_package_name = package['apppackagename']
    if new_package_name != prev_package_name:  
        prev_package_name = new_package_name
        output.write('  <Entry uri="' + str(new_package_name) + '"/>\n')
                
output.write('</TestPlan>\n')
output.close()
