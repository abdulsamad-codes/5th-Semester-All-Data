# Lab Task 7.1

If you are not present in lab, no need to attempt it

---

## Task 3: YAML and Config Files

### Background

YAML is a human-readable format often used for configuration files. It uses indentation instead of braces and brackets. Python does not include a YAML parser in the standard library, so you must install one using pip install pyyaml. The function yaml.safe_load converts a YAML string to a Python object. The function yaml.safe_dump converts a Python object to a YAML string.

### Scenario

You are building a configuration system for a small application. The configuration includes a list of students, a setting for the minimum GPA to pass, and a flag for whether the system is in debug mode. You will store this configuration in YAML and also in JSON so you can compare them.

### What to Do

#### Part A: Write the Configuration in YAML

Create a file called config.yaml by hand. It should contain a key debug set to true, a key min_gpa set to 3.5, and a key students that holds a list of at least three student records with the same fields as Task 1.

#### Part B: Load the YAML in Python

Create a file called task3_yaml.py. Install pyyaml first using pip. Write a function called load_config that takes a filename and returns the parsed configuration using yaml.safe_load.

Print the value of debug, the value of min_gpa, and loop over the students printing each one. Then print the type of the students value to confirm it is a list.

#### Part C: Convert YAML to JSON

Write a function called yaml_to_json that takes a YAML filename and a JSON filename, loads the YAML, and writes it as JSON. Call it to produce config_from_yaml.json.

Open both files side by side and write a short note in your report. Which one is easier to read as a human. Which one is easier for a machine to parse and why. Which one supports comments and why that matters for configuration.

### Expected Output

```text
Debug mode: True
Minimum GPA: 3.5

Students:
{'name': 'Ali Khan', 'age': 22, 'gpa': 3.75}
{'name': 'Sara Ahmed', 'age': 21, 'gpa': 3.90}
{'name': 'John Doe', 'age': 23, 'gpa': 3.60}

Type of students: <class 'list'>
```

The file config.yaml should look like this.

```yaml
debug: true
min_gpa: 3.5

students:
  - name: Ali Khan
    age: 22
    gpa: 3.75
  - name: Sara Ahmed
    age: 21
    gpa: 3.90
  - name: John Doe
    age: 23
    gpa: 3.60
```

---

## Task 4: Comparing Formats and Columnar Thinking

### Background

Different formats serve different needs. JSON is best for web APIs because browsers parse it natively. XML is best for enterprise systems that need schema validation and namespaces. YAML is best for configuration files because it is readable. Binary formats such as Protocol Buffers and Avro are best for performance-critical systems. Columnar storage is best for analytical queries over large datasets.

This task does not ask you to install a binary format library. Instead, it asks you to think about the tradeoffs concretely by measuring file sizes and simulating columnar access in pure Python.

### What to Do

#### Part A: Measure File Sizes

Write a file called task4_compare.py. Reuse the student data from Task 1. Write the same data to three files, students.json, students.xml, and students.yaml. Use os.path.getsize to print the size of each file in bytes.

#### Part B: Simulate Columnar Access

Write a function called sum_gpa_row_x	based that takes a list of student dictionaries and returns the sum of GPAs by looping over each student and reading the gpa key.ar


Write a function called sum_gpa_columnar that takes a dictionary where each key is a column name and each value is a list of values for that column, and returns the sum of the gpa column directly.

Call both functions on the same data and confirm they return the same result. Then write a short note in your report explaining in your own words why the columnar version is more efficient when the data is stored column by column on disk.

#### Part C: Design a Format Choice

Write a short report section answering these questions. If you were building a public REST API for a mobile app, which format would you choose and why. If you were building a configuration file for a DevOps pipeline, which format would you choose and why. If you were building an internal analytics system that scans millions of records to compute averages, which format would you choose and why. If you were building an internal microservice that must respond in under ten milliseconds, which format would you choose and why.

For each question, justify your answer using what you observed in this lab and what you learned in the theory class.

### Expected Output

```text
students.json size: 412 bytes
students.xml size: 624 bytes
students.yaml size: 298 bytes

Row based GPA sum: 18.5
Columnar GPA sum: 18.5
Results match: True
```

The exact byte counts will depend on the formatting you use. The important thing is the comparison between formats.

### HINTS

For Task 3, install pyyaml with pip before importing it, and always use yaml.safe_load instead of yaml.load for untrusted input. For Task 4, the exact byte counts do not matter as much as the relative comparison between formats. Keep each function focused on one task. Write comments explaining what each function does. Test your code with the sample data before moving on. If something does not work, read the error message carefully, it usually tells you exactly what is wrong.
