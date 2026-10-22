import json


def save_students(students, file_name):
    with open(file_name, "w") as file:
        json.dump(students, file, indent=2)
    print("\nStudents data saved to the file successfully")

def load_students(file_name):
    with open(file_name, "r") as file:
        students = json.load(file)

    for student in students:
        print(student)

def filter_by_gpa(students, min_gpa):
    filtered_list = []
    for student in students:
        if student["gpa"] >= min_gpa:
            filtered_list.append(student)

    print(f"Students with the gpa higher or equal to {min_gpa} are: ")
    for student in filtered_list:
        print(student)
    return filtered_list


def save_filtered(filtered_list, file_name):
    save_students(filtered_list, file_name)

students = [
    {
        "name": "Alice Smith",
        "age": 20,
        "courses": ["Introduction to Python", "Data Structures", "Calculus I"],
        "gpa": 3.8
    },
    {
        "name": "Bob Jones",
        "age": 22,
        "courses": ["Database Systems", "Web Development"],
        "gpa": 3.2
    },
    {
        "name": "Charlie Brown",
        "age": 19,
        "courses": ["Discrete Mathematics", "Linear Algebra", "Introduction to Python"],
        "gpa": 3.9
    },
    {
        "name": "Diana Prince",
        "age": 21,
        "courses": ["Artificial Intelligence", "Computer Networks", "Operating Systems"],
        "gpa": 3.5
    },
    {
        "name": "Evan Wright",
        "age": 23,
        "courses": ["Software Engineering", "Human-Computer Interaction"],
        "gpa": 2.9
    }
]


save_students(students, "students.json")
print("\n")
load_students("students.json")
print("\n")
filtered_list = filter_by_gpa(students, 3.5)
save_filtered(filtered_list, "top_students.json")
