import json
import os
import xml.etree.ElementTree as ET
import yaml


def save_json(students, filename):
    with open(filename, "w") as file:
        json.dump(students, file, indent=2)


def save_xml(students, filename):
    root = ET.Element("students")
    for student in students:
        student_element = ET.SubElement(root, "student")
        ET.SubElement(student_element, "name").text = student["name"]
        ET.SubElement(student_element, "age").text = str(student["age"])
        ET.SubElement(student_element, "gpa").text = str(student["gpa"])

        courses = ET.SubElement(student_element, "courses")
        for course in student["courses"]:
            ET.SubElement(courses, "course").text = course

    ET.indent(root, space="  ")
    tree = ET.ElementTree(root)
    tree.write(filename)


def save_yaml(students, filename):
    with open(filename, "w") as file:
        yaml.safe_dump(students, file, sort_keys=False)


def sum_gpa_row_based(students):
    sum = 0
    for student in students: 
        sum += student["gpa"]
    return sum


def sum_gpa_columnar(columns):
    return sum(columns["gpa"])


with open("students.json", "r") as file:
    students = json.load(file)

save_json(students, "students.json")
save_xml(students, "students.xml")
save_yaml(students, "students.yaml")

for filename in ["students.json", "students.xml", "students.yaml"]:
    size = os.path.getsize(filename)
    print(f"{filename} size: {size} bytes")

columns = {
    "name": [],
    "age": [],
    "courses": [],
    "gpa": []
}

for student in students:
    columns["name"].append(student["name"])
    columns["age"].append(student["age"])
    columns["courses"].append(student["courses"])
    columns["gpa"].append(student["gpa"])

row_sum = sum_gpa_row_based(students)
columnar_sum = sum_gpa_columnar(columns)

print(f"\nRow based GPA sum: {row_sum}")
print(f"Columnar GPA sum: {columnar_sum}")
print(f"Results match: {row_sum == columnar_sum}")
