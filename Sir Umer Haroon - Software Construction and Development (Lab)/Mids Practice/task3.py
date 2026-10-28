def clean_string(s: str) -> str:
    return "".join(char.lower() for char in s if char.isalnum())

def is_palindrome(s: str) -> bool:
    if len(s) < 2:
        return True
    if s[0] == s[-1]:
        return is_palindrome(s[1:-1])
    return False

def main():
    user_input = input("Enter a string: ")
    cleaned_string = clean_string(user_input)
    if is_palindrome(cleaned_string):
        print(f"The string {cleaned_string} is a palindrome.")
    else:
        print(f"The string {cleaned_string} is not a palindrome.")
main()