import re
user_input = input("Enter a Pakistani phone number: ")

pattern = r"^\+92[\s-]*\d{3}[\s-]*\d{7}$"

print("is the number pakistani ", bool(re.match(pattern, user_input)))