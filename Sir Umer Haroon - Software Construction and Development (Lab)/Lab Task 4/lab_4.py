
add_numbers = lambda a, b: a + b
num1 = 3
num2 = 4
print(f"Sum of {num1} and {num2} is {add_numbers(num1, num2)}")

is_even = lambda num: num % 2 == 0
num = 3
print(f"Is {num} even? {is_even(num)}")

first_letter = lambda my_str: my_str[0]
name = "samad"
print(f"First letter of {name} is {first_letter(name)}")

to_upper = lambda my_str: my_str.upper()
print(to_upper("samad"))

longer_than_five = lambda my_str: len(my_str) > 5
my_str = "samad"
print(f"Is {my_str} longer than five characters? {longer_than_five(my_str)}")
