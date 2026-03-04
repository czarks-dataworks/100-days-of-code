# Additional functionalities/features and other changes compared to course solution:
# 1. Removes already selected items from the list to avoid repetition of items shown in game. Game ends when either items run out or when guess is incorrect.
# 2. Adds an exit option for the player to exit the game anytime, and an exit confirmation to ensure player wants to exit.
# 3. Includes input validation with set number of attempts amd attempt notifications to handle invalid user inputs.
# 4. Gives player the option to play again after losing a game so that there will be no need to restart the program to play again.

import random
import os
from art import logo, vs
from game_data import data

def format_items(item_a, item_b):
    """Formats the randomly selected items"""
    format_a = item_a['name'] + ", a(n) " + item_a['description'] + ", from " + item_a['country']
    format_b = item_b['name'] + ", a(n) " + item_b['description'] + ", from " + item_b['country']
    return format_a, format_b

def validate_input(ans):
    """Checks if user input is valid, converts it to lower case, and returns it to gameplay.
    Otherwise, player is warned of remaining attempts. Program ends if attempts run out."""
    valid_choices = ["a", "b", "x", "A", "B", "X"]
    attempts = 3
    while attempts > 0:
        if ans in valid_choices:
            return ans.lower()
        else:
            attempts -= 1
            if attempts == 1:
                s = ""
            else:
                s = "s"
            if attempts == 0:
                print("Number of invalid inputs reached.")
                program_exit()
            else:
                ans = input(f"Invalid input. Enter only 'A', 'B', or 'X'. You have {attempts} attempt{s} remaining: ")

def check_guess(ans, a_follower_count, b_follower_count):
    """Compares player's guess to actual result. Returns True for correct guess, False for incorrect guess."""
    if a_follower_count > b_follower_count:
        higher = 'a'
    else:
        higher = 'b'
    if ans == higher:
        return True
    else:
        if a_follower_count == b_follower_count:
            return True
        else:
            return False

def exit_confirmation():
    confirmation = input("\nDo you really want to exit? Enter 'X' again to confirm. Any other input will bring you back into the game: ").lower()
    if confirmation == 'x':
        program_exit()
    else:
        return True

def program_exit():
    input("\nProgram will end. Good bye!")
    exit()

def one_game(data_in_game):
    """The gameplay. Ends when player makes one wrong guess or when items from the list run out."""
    running_score = 0
    notice = ""
    game_over = False
    item_b = random.choice(data_in_game)        # Note: item_b and item_a are both type dictionary
    data_in_game.remove(item_b)

    while True:
        print(logo, notice)
        if len(data_in_game) == 0:
            print(f"\nYou have exhausted all items in the list. Final score: {running_score}. YOU WIN!")
            break
        if game_over:
            break
        item_a = item_b
        item_b = random.choice(data_in_game)
        data_in_game.remove(item_b)

        formatted_a, formatted_b = format_items(item_a, item_b)
        print("Compare A:", formatted_a)
        print(vs)
        print("Against B:", formatted_b)

        exit_option = True
        while exit_option:
            guess = input("\nWho has more followers? Enter 'A' or 'B' (or 'X' to exit): ")
            guess = validate_input(guess)
            if guess == "x":
                exit_option = exit_confirmation()
            else:
                break

        is_correct = check_guess(guess, item_a['follower_count'], item_b['follower_count'])
        if is_correct:
            running_score += 1
            notice = f"\nYou're right! Current score: {running_score}"
        else:
            notice = f"\nSorry, that's wrong. Final score: {running_score}"
            game_over = True

        os.system("cls")

def higher_lower():
    """Top level gameplay. When player loses one game, they are given an option to play again"""
    while True:
        data_copy = data.copy()
        one_game(data_copy)
        play_again = input("\nDo you want to play again? Enter 'X' to exit. Any other input will restart the game: ").lower()
        if play_again == "x":
            program_exit()
        else:
            os.system("cls")


higher_lower()