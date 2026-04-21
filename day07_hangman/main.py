# Additional functionalities/features and other changes compared to course solution:
# 1. Addition of three selectable themed word banks (Classic Words, Movies, Songs) with a theme selection system and corresponding word lists.
# 2. Implementation of a quit-anytime feature with confirmation to prevent accidental exits, allowing players to gracefully exit the game at any point.
# 3. Addition of a "guess entire word/title" option, allowing players to attempt the full answer in one go by entering 'guess' during gameplay.
# 4. Tracking and display of guess history (both correct and incorrect letters) when players re-enter a previously guessed letter.
# 5. Validation of all user inputs (theme selection, letter guesses, quit confirmations, replay) with limited attempts and clear error messaging.
# 6. Implementation of a replay system allowing players to start a new game without restarting the program, with the option to select a different theme.
# 7. Restructuring of game data into nested dictionaries and extensive use of helper functions for cleaner code organization and maintainability.

import random
import os
from words import word_list, movie_list, song_list
from art import stages, logo

themes = {
    'A': {
        'name': 'Classic Words',
        'words': word_list,
        'descriptor': 'word'
    },
    'B': {
        'name': 'Movies',
        'words': movie_list,
        'descriptor': 'movie title'
    },
    'C': {
        'name': 'Songs',
        'words': song_list,
        'descriptor': 'song title'
    }
}

no_attempts_remaining = "No more attempts remaining. Game will terminate. Follow instructions next time. Good bye!"

def print_themes():
    for key, theme_data in themes.items():
        print(f"  [{key}] {theme_data['name']}")

def choose_theme():
    attempts = 3
    while attempts > 0:
        print("\nChoose a theme:")
        print_themes()
        theme = input("\nEnter the letter that corresponds to your choice: ").upper()
        if theme in themes:
            print(f"\nYou have chosen to guess {str(themes[theme]['name']).upper()}!")
            return theme
        elif theme == "QUIT":
            if confirm_quit():
                return None
        else:
            attempts -= 1
            if attempts == 0:
                input(no_attempts_remaining)
                return None
            else:
                s = "s" if attempts > 1 else ""
                print(f"\nInvalid input. Enter only either A or B. You have {attempts} attempt{s} left.")
    return None

def confirm_quit():
    confirm = input("\n>> Are you sure you want to quit the game? Enter 'quit' again to confirm. Enter any other key to resume the game: ").upper()
    if confirm == "QUIT":
        input("\nThank you for playing. Good bye!")
        exit()
    else:
        return False

def create_display(unknown, correct_guesses = None):
    if correct_guesses is None:
        correct_guesses = []
    display = ""
    for character in unknown:
        if character in correct_guesses:
            display += character
        elif character.isalpha():
            display += "_"
        else:
            display += character
    return display

def validate_guess():
    attempts = 3
    while attempts > 0:
        guess = input("Enter a letter: ").upper()
        if guess == "QUIT":
            if confirm_quit():
                return None
        elif guess == "GUESS":
            return guess
        elif not guess.isalpha() or len(guess) != 1:
            attempts -= 1
            s = "s" if attempts > 1 else ""
            if attempts == 0:
                input(no_attempts_remaining)
                exit()
            else:
                print(f"Invalid input. Enter a letter only. You have {attempts} attempt{s} left.")
        else:
            return guess
    return None

def display_game_state(num_lives, message = ""):
    """Clear the screen and show current hangman stage with applicable message, if any"""
    os.system("cls")
    print(stages[num_lives])
    if message:
        print(message)

def guess_now(item):
    quit_game = False
    while not quit_game:
        guess = input(f"\nEnter the whole {item} (do not include symbols): ").upper()
        if guess == "QUIT":
            if confirm_quit():
                return None
            else:
                quit_game = False
        else:
            return guess
    return None

def notify_repeat_guess(letter, c_guesses, i_guesses):
    print(f"You have already guessed {letter}. Below are your previous guesses:")
    print("  Correct guesses:", ", ".join(c_guesses))
    print("  Incorrect guesses:", ", ".join(i_guesses))

def declare_final_outcome(win, unknown, item):
    if win:
        print(f"\nYou have guessed {unknown.upper()}!\n\n******* YOU WIN! 😏🏆 *******")
    else:
        print(f"\nYou have run out of lives. The {item} is: {unknown.upper()}!\n\n******* YOU LOSE. 🥺👎 *******")
    return True

def hangman():
    while True:
        print(logo)
        print("Welcome to Hangman! Enter 'quit' anytime to exit the game.")
        print("You may also guess the entire word/title in one go by entering 'guess'.")

        end_game = False
        num_lives = 9

        theme = choose_theme()
        if theme is None:
            break
        print("\nOnly letters of the alphabet are used. Symbols are removed and numbers are spelled out.")
        print("Enter a previously guessed letter to display all previous guesses.")
        word_bank = themes[theme]['words']
        unknown = random.choice(word_bank).upper()
        # print(unknown, "<-- NOT PRINTED IN ACTUAL GAMEPLAY") # Uncomment this line to display word/title to be guessed

        correct_guesses = []
        incorrect_guesses =[]
        display = create_display(unknown)

        while not end_game:
            print()
            item = themes[theme]['descriptor']
            print(f"Guess this {item}: {display}\n")
            lives = "lives" if num_lives > 1 else "life"
            print(f"You have {num_lives} {lives} left.")
            guess = validate_guess()
            if guess is None:
                break
            elif guess == "GUESS":
                guess = guess_now(item)
                if guess is None:
                    break
                elif guess == unknown:
                    end_game = declare_final_outcome(True, unknown, item)
                else:
                    num_lives -= 1
                    display_game_state(num_lives, f"That is not the {item}! You lose one life!")
                    if num_lives == 0:
                        end_game = declare_final_outcome(False, unknown, item)
            elif guess in correct_guesses or guess in incorrect_guesses:
                display_game_state(num_lives)
                notify_repeat_guess(guess, correct_guesses, incorrect_guesses)
            elif guess in unknown:
                correct_guesses.append(guess)
                display_game_state(num_lives, f"{guess.upper()} is correct!")
                display = create_display(unknown, correct_guesses)
                if "_" not in display:
                    end_game = declare_final_outcome(True, unknown, item)
                else:
                    end_game = False
            else:
                incorrect_guesses.append(guess)
                num_lives -= 1
                display_game_state(num_lives, f"{guess.upper()} is wrong! You lose one life!")
                if num_lives == 0:
                    end_game = declare_final_outcome(False, unknown, item)

        play_again = input("\n\n\n>> Do you wish to play again? Enter 'y' if yes, otherwise enter any other key: ").upper()
        if play_again != 'Y':
            input("\n******* GAME OVER. Thank you for playing Hangman! Good bye! *******")
            break
        else:
            os.system("cls")


hangman()

# Emoji choices: 🥲😃🎉😭😓😿🏅