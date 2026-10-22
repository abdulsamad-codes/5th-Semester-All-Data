import xml.etree.ElementTree as ET

def parse_students(file_name):
    with open(file_name, "r") as file:
        data = ET.parse(file)
    students = data.findall("student")
    result = []
    for student in students:
        name = student.find("name").text
        age = student.find("age").text
        gpa = student.find("gpa").text
        courses = []
        for course in student.find("courses").findall("course"):
            courses.append(course.text)
        student_dict = {"name": name, "age": age, "gpa": gpa, "courses": courses}
        print(student_dict)
        result.append(student_dict)
    return result

parse_students("students.xml")