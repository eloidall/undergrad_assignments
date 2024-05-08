# Author: Éloi dallaire
# McGill ID: 260794674

from farkle_utils import *
import random


# Global Variables
SINGLE_ONE = 100
SINGLE_FIVE = 50
TRIPLET_MULTIPLIER = 100
STRAIGHT = 3000
THREE_PAIRS = 1500




def compute_score(selected_dice):
    """
    (list) -> int

    This function takes as input a list of integers between 1 and 6 (both included)
    representing the dice rolls selected by the player and return the points scored

    >>> compute_score([4,4,4,1])
    500
    
    >>> compute_score([1,5,5,1,4])
    0
    
    >>> compute_score([1,2,4,6,5,3])
    3000
    
    >>> compute_score([5,5,1])
    200
    
    >>> compute_score([3,6,6,2,3,2])
    1500
    
    >>> compute_score([1,1,1,1,1,1])
    2000
    """
    
    # To create a copy of the list taken as input
    selected_dice_copy = selected_dice[:]
    
    # To initialize points
    score = 0    
                    
    # To account for a straight (1 through 6)
    if (contains_all(selected_dice_copy) == True) and (len(selected_dice_copy) == 6):
        return STRAIGHT  
    
    
    # To account for 3 pairs
    if count_num_of_pairs(selected_dice_copy) == 3:
        
        # To account for 6 identical 1s
        if contains_repetitions(selected_dice_copy, 1, 6):
            return max(THREE_PAIRS, TRIPLET_MULTIPLIER * 10 * 2)
    
        # To account for 6 identical numbers except 1s
        for element in selected_dice_copy:
            if contains_repetitions(selected_dice_copy, element, 6):
                return max(THREE_PAIRS, TRIPLET_MULTIPLIER * element * 2)
            
        # If the three pairs are different
        else:
            return THREE_PAIRS
            
    # To account for other possibilities                             
    while len(selected_dice_copy) > 0:
        
        # To account for triplet
        for x in selected_dice_copy:
            
            # Triplet of 1s
            if contains_repetitions(selected_dice_copy, 1, 3):
                score += TRIPLET_MULTIPLIER * 10 * 1
                # To remove the triplet that scored from the list
                for y in range(3):
                    selected_dice_copy.remove(1)
                          
            # All other triplet of  
            elif contains_repetitions(selected_dice_copy, x, 3):
                score += TRIPLET_MULTIPLIER * x
                # To remove the triplet that scored from the list
                for y in range(3):
                    selected_dice_copy.remove(x)
                    

        # To account for SINGLE_ONE
        if contains_repetitions(selected_dice_copy, 1, 1):
            count = selected_dice_copy.count(1)
            score += SINGLE_ONE * count
            # To remove the dice that scored from the list
            for y in range(count):
                selected_dice_copy.remove(1)
        
        # To account for SINGLE_FIVE   
        elif contains_repetitions(selected_dice_copy, 5, 1):
            count = selected_dice_copy.count(5)
            score += SINGLE_FIVE * count
            # To remove the dice that scored from the list
            for y in range(count):
                selected_dice_copy.remove(5)
            
        # To account for all other possibilities as FARKLES
        elif contains_repetitions(selected_dice_copy, x, 1):
            return 0
            break
    
    return score
        
   

def convert_list_to_string(int_list, sep):
    """
    (list) -> str

    This function takes as input a list of integers and returns a string
    containing every element on one line and separated by a comma

    >>> convert_list_to_string([3,3,3,3,1,2,2], ", ")
    '3, 3, 3, 3, 1, 2, 2'
    
    >>> convert_list_to_string([1,2,3,4]," ")
    '1 2 3 4'
    
    >>> convert_list_to_string([-6, -152, 45, 12], " | ")
    '-6 | -152 | 45 | 12'
    """
    
    # To create a copy of the list taken as input
    int_list_copy = int_list[:]
    
    # To create a str_list with every element converted in string
    str_list = []
    for element in int_list_copy:
        str_list.append(str(element))

    # To display every element of the list on one line and separated by sep
    displayed_list = sep.join(str_list)
    return displayed_list

 
def convert_string_to_list(string):
    """
    (str) -> list
    
    This function takes as input a string and returns a list of integers of all the element
    
    >>> convert_string_to_list("3 3 3 3")
    [3, 3, 3, 3]
    
    >>> convert_string_to_list("1 1 2 3")
    [1, 1, 2, 3]
    
    >>> convert_string_to_list("6 5")
    [6, 5]
    """
    
    # To split all substrings into a list of string
    string_list = string.split()
    int_list = []
    
    # To store all element in a list as integers
    for element in string_list:
        int_list.append(int(element))
    return int_list
       
    
