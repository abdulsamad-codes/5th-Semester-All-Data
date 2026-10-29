import re

text = "The quick brown fox jumps over 9 lazy dogs! Item #101 cost $50."

pattern = r"[a-fA-F0-9]"
found = re.findall(pattern, text)
print(found)

pattern2 = r"\b[^aeiou][a-z]\b"
found = re.findall(pattern2, text)
print(found)

pattern3 = r"^[$£€][0-9]$"
found = re.findall(pattern3, text)
print(found)