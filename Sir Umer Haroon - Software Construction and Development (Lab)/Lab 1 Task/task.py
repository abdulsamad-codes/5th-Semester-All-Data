import json
from datetime import datetime
from pathlib import Path


DATA_FILE = Path(__file__).with_name("library_data.json")
BORROWING_DAYS = 14


class LibraryItem:
    def __init__(self, item_id, name, item_type):
        self.__item_id = item_id
        self.__name = name
        self.__item_type = item_type
        self.__available = True
        self.__borrowed_by = ""
        self.__borrow_date = ""
        self.__renewal_count = 0

    @property
    def item_id(self):
        return self.__item_id

    @property
    def name(self):
        return self.__name

    @property
    def item_type(self):
        return self.__item_type

    @property
    def available(self):
        return self.__available

    @property
    def borrowed_by(self):
        return self.__borrowed_by

    @property
    def borrow_date(self):
        return self.__borrow_date

    @property
    def renewal_count(self):
        return self.__renewal_count

    def borrow(self, borrower):
        self.__available = False
        self.__borrowed_by = borrower
        self.__borrow_date = datetime.now().isoformat(timespec="seconds")

    def return_item(self):
        self.__available = True
        self.__borrowed_by = ""
        self.__borrow_date = ""
        self.__renewal_count = 0

    def renew(self):
        self.__renewal_count += 1
        self.__borrow_date = datetime.now().isoformat(timespec="seconds")

    def borrowed_days(self):
        if self.__available or not self.__borrow_date:
            return 0
        borrowed_at = datetime.fromisoformat(self.__borrow_date)
        return (datetime.now() - borrowed_at).days

    def to_dict(self):
        return {
            "id": self.__item_id,
            "name": self.__name,
            "type": self.__item_type,
            "available": self.__available,
            "borrowed_by": self.__borrowed_by,
            "borrow_date": self.__borrow_date,
            "renewal_count": self.__renewal_count,
        }

    def load_status(self, data):
        self.__available = bool(data.get("available", True))
        self.__borrowed_by = data.get("borrowed_by", "") or ""
        self.__borrow_date = data.get("borrow_date", "") or ""
        self.__renewal_count = int(data.get("renewal_count", 0))


class Book(LibraryItem):
    MAX_RENEWALS = 2

    def __init__(self, item_id, name):
        super().__init__(item_id, name, "Book")


class Magazine(LibraryItem):
    def __init__(self, item_id, name):
        super().__init__(item_id, name, "Magazine")


class DVD(LibraryItem):
    def __init__(self, item_id, name, rental_fee=2.0):
        super().__init__(item_id, name, "DVD")
        self.__rental_fee = rental_fee

    @property
    def rental_fee(self):
        return self.__rental_fee

    def to_dict(self):
        data = super().to_dict()
        data["rental_fee"] = self.__rental_fee
        return data


