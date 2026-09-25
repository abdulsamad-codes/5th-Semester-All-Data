def validate_pin(entered_pin):
    return entered_pin == "1234"
        
def check_balance(balance, amount):
    return balance >= amount

def is_valid_multiple(amount):
    return amount % 500 == 0

def withdraw(balance, amount):
    return balance - amount

def format_receipt(account_holder_name, amount, new_balance):
    print('''=================== RECEIPT ==================''')
    print("Account Holder : ", account_holder_name)
    print("Amount Withdrawn: ", amount)
    print("Remaining Balance : ", new_balance)
    print('''=============================================''')

    # print("=" * 30)


def main():
    account_holder_name = input("Enter account holder name: ")
    account_pin = input("Enter PIN: ")
    amount = int(input("Enter withdrawal amount: "))
    balance = 10000
    if not(validate_pin(account_pin)):
        print("Incorrect PIN, Try Again Later")

    if not(check_balance(balance, amount)):
        print("Your amount is greater than the balance, Try again")
    
    if not(is_valid_multiple(amount)):
        print("Your amount is not a multiplie of 500, Try again")
    balance = withdraw(balance, amount)
    format_receipt(account_holder_name, amount, balance)

    
    
main()