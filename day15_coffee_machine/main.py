# Additional functionalities/features and other changes compared to course solution:
# 1. Improvement of resources dictionary so that the units of measurement are not hardcoded.
# 2. Addition of a COINS dictionary for ease of access (no hardcoding) and iteration.
# 3. Validation of *all* user inputs: order, inserted coins, etc.
# 4. Addition of a function refill() to enable continued "machine use" without exiting the program,
#    and a function turn_off() to exit the program.
# 5. Extensive use of loops and intermediate dictionary referencing to get inputs, iterate printing, update values, etc.

from references import MENU, COINS

resources = {
    "water": {"amount": 300, "unit": "mL"},
    "milk": {"amount": 200, "unit": "mL"},
    "coffee": {"amount": 100, "unit": "g"}
}

money = 0

enter_whole_num = "Invalid input. Enter a whole number."

def get_order():
    """Validates the order inputted by user, prompts user for invalid inputs, and repeats until order is valid"""
    choices = ["espresso", "latte", "cappuccino", "off", "report", "refill"]
    while True:
        order = input("\nWhat would you like? Espresso / Latte / Cappuccino: ").lower()
        if order in choices:
            return order
        else:
            print("Choose only from the three items in the menu.")

def turn_off():
    """Turns off the machine for maintenance (i.e. ends the program)"""
    input("Machine will turn off when you press Enter.")

def print_report():
    for ingredient, attribute in resources.items():
        print(f"{ingredient.title()}: {attribute['amount']} {attribute['unit']}")
    print(f"Money: ${money:.2f}")

def refill():
    """Allows digital refill of coffee ingredients for machine maintenance"""
    for ingredient, attribute in resources.items():
        while True:
            try:
                refill_amount = int(input(f"Amount of {ingredient} (in {attribute['unit']}): "))
                if refill_amount >= 0:
                    attribute['amount'] += refill_amount
                    break
                else:
                    print(enter_whole_num)
            except ValueError:
                print(enter_whole_num)
    print("\nUpdated resources: ")
    print_report()

def check_resources(order):
    """Checks if there is sufficient ingredients in the machine to fulfill the current order"""
    need_refill = []
    for ingredient, amount_needed in MENU[order]['ingredients'].items():
        if amount_needed > resources[ingredient]['amount']:
            need_refill.append(ingredient)
    return ", ".join(need_refill)

def get_payment(order):
    """Prompts user to insert coins and gets their payment"""
    price = MENU[order]['cost']
    n = "n" if order == "espresso" else ""
    print(f"\nA{n} {order} costs ${price:.2f}. Please insert coins:")
    payment = 0
    for coin_data in COINS.values():
        coin_count = validate_coins(coin_data['name'], coin_data['display'])
        payment += coin_count * coin_data['value']
    return round(payment, 2)

def validate_coins(coin_str, coin_display):
    """Validates number of coins inserted (entered) -- should be whole number"""
    while True:
        try:
            coin_count = int(input(f"Number of {coin_str} {coin_display}: "))
            if coin_count >= 0:
                return coin_count
            else:
                print(enter_whole_num)
        except ValueError:
            print(enter_whole_num)

def process_payment(order, payment):
    """Adds the price of the order to the money of the machine and gives change when applicable"""
    global money
    money += MENU[order]['cost']
    if payment > MENU[order]['cost']:
        change = round(payment - MENU[order]['cost'], 2)
        print(f"Here is your change: ${change:.2f}")
    else:
        print("Exact amount received.")

def make_coffee(order):
    """Deducts the amount of ingredients from the machine inventory and gives the order to the user.
    Restarts the machine after"""
    for ingredient, amount in MENU[order]['ingredients'].items():
        resources[ingredient]['amount'] -= amount
    print(f"\nHere is your {order} ☕. Enjoy!")

def coffee_machine():
    """Top level program flow"""
    print("\n*** ☕ Coffee Machine Started ☕ ***")
    while True:
        order = get_order()
        if order == "off":
            turn_off()
            break
        elif order == "report":
            print_report()
        elif order == "refill":
            refill()
        else:
            need_refill = check_resources(order)
            if need_refill:
                print(f"Sorry, there is not enough {need_refill}.")
            else:
                payment = get_payment(order)
                if payment < MENU[order]['cost']:
                    print("Sorry, that's not enough money. Money refunded.")
                else:
                    process_payment(order, payment)
                    make_coffee(order)


coffee_machine()