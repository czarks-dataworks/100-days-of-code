# Additional functionalities/features and other changes compared to course solution:
# 1. Displays face cards in the hand (A, K, Q, and J) instead of their corresponding numerical values
# 2. Hand display has no quotation marks around letters representing face cards
# 3. Displays "*** BLACKJACK! ***" when blackjack conditions are met
# 4. Displays game stats after every round: rounds, wins, losses, and win streak
# 5. Asks if player wants to play again after the first/initial round, not at game start
# 6. More readable code with the use of functions that better reflect the game structure

import random
from art import logo
import os

card_values = {
    "A": 11,
    2: 2,
    3: 3,
    4: 4,
    5: 5,
    6: 6,
    7: 7,
    8: 8,
    9: 9,
    10: 10,
    "J": 10,
    "Q": 10,
    "K": 10,
}

deck = list(card_values.keys())

def initial_deal():
    """Returns two random cards from the deck at the start of the round"""
    card1 = random.choice(deck)
    card2 = random.choice(deck)
    hand = [card1, card2]
    score = get_score(hand)
    return hand, score


def deal(hand):
    """Returns one random card from the deck to add to the player's/dealer's hand and updates their score"""
    card = random.choice(deck)
    hand.append(card)
    score = get_score(hand)
    return score


def get_score(hand):
    """Calculates the score of the player's/dealer's hand"""
    score = 0
    for card in hand:
        score += card_values[card]
    if score > 21 and "A" in hand:
        aces_count = hand.count("A")
        score -= aces_count * 10
    return score


def format_hand(cards):
    card_string = (str(card) for card in cards)
    p_hand = "[" + ", ".join(card_string) + "]"
    return p_hand


def in_game_status(p_cards, p_score, d_first_card):
    """Displays the player's current hand and score and the dealer's first card"""
    p_hand = format_hand(p_cards)
    print(f"  Your cards: {p_hand}. Current score: {p_score}")
    print(f"  Computer's first card: [{d_first_card}].")


def conclude_round(p_cards, p_score, d_cards, d_score):
    """
    Outlines the series of actions to conclude the round when any of the following scenarios becomes true:
    1. Either player or dealer was dealt an initial hand with score of exactly 21 - Blackjack!;
    2. Player reaches a score of at least 21; or
    3. Dealer score exceeds 16
    """
    final_hands_and_scores(p_cards, p_score, d_cards, d_score)
    winner = decide_winner(p_score, d_score)
    is_blackjack = check_blackjack(p_cards, p_score, d_cards, d_score)
    declare_winner(winner, is_blackjack)
    return winner


def final_hands_and_scores(p_cards, p_score, d_cards, d_score):
    """Displays the final hands and scores"""
    p_hand = format_hand(p_cards)
    d_hand = format_hand(d_cards)
    print(f"\nYour final hand: {p_hand}. Your final score: {p_score}.")
    print(f"Computer's final hand: {d_hand}. Computer's final score: {d_score}.")


def decide_winner(p_score, d_score):
    """Determines the winner based on rules and respective scores"""
    if p_score > 21:  # Remaining scenarios: p_score <= 21, d_score = any, p & d may be equal
        winner = "dealer"
    elif d_score == 21:  # Rem. scenarios: p_score <= 21, d_score = anything but 21, p & d may be equal
        winner = "dealer"
    elif p_score == d_score:  # Rem. scenarios: p_score <= 21, d_score = anything but 21, p != d
        winner = "draw"
    elif d_score > 21:  # Rem. scenarios: p_score <= 21, d_score < 21, p != d
        winner = "player"
    elif p_score > d_score:  # Rem. scenarios: p_score < d_score
        winner = "player"
    else:  # p_score < d_score
        winner = "dealer"
    return winner


def check_blackjack(p_cards, p_score, d_cards, d_score):
    if (len(p_cards) == 2 and p_score == 21) or (len(d_cards) == 2 and d_score == 21):
        return True
    else:
        return False


def declare_winner(winner, is_blackjack):
    """Displays the winner. Also displays "Blackjack!" if either player or dealer has an Ace and a 10 card"""
    if is_blackjack:
        exclaim = "*** BLACKJACK! *** "
    else:
        exclaim = ""
    if winner == "player":
        print(f"\n{exclaim}You win! :D")
    elif winner == "dealer":
        print(f"\n{exclaim}You lose. :(")
    else:
        print(f"\n{exclaim}It's a draw!")


def play_blackjack(rounds, wins, win_streak):
    print(logo)
    rounds += 1
    player_cards, player_score = initial_deal()
    dealer_cards, dealer_score = initial_deal()
    in_game_status(player_cards, player_score, dealer_cards[0])

    if player_score == 21: # dealer_score condition was removed so that the player can still hit while dealer's cards are not yet revealed
        winner = conclude_round(player_cards, player_score, dealer_cards, dealer_score)
    else:
        while player_score < 21:
            hit = input("\nEnter 'y' to get another card. Enter any key to pass: ").lower()
            if hit == 'y':
                player_score = deal(player_cards)
                in_game_status(player_cards, player_score, dealer_cards[0])
            else:
                break
        while dealer_score <= 16:
            dealer_score = deal(dealer_cards)
        winner = conclude_round(player_cards, player_score, dealer_cards, dealer_score)

    if winner == "player":
        wins += 1
        win_streak += 1
    else:
        win_streak = 0

    return rounds, wins, win_streak


def display_stats(rounds, wins, win_streak):
    streak_messages = {
        3: "*** You're on a roll! ***",
        7: "*** Luck is DEFINITELY on your side! ***",
        10: "* * *   H A L L   O F   F A M E   * * *",
    }
    if win_streak in streak_messages:
        streak_message = streak_messages[win_streak]
    else:
        streak_message = ""
    print("Your game stats:")
    print(f"  Rounds played: {rounds}")
    print(f"  Wins: {wins}, Losses: {rounds - wins}")
    print(f"  Current winning streak: {win_streak}  " + streak_message)


game_on = True
round_count = 0
win_count = 0
winning_streak = 0

while game_on:
    round_count, win_count, winning_streak = play_blackjack(round_count, win_count, winning_streak)
    input()
    display_stats(round_count, win_count, winning_streak)
    choice = input("\nDo you wish to keep on playing? Enter 'y' to continue. Otherwise, enter any key: ").lower()
    if choice != 'y':
        print("\nThank you for playing! Game over.")
        game_on = False
    else:
        print("\n" * 50)
        os.system("cls")