def get_winners(players_score, score_to_win):
    """
    (list, int) -> list

    This function takes as input a list of positive integers representings the
    scores of the players and a positive integer representing the score to reach
    to win the game. It returns a list of winning players.
    
    >>> get_winners([4,12,9,12],12)
    [2, 4]
    
    >>> get_winners([50,125,25],175)
    []
    
    >>> get_winners([50,125,25],24)
    [2]
    """
    
    # To create a copy of the list taken as input
    players_score_copy = players_score[:]
    
    # Input validation
    for element in players_score_copy:
        if element < 0:
            raise ValueError("the list must contain positive integers")
        
    if score_to_win < 0:
        raise ValueError("the winning score must be a positive integer")
    
    # To initialize the winners list
    winners = []
    
    for i in range(len(players_score_copy)):
        
        # To select all the players with the maximum points
        # that at least reached the winning_score
        if players_score_copy[i] >= score_to_win and players_score_copy[i] == max(players_score_copy[:]):
            winners.append(i+1)
    
    return winners
    
   
   
def play_one_turn(player_number):
    """
    (int) -> int

    This function takes as input a positive integer representing a player
    and returns the score of the player after they end their turn
    """
    # To identify which player's turn it is
    print("Player", player_number, "it's your turn!")
    
    score = 0
    available_dice = 6
    
    # To keep playing until there's no more dice available
    while available_dice > 0:
        
        # To get the player's action as an input
        player_action = input("\nWhat would you like to do? (roll or pass): ")
        
        # If the player decide to roll
        if player_action.lower() == "roll":
            
            # To roll the number of available dice and display the result
            dice_results = dice_rolls(available_dice)
            print("Here's the result of rolling your", available_dice,
                  "dice: ", convert_list_to_string(dice_results, ", "))
            
            # To get the player's selection of dice set aside for scoring
            while True:
                selected_dice = input("Please select the dice you'd like to set aside for scoring: ")
                selected_dice = convert_string_to_list(selected_dice)
                # To re-ask for an input until it's valid
                if is_included(dice_results, selected_dice) == True:
                    break
                          
            # To compute the points scored with the selected dice
            score += compute_score(selected_dice)
            
            # To compute the number of available_dice
            available_dice -= len(selected_dice)
  
            # To account for FARKLE
            if compute_score(selected_dice) == 0:
                print("FARKLE! All the points accumulated up to now are lost.")
                available_dice += len(selected_dice)
                score = 0
            
            if available_dice == 0:
                available_dice += 6
                print("HOT DICE! You are on a roll. You get all six dice back.")
                
            # To display the current score and the number of available_dice
            print("Your current score in this turn is: ", score) 
            print("You have", available_dice, "dice to keep playing.")
            
            
        # If the player decide to pass
        else:
            return score
        


def play_farkle():
    """
    () -> NoneType

    This function allows up to 8 players to play a game of Farkle
    """
    
    # To greet the participants
    print("Welcome to COMP202_Farkle!\n")
    
    # To determine the number of players
    while True:
        number_of_players = int(input("Please select the number of players (between 2 and 8): "))
        # To re-ask for an input until it's valid
        if 2 <= number_of_players <= 8:
            break
    
    # To determine the winning score
    while True:
        score_to_win = int(input("Select the winning score for this game: "))
        # To re-ask for an input until it's valid
        if score_to_win >= 0:
            break

    # To initialize each player's score in a list
    results = []
    for player_number in range(number_of_players):
        x = 0
        results.insert(player_number, x)
        
    # To keep playing until we have a winner
    round_ = 1
    while max(results) < score_to_win:
        
        # To add the points scored every round
        for player_number in range(number_of_players):
            print()
            round_score = play_one_turn(player_number+1)
            results[player_number] = round_score + results[player_number]
            
        # To display a points summary after each round played
        print("After round", round_, "the scores are as follows:")
        for player_number in range(number_of_players):
            print("Player", player_number+1, ":", results[player_number])
            
        round_ += 1

    # To display the winning players
    winning_players = pick_random_element(get_winners(results, score_to_win))
    
    print("Thanks for playing! The winner of this game is: ", end= "")
    print("Player", winning_players)
    




