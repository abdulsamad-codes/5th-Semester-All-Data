inventory_list = []
while True:
	user_input = input("Enter an item (or type 'done' to finish): ").strip().lower()
	if user_input == "done":
		break
	if not user_input:
		continue
	if user_input.startswith("remove "):
		item_to_remove = user_input[7:].strip()
		if item_to_remove in inventory_list:
			inventory_list.remove(item_to_remove)
			print(f"Removed: {item_to_remove}")
		else:
			print(f"Item not found: {item_to_remove}")
	elif user_input in inventory_list:
		print(f"Item already exists: {user_input}")
	else:
		inventory_list.append(user_input)
		print(f"Added: {user_input}")

inventory_list.sort()

print("\nFinal inventory:")
print(f"Total items: {len(inventory_list)}")
for item in inventory_list:
	print(item)
