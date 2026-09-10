
def main():
    print("Hello")

class BookWiseSolutions:

    class Books:
        books = []
        borrow = bool
        returned = bool
    class Magazines:
        magazines = []
        borrow = bool
        renewed = bool
    class DVDS:
        dvds = []
        borrow = bool
        rental_fee = int

    def getbooks(self):
        for i, book in self.books:
            print(i + 1, self.book)

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
                pass
            else:
                return "The item is not found in the cart kindly check again"           
        else:
            return "Invalid Item Type Try Again Later"

if __name__ == "__main__":
    main()