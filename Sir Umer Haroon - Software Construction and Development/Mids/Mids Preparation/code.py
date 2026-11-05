def countdown(n):
    if n == 0:
        return True 
   
    return countdown(n - 1 )

def main():
    user_input = int(input("enter a number: "))
    print(f" The number  {user_input} is cowntdown ",countdown(user_input))
main()