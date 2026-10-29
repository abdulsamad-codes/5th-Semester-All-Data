import json


def save_students(students:list, filename:str)-> None:
    try:
        with open(filename, "w") as file:
            json.dump(students, file, indent=4)
    except Exception as e:
        print("foudn exception", e)

students = [
    {
        "name": "Alice Johnson",
        "age": 20,
        "courses": ["Mathematics", "Computer Science", "Physics"],
        "gpa": 3.8
    },
    {
        "name": "Bob Smith",
        "age": 22,
        "courses": ["Biology", "Chemistry", "English Literature"],
        "gpa": 3.4
    },
    {
        "name": "Charlie Brown",
        "age": 19,
        "courses": ["History", "Political Science", "Economics"],
        "gpa": 3.1
    },
    {
        "name": "Diana Prince",
        "age": 21,
        "courses": ["Computer Science", "Data Structures", "Discrete Math"],
        "gpa": 3.9
    },
    {
        "name": "Evan Wright",
        "age": 23,
        "courses": ["Psychology", "Sociology", "Statistics"],
        "gpa": 3.5
    }
]

save_students(students, "students.json")