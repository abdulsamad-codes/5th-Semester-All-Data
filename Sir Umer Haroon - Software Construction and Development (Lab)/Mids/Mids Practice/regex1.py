import re
text = "Apples: 5, Oranges: 10, Bananas: 15"


findall_res = re.findall(r"\w+", text)
print("re.findall():", findall_res) # Output: ['5', '10', '15']
                                               