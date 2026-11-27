import requests

BASE = "http://127.0.0.1:8000"

new_student = {
    "name": "Fatima Khan",
    "age": 20,
    "program": "CS",
}

response = requests.post(f"{BASE}/students", json=new_student)
print("Create status:", response.status_code)
print("Create response:", response.json())

list_response = requests.get(f"{BASE}/students")
all_students = list_response.json()["students"]
print("\nTotal students now:", len(all_students))
print("Last student:", all_students[-1])
