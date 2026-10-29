# Name: Awais Qarni
import json
import re

DATA_FILE = "friends_data.json"

def validate_username(username):
    pattern = r"^[a-zA-Z0-9_]{3,15}$"
    return bool(re.match(pattern, username))

def validate_email(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))

def validate_phone(phone):
    pattern = r"^\+92-\d{3}-\d{7}$"
    return bool(re.match(pattern, phone))

def validate_date(date_str):
    pattern = r"^\d{2}/\d{2}/\d{4}$"
    return bool(re.match(pattern, date_str))

def load_data():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_data(friends_list):
    try:
        with open(DATA_FILE, "w") as file:
            json.dump(friends_list, file, indent=4)
        return True
    except IOError:
        return False

def create_friend_profile(name, username, email, phone, date_added, trust_score):
    return {
        "name": name,
        "username": username,
        "email": email,
        "phone": phone,
        "date_added": date_added,
        "trust_score": trust_score
    }

def add_friend(friends_list):
    name = input("Enter Friend Name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return
        
    username = input("Enter Username (3-15 chars, alnum/_): ").strip()
    if not validate_username(username):
        print("Invalid username format.")
        return
        
    email = input("Enter Email: ").strip()
    if not validate_email(email):
        print("Invalid email format.")
        return
        
    phone = input("Enter Phone (+92-XXX-XXXXXXX): ").strip()
    if not validate_phone(phone):
        print("Invalid phone format.")
        return
        
    date_added = input("Enter Date (DD/MM/YYYY): ").strip()
    if not validate_date(date_added):
        print("Invalid date format.")
        return
        
    try:
        trust_score = int(input("Enter Trust Score (1-100): "))
        if trust_score < 1 or trust_score > 100:
            print("Trust score must be between 1 and 100.")
            return
    except ValueError:
        print("Invalid number entered.")
        return
        
    new_friend = create_friend_profile(name, username, email, phone, date_added, trust_score)
    friends_list.append(new_friend)
    if save_data(friends_list):
        print("Friend profile added successfully!")
    else:
        print("Error saving data to file.")

def display_friends(friends_list):
    if not friends_list:
        print("No friends found in the registry.")
        return
        
    print("\n--- True Friends List ---")
    for index, friend in enumerate(friends_list, start=1):
        print(f"{index}. {friend['name']} (@{friend['username']})")
        print(f"   Email: {friend['email']} | Phone: {friend['phone']}")
        print(f"   Added: {friend['date_added']} | Trust Score: {friend['trust_score']}/100")
        print("-" * 40)

def update_trust_score(friends_list):
    username = input("Enter username of friend to update: ").strip()
    for friend in friends_list:
        if friend['username'] == username:
            try:
                new_score = int(input("Enter new Trust Score (1-100): "))
                if 1 <= new_score <= 100:
                    friend['trust_score'] = new_score
                    save_data(friends_list)
                    print("Trust score updated successfully!")
                    return
                else:
                    print("Score must be between 1 and 100.")
                    return
            except ValueError:
                print("Invalid number entered.")
                return
    print("Friend username not found.")

def main():
    friends_list = load_data()
    while True:
        print("\n=== True Friends Platform ===")
        print("1. Add New Friend")
        print("2. View All Friends")
        print("3. Update Trust Score")
        print("4. Exit")
        
        choice = input("Enter choice (1-4): ").strip()
        if choice == "1":
            add_friend(friends_list)
        elif choice == "2":
            display_friends(friends_list)
        elif choice == "3":
            update_trust_score(friends_list)
        elif choice == "4":
            print("Exiting platform. Goodbye!")
            break
        else:
            print("Invalid choice, please select 1-4.")

if __name__ == "__main__":
    main()
