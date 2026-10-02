def create_task(name, priority, status):
    return {"name": name, "priority": priority, "status": status}

def is_valid_priority(priority):
    return priority in ("high", "medium", "low")
    
def is_valid_status(status):
    return status in ("pending", "done")

def add_task(to_do_list, name, priority, status):
    to_do_list.append(create_task(name, priority, status))

def mark_done(to_do_list, name):
    for task in to_do_list:
        if task["name"] == name:
            task["status"] = "done"
            break

def remove_task(to_do_list, name):
    for task in to_do_list:
        if task["name"] == name:
            to_do_list.remove(task)
            break

def count_tasks(to_do_list):
    return len(to_do_list)

def count_done(to_do_list):
    count = 0
    for task in to_do_list:
        if task["status"] == "done":
            count = count + 1
    return count

def count_pending(to_do_list):
    count = 0
    for task in to_do_list:
        if task["status"] == "pending": 
            count = count + 1
    return count

def print_task(task):
    print(f"Task: {task["name"]} | Priority: {task["priority"]} | Status: {task["status"]}")

def print_all_tasks(to_do_list):
    for list in to_do_list:
        print_task(list)



def main():
    
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
    print("\n")
    to_do_list = []

    add_task(to_do_list, "Buy groceries", "high", "pending")
    add_task(to_do_list, "Finish assignment", "high", "pending")
    add_task(to_do_list, "Call mom", "medium", "pending")
    add_task(to_do_list, "Read a chapter", "low", "pending")
    add_task(to_do_list, "Clean room", "low", "pending")

    mark_done(to_do_list, "Finish assignment")
    remove_task(to_do_list, "clean room")

    print_all_tasks(to_do_list)
    print()
    print(f"Total tasks: {count_tasks(to_do_list)}")
    print(f"Done tasks: {count_done(to_do_list)}")
    print(f"Pending tasks: {count_pending(to_do_list)}")
main()