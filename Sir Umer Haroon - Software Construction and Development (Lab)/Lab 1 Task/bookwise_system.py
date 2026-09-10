import json
import os
from datetime import datetime, timedelta

# File to store data
DATA_FILE = "library_data.json"

class Item:
    """Base class for all library items"""
    def __init__(self, item_id, name, item_type):
        self.item_id = item_id
        self.name = name
        self.item_type = item_type
        self.is_available = True
        self.borrowed_by = None
        self.borrow_date = None
        self.renewal_count = 0

class Book(Item):
    """Book item - can be borrowed and renewed"""
    def __init__(self, item_id, name):
        super().__init__(item_id, name, "Book")
        self.max_renewals = 2

class Magazine(Item):
    """Magazine item - can be borrowed but not renewed"""
    def __init__(self, item_id, name):
        super().__init__(item_id, name, "Magazine")

class DVD(Item):
    """DVD item - can be borrowed with rental fee"""
    def __init__(self, item_id, name, rental_fee=2.0):
        super().__init__(item_id, name, "DVD")
        self.rental_fee = rental_fee

class LibrarySystem:
    """Main library management system"""
    
    def __init__(self):
        self.items = []
        self.next_id = 1
        self.load_data()
    
    def load_data(self):
        """Load all items from file"""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r') as f:
                    data = json.load(f)
                    for item_data in data:
                        if item_data['type'] == "Book":
                            item = Book(item_data['id'], item_data['name'])
                        elif item_data['type'] == "Magazine":
                            item = Magazine(item_data['id'], item_data['name'])
                        else:
                            item = DVD(item_data['id'], item_data['name'])
                        
                        item.is_available = item_data['is_available']
                        item.borrowed_by = item_data['borrowed_by']
                        item.borrow_date = item_data['borrow_date']
                        item.renewal_count = item_data['renewal_count']
                        self.items.append(item)
                        self.next_id = max(self.next_id, item.item_id + 1)
            except:
                print("Error loading data!")
        else:
            self.items = []
    
    def save_data(self):
        """Save all items to file"""
        data = []
        for item in self.items:
            data.append({
                'id': item.item_id,
                'name': item.name,
                'type': item.item_type,
                'is_available': item.is_available,
                'borrowed_by': item.borrowed_by,
                'borrow_date': item.borrow_date,
                'renewal_count': item.renewal_count
            })
        
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)
    
    def add_item(self, name, item_type, rental_fee=None):
        """Add a new item to library"""
        if item_type.lower() == "book":
            item = Book(self.next_id, name)
        elif item_type.lower() == "magazine":
            item = Magazine(self.next_id, name)
        elif item_type.lower() == "dvd":
            item = DVD(self.next_id, name, rental_fee if rental_fee else 2.0)
        else:
            print("Invalid item type! Use: Book, Magazine, or DVD")
            return
        
        self.items.append(item)
        self.next_id += 1
        self.save_data()
        print(f"✓ {name} added successfully (ID: {item.item_id})")
    
    def view_all_items(self):
        """Display all items"""
        if not self.items:
            print("No items in library!")
            return
        
        print("\n" + "="*70)
        print(f"{'ID':<5} {'Name':<20} {'Type':<10} {'Status':<15} {'Borrowed By':<15}")
        print("="*70)
        for item in self.items:
            status = "Available" if item.is_available else "Borrowed"
            borrowed_by = item.borrowed_by if item.borrowed_by else "-"
            print(f"{item.item_id:<5} {item.name:<20} {item.item_type:<10} {status:<15} {borrowed_by:<15}")
        print("="*70 + "\n")
    
    def borrow_item(self, item_id, borrower_name):
        """Borrow an item"""
        item = self.find_item(item_id)
        
        if not item:
            print("Item not found!")
            return
        
        if not item.is_available:
            print(f"Sorry! {item.name} is already borrowed by {item.borrowed_by}")
            return
        
        item.is_available = False
        item.borrowed_by = borrower_name
        item.borrow_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.save_data()
        print(f"✓ {item.name} borrowed by {borrower_name}")
    
    def return_item(self, item_id):
        """Return an item"""
        item = self.find_item(item_id)
        
        if not item:
            print("Item not found!")
            return
        
        if item.is_available:
            print(f"{item.name} is not borrowed!")
            return
        
        # Check for overdue
        borrow_datetime = datetime.strptime(item.borrow_date, "%Y-%m-%d %H:%M:%S")
        days_borrowed = (datetime.now() - borrow_datetime).days
        
        late_fee = 0
        if days_borrowed > 14:
            late_fee = (days_borrowed - 14) * 0.50  # $0.50 per day
            print(f"⚠ OVERDUE! Item was borrowed for {days_borrowed} days.")
            print(f"  Late fee: ${late_fee:.2f}")
        
        item.is_available = True
        item.borrowed_by = None
        item.borrow_date = None
        item.renewal_count = 0
        self.save_data()
        print(f"✓ {item.name} returned successfully")
    
    def renew_item(self, item_id):
        """Renew a borrowed book"""
        item = self.find_item(item_id)
        
        if not item:
            print("Item not found!")
            return
        
        if item.is_available:
            print(f"{item.name} is not borrowed!")
            return
        
        if item.item_type != "Book":
            print(f"Only books can be renewed! {item.name} is a {item.item_type}")
            return
        
        if item.renewal_count >= item.max_renewals:
            print(f"Cannot renew! Maximum renewals ({item.max_renewals}) reached.")
            return
        
        # Check for overdue
        borrow_datetime = datetime.strptime(item.borrow_date, "%Y-%m-%d %H:%M:%S")
        days_borrowed = (datetime.now() - borrow_datetime).days
        
        if days_borrowed > 14:
            print("Cannot renew overdue items! Please return first.")
            return
        
        item.renewal_count += 1
        item.borrow_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.save_data()
        print(f"✓ {item.name} renewed successfully (Renewal #{item.renewal_count})")
    
    def check_overdue(self):
        """Check and display overdue items"""
        overdue_items = []
        
        for item in self.items:
            if not item.is_available:
                borrow_datetime = datetime.strptime(item.borrow_date, "%Y-%m-%d %H:%M:%S")
                days_borrowed = (datetime.now() - borrow_datetime).days
                
                if days_borrowed > 14:
                    late_fee = (days_borrowed - 14) * 0.50
                    overdue_items.append({
                        'name': item.name,
                        'borrowed_by': item.borrowed_by,
                        'days': days_borrowed,
                        'fee': late_fee
                    })
        
        if not overdue_items:
            print("No overdue items!")
            return
        
        print("\n" + "="*70)
        print("OVERDUE ITEMS ALERT")
        print("="*70)
        for item in overdue_items:
            print(f"Name: {item['name']}")
            print(f"Borrowed by: {item['borrowed_by']}")
            print(f"Days overdue: {item['days'] - 14} days")
            print(f"Late fee: ${item['fee']:.2f}")
            print("-"*70)
        print("="*70 + "\n")
    
    def find_item(self, item_id):
        """Find an item by ID"""
        for item in self.items:
            if item.item_id == item_id:
                return item
        return None

