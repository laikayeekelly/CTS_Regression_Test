package_list = []
package_chances = []

from xml.etree.ElementTree import ElementTree
tree = ElementTree()

input_var = raw_input("Enter number of files: ")
no_of_files = int(input_var)
print "For the location of every file, type the location and then press Enter"
for i in range(0, no_of_files):
    input_var = raw_input("Enter location: ")
    input = open(input_var, 'r')

    tree.parse(input)
    package = tree.findall("TestPackage")

    for i in package:
        testcases = list(i.iter("Test"))
        for j in testcases:
            if(j.attrib["result"]=='fail'):
                if i.attrib["appPackageName"] not in package_list:
                    package_list.append(i.attrib["appPackageName"])
                    package_chances.append(1)
                else:
                    index = package_list.index(i.attrib["appPackageName"])
                    package_chances[index] = package_chances[index] + 1
                break

for chances in range(1, no_of_files+1):
	if(chances in package_chances):
		print('chances = ' + str(chances))
		for i in [i for i,x in enumerate(package_chances) if x == chances]:
			print(package_list[i])


print package_list		
print package_chances   





