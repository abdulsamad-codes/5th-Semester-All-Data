import os

json_size = os.path.getsize("students.json")
xml_size = os.path.getsize("students.xml")

print(f"The json file size is: {json_size}")
print(f"The xml file size is: {xml_size}")
