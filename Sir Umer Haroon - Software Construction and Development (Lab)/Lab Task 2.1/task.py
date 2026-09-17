def clean_string(input):
    cleaned_string = ""
    for character in input:
        if character.isalnum():
            cleaned_string += character.lower()

    return cleaned_string


def is_palindrome(input_string):
    if len(input_string) <= 1:
        return True
    if input_string[0] != input_string[-1]:
        return False
    return is_palindrome(input_string[1:-1])


def main():
    print(clean_string("Zai N Qn.k, "))
    user_input = input("Enter a word or phrase or sequence:")
    cleaned_input = clean_string(user_input)

    if is_palindrome(cleaned_input):
        print("The input is a palindrome.")
    else:
        print("The input is not a palindrome.")


if __name__ == "__main__":
    main()
