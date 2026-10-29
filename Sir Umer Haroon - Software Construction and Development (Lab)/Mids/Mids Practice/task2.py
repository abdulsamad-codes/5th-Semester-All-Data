inventory_list = []
def item_input(prompt:str)->str:
    item_name = input(prompt).strip()
    if item_name.lower().isalnum():
            return item_name

def check_availability(item_name:str)->bool:
    if item_name in inventory_list:
        return True
    return False

def remove_item(item_name:str):
    updated_item_name = item_name[6:]
    if check_availability(updated_item_name):
        inventory_list.remove(updated_item_name)
        print(f"The item {updated_item_name} is removed from the inventory list")
    else:
        print(f"The item {updated_item_name} is not in the list.")



while True:

    item_name = item_input("Enter the item name (type 'done' once finished): ")
    if item_name == "done":
        break

    if check_availability(item_name):
        print(f"{item_name} already exists. ")
        continue

    if item_name[0:6] == "remove":
        remove_item(item_name)
    inventory_list.append(item_name)

inventory_list.sort()
total_item_count = len(inventory_list)
print("\n Final Summary of Inventory List ")
print(f"Total Items in the inventory list: {total_item_count}")
for index, item in enumerate(inventory_list):
    print(f"{index + 1} : {item}")