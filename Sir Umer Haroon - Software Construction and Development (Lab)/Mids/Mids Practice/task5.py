is_even = lambda num: num % 2 == 0
add_numbers = lambda a, b : a + b
first_letter = lambda my_string: my_string[0]
to_upper = lambda my_string: my_string.upper()
longer_than_five = lambda my_string: len(my_string) > 5


print(f"Sum of 4 and 7 is {add_numbers(4, 7)}")
print(f"Is 10 even? {is_even(10)}")
print(f"First letter of hello is {first_letter('hello')}")
print(to_upper('hello'))
print(f'Is "programming" longer than five characters? {longer_than_five("programming")}')