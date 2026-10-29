def create_task(name:str, priority:str, status:str) -> dict:
    return {
        "task": name,
        "priority": priority,
        "status": status
    }
    

def is_valid_priority(priority: str)->bool:
    return priority in ('High', 'Low', 'Medium', 'high', 'low', 'medium')

def is_valid_status(status: str) -> bool:
    return status in ('Pending', 'Done', 'pending', 'done')

def add_task(todo_list: list, name:str, priority: str, status: str):
    todo_list.append(create_task(name, priority, status))

def mark_done(todo_list:list, name:str):
    for item in todo_list:
        if item['task'] == name:
            item['status'] = 'done'

def remove_task(todo_list:list, name:str):
    for item in todo_list:
        if item['task'] == name:
            todo_list.remove(item)

def count_tasks(todo_list: list) -> int:
    """Returns total task count."""
    return len(todo_list)

def count_done(todo_list: list) -> int:
    """Returns done task count using lambda + filter."""
    return len(list(filter(lambda item: item["status"].lower() == "done", todo_list)))

def count_pending(todo_list: list) -> int:
    """Returns pending task count using lambda + filter."""
    return len(list(filter(lambda item: item["status"].lower() == "pending", todo_list)))

def print_task(task: dict) -> None:
    """Formats and prints a single task."""
    print(f"Task: {task['task']} | Priority: {task['priority']} | Status: {task['status']}")

def print_all_tasks(todo_list: list) -> None:
    """Prints all tasks by delegating to print_task."""
    for task in todo_list:
        print_task(task)  

def main():
    todo_list = []
    todo_list.append({"task": "Finish the Q4 financial report", "priority": "High", "status": "done"})
    todo_list.append({"task": "Schedule annual dental checkup", "priority": "Low", "status": "Pending"})
    todo_list.append({"task": "Renew car insurance policy", "priority": "High", "status": "Pending"})
    todo_list.append({"task": "Grocery shopping for the week", "priority": "Medium", "status": "Pending"})
    todo_list.append({"task": "Fix the leaking kitchen faucet", "priority": "Medium", "status": "done"})

    mark_done(todo_list, 'Grocery shopping for the week')
    remove_task(todo_list, "Fix the leaking kitchen faucet")



    pending_tasks = lambda todo_list: len(list(filter(lambda item: item['status'] == 'Pending', todo_list)))
    done_tasks = lambda todo_list:len( list(filter(lambda item: item['status'] == 'done', todo_list)))


    print("Total tasks: ", len(todo_list))
    print("Done Tasks: ", done_tasks(todo_list))
    print("Pending tasks: ", pending_tasks(todo_list))
main()