import xml.etree.ElementTree as ET


# 69269337_1_FULL.xml
tree = ET.parse("../docs/v1/69269337_1_FULL.xml")
root = tree.getroot()

# iterate through the XML tree and get a list of unique tags
tags = []
for elem in root.iter():
    if elem.tag not in tags:
        tags.append(elem.tag)

# sort the list of tags
tags.sort()

for tag in tags:
    print(tag)
