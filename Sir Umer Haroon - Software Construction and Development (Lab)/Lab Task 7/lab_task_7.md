# Lab Task 7

---

## Task 1: Working with JSON

### Background

JSON is a text format for representing structured data as key-value pairs and lists. Python has a built-in json module that converts Python dictionaries and lists to JSON strings and back. The function json.dumps converts a Python object to a JSON string. The function json.loads converts a JSON string back to a Python object. The functions json.dump and json.load do the same but work with files.

### Scenario

You are building a small student records system. Each student has a name, age, list of courses, and GPA. You will store this data in JSON, read it back, filter it, and write the filtered result to a new file.

### What to Do

#### Part A: Serialize a Python Dictionary to JSON

Create a file called task1_json.py. Inside it, create a list of at least five student dictionaries. Each dictionary should have keys name, age, courses, and gpa. The courses key should hold a list of course names.

Write a function called save_students that takes a list of students and a filename and writes the list to a JSON file using json.dump with an indent of 2.

Write a function called load_students that takes a filename and returns the list of students using json.load.

Call save_students to write your list to a file called students.json. Then call load_students to read it back and print each student.

#### Part B: Filter and Write

Write a function called filter_by_gpa that takes a list of students and a minimum GPA and returns a new list containing only the students whose GPA is greater than or equal to the minimum.

Write a function called save_filtered that takes a list of students and a filename and writes them to a JSON file, reusing save_students.

Call filter_by_gpa with a minimum of 3.5, then call save_filtered to write the result to top_students.json. Print the contents of the filtered list.

#### Part C: Pretty Print and Inspect

Open students.json in a text editor and observe the structure. Notice the curly braces, square brackets, double quotes, and the indentation produced by the indent argument. Then open top_students.json and compare. Write a short note in your report explaining what the indent argument did and why it is useful.

### Expected Output

```text
Student: Ali Khan, Age: 22, GPA: 3.75, Courses: ['SCD', 'DB']
Student: Sara Ahmed, Age: 21, GPA: 3.90, Courses: ['SCD', 'OS']
Student: John Doe, Age: 23, GPA: 3.60, Courses: ['DS', 'DB']
Student: Ayesha Malik, Age: 20, GPA: 3.40, Courses: ['SCD']
Student: Bilal Raza, Age: 24, GPA: 3.85, Courses: ['Networks', 'DB']

Students with GPA >= 3.5:
Student: Ali Khan, Age: 22, GPA: 3.75
Student: Sara Ahmed, Age: 21, GPA: 3.90
Student: John Doe, Age: 23, GPA: 3.60
Student: Bilal Raza, Age: 24, GPA: 3.85
```

The file students.json should look like this.

```json
[
  {
    "name": "Ali Khan",
    "age": 22,
    "courses": ["SCD", "DB"],
    "gpa": 3.75
  },
  {
    "name": "Sara Ahmed",
    "age": 21,
    "courses": ["SCD", "OS"],
    "gpa": 3.9
  }
]
```

**\*seperate submission files for both tasks**

---

## Task 2: Working with XML

### Background

XML represents data using tags. An element has an opening tag and a closing tag, and may contain text, attributes, or nested elements. Python's xml.etree.ElementTree module parses XML strings and files and lets you navigate the tree of elements. The function ET.fromstring parses a string. The function ET.parse parses a file. The method findall finds all matching child elements. The method find finds the first match. The method get reads an attribute. The attribute .text reads the text content of an element.

### Scenario

You are given the same student data as Task 1, but this time it is in XML. You will parse the XML, extract the data, and convert it to a list of dictionaries so that it can be processed like any other Python data.

### What to Do

#### Part A: Create the XML File

Create a file called students.xml by hand. The root element should be `<students>`. Inside it, create at least five `<student>` elements. Each student element should have an id attribute and child elements for name, age, gpa, and courses. The courses element should contain multiple `<course>` child elements.

#### Part B: Parse the XML

Create a file called task2_xml.py. Write a function called parse_students that takes a filename and returns a list of dictionaries. Each dictionary should have the same keys as in Task 1, name, age, courses, and gpa. Use ET.parse to load the file, findall to find all student elements, find to find each field, and .text to read the text.

Print each student dictionary as you parse it.

#### Part C: Compare JSON and XML

Write a short note in your report answering these questions. Which file was easier to write by hand, students.json or students.xml. Which file was larger in bytes. Which one was easier to read. Which one required more code to parse in Python.

Use the os.path.getsize function or the file size shown in your file explorer to compare file sizes.

### Expected Output

```text
{'name': 'Ali Khan', 'age': '22', 'gpa': '3.75', 'courses': ['SCD', 'DB']}
{'name': 'Sara Ahmed', 'age': '21', 'gpa': '3.90', 'courses': ['SCD', 'OS']}
{'name': 'John Doe', 'age': '23', 'gpa': '3.60', 'courses': ['DS', 'DB']}
{'name': 'Ayesha Malik', 'age': '20', 'gpa': '3.40', 'courses': ['SCD']}
{'name': 'Bilal Raza', 'age': '24', 'gpa': '3.85', 'courses': ['Networks', 'DB']}
```

The file students.xml should look like this.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<students>
    <student id="1">
        <name>Ali Khan</name>
        <age>22</age>
        <gpa>3.75</gpa>
        <courses>
            <course>SCD</course>
            <course>DB</course>
        </courses>
    </student>
</students>
```
