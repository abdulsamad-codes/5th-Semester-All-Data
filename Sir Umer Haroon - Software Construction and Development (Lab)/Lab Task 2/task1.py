shopping_list = {}
while True:
	item = input("Enter an item (or press Enter to finish): ").strip()
	if not item:
		break
	quantity_input = int(input(f"Enter the quantity for {item}: ").strip())
	if quantity_input < 1:
		print("Please enter a positive number.")
	else:
		shopping_list[item] = int(quantity_input)
print('''  Final shopping list:  ''')
for item, quantity in shopping_list.items():
	print(f"{item} : {quantity}")
