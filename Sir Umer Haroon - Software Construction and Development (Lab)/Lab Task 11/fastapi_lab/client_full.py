import requests

BASE = "http://127.0.0.1:8000"

print("=== Step 1: Read all students ===")
initial_response = requests.get(f"{BASE}/students")
initial_data = initial_response.json()
print(f"Status: {initial_response.status_code}, Count: {initial_data['count']}")
print("Students:", initial_data["students"])

new_student = {
    "name": "Hassan Raza",
    "age": 21,
    "program": "SE",
}
new_student_id = initial_data["count"]

print("\n=== Step 2: Create a new student ===")
create_response = requests.post(f"{BASE}/students", json=new_student)
print(f"Status: {create_response.status_code}, Response: {create_response.json()}")

print("\n=== Step 3: Confirm the student was added ===")
updated_response = requests.get(f"{BASE}/students")
updated_data = updated_response.json()
print(f"Status: {updated_response.status_code}, Count: {updated_data['count']}")
print("Students:", updated_data["students"])

print("\n=== Step 4: Read the newly created student ===")
student_response = requests.get(f"{BASE}/students/{new_student_id}")
print(f"Status: {student_response.status_code}, Response: {student_response.json()}")

missing_student_id = updated_data["count"]
print("\n=== Step 5: Request a student that does not exist ===")
missing_response = requests.get(f"{BASE}/students/{missing_student_id}")
print(f"Status: {missing_response.status_code}, Response: {missing_response.json()}")