class LibrarySystem:
    def __init__(self):
        self.__items = []
        self.__next_id = 1
        self.load_data()

    def load_data(self):
        if not DATA_FILE.exists():
            return
        try:
            data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            print("The saved data could not be loaded. Starting with an empty library.")
            return

        for item_data in data:
            item_type = str(item_data.get("type", "")).lower()
            item_id = int(item_data.get("id", self.__next_id))
            name = str(item_data.get("name", "Unnamed item"))
            if item_type == "book":
                item = Book(item_id, name)
            elif item_type == "magazine":
                item = Magazine(item_id, name)
            elif item_type == "dvd":
                item = DVD(item_id, name, float(item_data.get("rental_fee", 2.0)))
            else:
                continue
            item.load_status(item_data)
            self.__items.append(item)
            self.__next_id = max(self.__next_id, item_id + 1)

    def save_data(self):
        data = [item.to_dict() for item in self.__items]
        DATA_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def add_item(self, name, item_type, rental_fee=2.0):
        item_type = item_type.strip().lower()
        if item_type == "book":
            item = Book(self.__next_id, name)
        elif item_type == "magazine":
            item = Magazine(self.__next_id, name)
        elif item_type == "dvd":
            item = DVD(self.__next_id, name, rental_fee)
        else:
            return None
        self.__items.append(item)
        self.__next_id += 1
        self.save_data()
        return item

    def find_item(self, item_id):
        return next((item for item in self.__items if item.item_id == item_id), None)

    def all_items(self):
        return list(self.__items)

    def borrow_item(self, item_id, borrower):
        item = self.find_item(item_id)
        if item is None:
            return "Item was not found."
        if not item.available:
            return f"{item.name} is already borrowed by {item.borrowed_by}."
        item.borrow(borrower)
        self.save_data()
        return f"{item.name} was borrowed by {borrower}."

    def return_item(self, item_id):
        item = self.find_item(item_id)
        if item is None:
            return "Item was not found."
        if item.available:
            return f"{item.name} is already available."
        late_fee = self.late_fee(item)
        item.return_item()
        self.save_data()
        message = f"{item.name} was returned successfully."
        if late_fee:
            message += f" Late fee: ${late_fee:.2f}."
        return message

    def renew_item(self, item_id):
        item = self.find_item(item_id)
        if item is None:
            return "Item was not found."
        if item.available:
            return f"{item.name} is not borrowed."
        if not isinstance(item, Book):
            return "Only books can be renewed."
        if item.renewal_count >= Book.MAX_RENEWALS:
            return "This book has reached its renewal limit."
        if item.borrowed_days() > BORROWING_DAYS:
            return "This book is overdue and cannot be renewed."
        item.renew()
        self.save_data()
        return f"{item.name} was renewed successfully."

    def overdue_items(self):
        return [item for item in self.__items if item.borrowed_days() > BORROWING_DAYS]

    def late_fee(self, item):
        overdue_days = max(0, item.borrowed_days() - BORROWING_DAYS)
        return overdue_days * 0.50


def read_integer(prompt):
    try:
        return int(input(prompt).strip())
    except ValueError:
        print("Please enter a valid number.")
        return None


def show_items(library):
    items = library.all_items()
    if not items:
        print("There are no items in the library.")
        return
    print("\nID | Name | Type | Status | Borrowed by")
    print("-" * 65)
    for item in items:
        status = "Available" if item.available else "Borrowed"
        borrower = item.borrowed_by or "-"
        extra = f" | Fee: ${item.rental_fee:.2f}" if isinstance(item, DVD) else ""
        print(f"{item.item_id} | {item.name} | {item.item_type}{extra} | {status} | {borrower}")


def show_overdue_items(library):
    overdue = library.overdue_items()
    if not overdue:
        print("There are no overdue items.")
        return
    print("\nLate Fee Alert")
    for item in overdue:
        print(f"{item.name} is {item.borrowed_days() - BORROWING_DAYS} days overdue.")
        print(f"Late fee: ${library.late_fee(item):.2f}")


def run_menu():
    library = LibrarySystem()
    while True:
        print("\nBookWise Solutions")
        print("1. Add item")
        print("2. View all items")
        print("3. Borrow item")
        print("4. Return item")
        print("5. Renew book")
        print("6. Late Fee Alert")
        print("7. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            name = input("Enter item name: ").strip()
            item_type = input("Enter item type (Book, Magazine, DVD): ").strip()
            if not name:
                print("The item name cannot be empty.")
                continue
            fee = 2.0
            if item_type.lower() == "dvd":
                try:
                    fee = float(input("Enter DVD rental fee: ").strip())
                    if fee < 0:
                        raise ValueError
                except ValueError:
                    print("Please enter a valid non-negative fee.")
                    continue
            item = library.add_item(name, item_type, fee)
            print(f"{name} was added with ID {item.item_id}." if item else "Invalid item type.")
        elif choice == "2":
            show_items(library)
        elif choice == "3":
            item_id = read_integer("Enter item ID: ")
            if item_id is not None:
                borrower = input("Enter borrower name: ").strip()
                print(library.borrow_item(item_id, borrower) if borrower else "Borrower name cannot be empty.")
        elif choice == "4":
            item_id = read_integer("Enter item ID: ")
            if item_id is not None:
                print(library.return_item(item_id))
        elif choice == "5":
            item_id = read_integer("Enter book ID: ")
            if item_id is not None:
                print(library.renew_item(item_id))
        elif choice == "6":
            show_overdue_items(library)
        elif choice == "7":
            print("Thank you for using BookWise Solutions.")
            break
        else:
            print("Please choose a number from 1 to 7.")


if __name__ == "__main__":
    run_menu()