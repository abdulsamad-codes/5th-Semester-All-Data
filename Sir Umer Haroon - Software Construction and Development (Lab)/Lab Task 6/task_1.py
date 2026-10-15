import re 

# def date_validation(date):
#     pattern = r"^\d{1,2}/\d{1,2}/\d{4}$"
#     return re.match(pattern, date)


# date = input("Enter the date in the (DD/MM/YY): ")
# if date_validation(date):
#     print("The date is valid")
# else:
#     print("The date is invalid")


# def phone_number_validation(phone_number):
#     pattern = r"^\+92[-\s]\d{3}[-\s]?\d{7}$"
#     return re.match(pattern, phone_number)


# phone_number = input("Enter your phone number: ")
# if phone_number_validation(phone_number):
#     print("The phone number is valid")
# else:
#     print("The phone number is invalid")


def date_validation_advanced(date):
    pattern = r"^(0?[1-9]|[12]\d|3[01])/(0?[1-9]|1[0-2])/[1-9]\d{3}$"
    return re.match(pattern, date)


date = input("Enter the date in the (DD/MM/YY): ")
if date_validation_advanced(date):
    print("The date is valid")
else:
    print("The date is invalid")

