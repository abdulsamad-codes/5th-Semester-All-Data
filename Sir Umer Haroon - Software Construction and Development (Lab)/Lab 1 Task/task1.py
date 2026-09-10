
def main():
    item = BookWiseSolutions()
    print("Hello")
    print(item.add_item("my book", "book"))
    print(item.getbooks())
    print("hello")

class BookWiseSolutions:

    is_borrowed = bool
    is_returned = bool
    is_available: bool
    is_renewed = bool
    rental_fee = int
    
    def __init__(self, item, item_type):
        self.is_available = True
        self.is_returned = False
        self.is_borrowed = False
        self.is_renewed = False
        self.rental_fee = 2.0
        self.item = item
        self.item_type = item_type
        
    def getbooks(self):
        for i, book in enumerate(self.books):
            print(i + 1, book)

    def add_item(self, item, item_type):
        if item_type in ("book", "magazine", 'dvd'):
            if item_type == "book":
                self.books.append(item)
            elif item_type == 'magazine':
                self.magazines.append(item)
            else:
                self.dvds.append(item)
        else:
            return "Invalid Item Type Try Again Later"

    def borrow_item(self, item, item_type):
        if item_type in ("book", "magazine", 'dvd'):
            if item in (self.books, self.magazines, self.dvds):
                if item in self.books:
                    pass
            else:
                return "The item is not found in the cart kindly check again"           
        else:
            return "Invalid Item Type Try Again Later"
    def return_item(self, item, item_type):
        pass


if __name__ == "__main__":
    main()