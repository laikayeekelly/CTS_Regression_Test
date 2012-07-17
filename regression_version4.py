# CTS Regression Test Plan Generating System
# Prepared by Kelly Lai
from lxml import etree

with open('ctsRegression.xml', 'w') as output:

    prev_package_name = ''

    output.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    output.write('<TestPlan version="1.0">\n')

    tree = etree.parse("testResult.xml")
    find = etree.XPath("//Test[@result='fail']")
    for node in find(tree):
        while node.getparent().tag != 'TestResult':
            node = node.getparent()
        new_package_name = node.values()[1]
        if new_package_name != prev_package_name: 
            prev_package_name = new_package_name
            xml_text = '  <Entry uri="' + str(new_package_name) + '"/>\n'
            output.write(xml_text)

    output.write('</TestPlan>\n')

