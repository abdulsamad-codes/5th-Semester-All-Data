import json

import requests

BASE = "http://127.0.0.1:8000"

invalid_student = {"name": "Missing Age"}
response = requests.post(f"{BASE}/students", json=invalid_student)
print("Status:", response.status_code)
print("Error body:", json.dumps(response.json(), indent=2))

# The 422 error is generated BEFORE create_student() runs.
# Add a print() inside create_student() to verify that this request never reaches it.
# FastAPI validates the JSON body against StudentCreate before calling the endpoint.
