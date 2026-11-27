import requests

BASE = "http://127.0.0.1:8000"

list_response = requests.get(f"{BASE}/students")
print("List status:", list_response.status_code)
print("List data:", list_response.json())

single_response = requests.get(f"{BASE}/students/1")
print("\nSingle status:", single_response.status_code)
print("Single data:", single_response.json())

invalid_response = requests.get(f"{BASE}/students/99")
print("\nInvalid status:", invalid_response.status_code)
print("Invalid data:", invalid_response.json())

# The invalid request returned 404 because main.py explicitly raises HTTPException(status_code=404).
# If that status were changed to 200, the client could mistake a missing student for a successful result.
# A 404 response clearly tells the client that the requested student does not exist.