def main():
    """Main menu system"""
    library = LibrarySystem()
    
    while True:
        print("\n" + "="*50)
        print("BOOKWISE SOLUTIONS - LIBRARY SYSTEM")
        print("="*50)
        print("1. Add Item")
        print("2. View All Items")
        print("3. Borrow Item")
        print("4. Return Item")
        print("5. Renew Book")
        print("6. Check Overdue Items")
        print("7. Exit")
        print("="*50)
        
        choice = input("Enter your choice (1-7): ").strip()
        
        if choice == "1":
            print("\nAdd Item")
            print("Types: Book, Magazine, DVD")
            item_type = input("Enter item type: ").strip()
            name = input("Enter item name: ").strip()
            
            if item_type.lower() == "dvd":
                try:
                    fee = float(input("Enter rental fee (default 2.0): ").strip() or 2.0)
                    library.add_item(name, item_type, fee)
                except:
                    library.add_item(name, item_type)
            else:
                library.add_item(name, item_type)
        
        elif choice == "2":
            library.view_all_items()
        
        elif choice == "3":
            try:
                item_id = int(input("Enter item ID: ").strip())
                borrower = input("Enter borrower name: ").strip()
                library.borrow_item(item_id, borrower)
            except:
                print("Invalid input!")
        
        elif choice == "4":
            try:
                item_id = int(input("Enter item ID: ").strip())
                library.return_item(item_id)
            except:
                print("Invalid input!")
        
        elif choice == "5":
            try:
                item_id = int(input("Enter book ID: ").strip())
                library.renew_item(item_id)
            except:
                print("Invalid input!")
        
        elif choice == "6":
            library.check_overdue()
        
        elif choice == "7":
            print("Thank you for using BookWise Solutions!")
            break
        
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
