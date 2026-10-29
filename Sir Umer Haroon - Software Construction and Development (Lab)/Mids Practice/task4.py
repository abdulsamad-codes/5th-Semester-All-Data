def validate_pin(pin:int, correct_pin:int) ->bool:
    return pin == correct_pin 

def check_balance(balance:int, amount:int)->bool:
    return balance >= amount 

def is_valid_multiple(amount: int) -> bool:
    return amount % 500 == 0

def withdraw(balance:int, amount:int)->int:
    return balance - amount

def format_receipt(balance:int, amount:int, account_holder_name:str) -> str:
    return (
    "========== RECEIPT ==========\n"
    f"Account Holder : {account_holder_name}\n"
    f"Amount Withdrawn: {amount}\n"
    f"Remaining Balance: {balance}\n"
    "============================="
)

def main():
    CORRECT_PIN = 1234
    balance = 10000
    while True:
        account_holder_name = input("Enter account holder name: ")
        entered_pin = int(input("Enter PIN: "))
        if not validate_pin(entered_pin, CORRECT_PIN):
            print(f"The PIN is not correct try again later")
            continue

        amount = int(input("Enter withdrawal amount: "))
        if not check_balance(balance, amount):
            print(f"The entered amount is greater than the balance, try again later")
            continue
        
        if not is_valid_multiple(amount):
            print("The amount is not the multiple of 500, Try Again")
            continue
        new_balance = withdraw(balance, amount)
        print(format_receipt(new_balance, amount, account_holder_name))


main()