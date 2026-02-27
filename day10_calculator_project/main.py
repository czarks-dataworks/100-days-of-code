import os
from art import logo

def add(n1, n2):
    return n1 + n2, n2

def subtract(n1, n2):
    return n1 - n2, n2

def multiply(n1, n2):
    return n1 * n2, n2

def divide(n1, n2):
    if n2 == 0:
        attempts_div = 3
        while n2 == 0 and attempts_div > 0:
            attempts_div -= 1
            if attempts_div == 0:
                print(zero_attempts_msg)
                exit()
            else:
                n2 = float(input(f"\nCannot divide by zero. Enter another number. {attempts_div} attempt(s) left: "))
    return n1 / n2, n2

operations = {
    "+": add, "-": subtract, "*": multiply, "/": divide,
}

zero_attempts_msg = "You have run out of attempts to enter a valid input. Program will end."

while True:
    print(logo)
    should_continue = 'y'
    first_input = True
    while should_continue == 'y':
        if first_input:
            attempts = 3
            while attempts > 0:
                try:
                    number1 = float(input("What's the first number?: "))
                    first_input = False
                    break
                except ValueError:
                    attempts -= 1
                    if attempts == 0:
                        print(zero_attempts_msg)
                        exit()
                    else:
                        print(f"Please enter a number. You have {attempts} attempt(s) left.")

        for symbol in operations:
            print(symbol)

        attempts = 3
        while attempts > 0:
            operation = input("Pick an operation by entering the equivalent symbol: ")
            if operation in operations:
                break
            else:
                attempts -= 1
                if attempts == 0:
                    print(zero_attempts_msg)
                    exit()
                else:
                    print(f"\nPlease enter a valid symbol. You have {attempts} attempt(s) left.")

        attempts = 3
        while attempts > 0:
            try:
                number2 = float(input("What's the next number?: "))
                break
            except ValueError:
                attempts -= 1
                if attempts == 0:
                    print(zero_attempts_msg)
                    exit()
                else:
                    print(f"\nPlease enter a number. You have {attempts} attempt(s) left.")

        result, number2 = operations[operation](number1, number2)
        print(f"\nCalculation: {number1} {operation} {number2} = {result}\n")

        should_continue = input(f"Enter 'y' to continue calculating with {result}, 'n' to start a new calculation,"
                                f" or any other key to exit the program: ").lower()
        if should_continue == 'y':
            number1 = result
        elif should_continue == 'n':
            print("\n" * 70)
            os.system("cls")
            break
        else:
            print("Program will end. Good bye.")
            exit()
