import requests

response = requests.get("http://127.0.0.1:8000/")
print("Status code:", response.status_code)
print("Response JSON:", response.json())

# The HTTP status code 200 means "OK" — the request succeeded.
# The .json() method parses the JSON text in the response body into a Python dictionary.
