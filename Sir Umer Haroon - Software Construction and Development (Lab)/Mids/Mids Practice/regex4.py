import re

passw="Pa$$w0rd123!"

# pattern = r"^(\d{1,2}[1-31])/(\d{1,2}[1-12])/(\d{4})$"

pattern = r"(\w+\d+[!@#$%]+){8}?"
print("Is valid date: ", bool(re.search(pattern, passw)))


