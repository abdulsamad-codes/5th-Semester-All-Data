shopping_list = {}
while True:
    item = input("Enter the name of an item (q to quit): ").strip()
    if item == "q":
        break
    while True:
        quantity = int(input(f"Enter the quantity for {item}: "))
        if (quantity <= 0):
            print("The quantity must be positive.")
        else:
            break
    shopping_list[item] = quantity
print(shopping_list)
    