# Author: Éloi dallaire
# McGill ID: 260794674


import random


def single_dice_roll():
    """
    (none) -> int

    This function takes no input and returns a random integer between 1 and 6 (both included)

    >>> random.seed(3)
    >>> single_dice_roll()
    2

    >>> random.seed(100)
    >>> single_dice_roll()
    2
    
    >>> random.seed(30)
    >>> single_dice_roll()
    5
    """
    
    return random.randint(1,6)
    


def dice_rolls(n):
    """
    (int) -> list

    This function takes a positive integer n as input and returns a list
    containing the numbers representing n independant 6-sided dice rolls

    >>> random.seed(11)
    >>> dice_rolls(5)
    [4, 5, 4, 4, 5]

    >>> random.seed(30)
    >>> dice_rolls(3)
    [5, 3, 5]
    
    >>> random.seed(100)
    >>> dice_rolls(6)
    [2, 4, 4, 2, 6, 4]
    """
    
    # To initialize the list that will serve as the output
    dice_results = []
    
    # Input validation: the function should work for positive integers
    if n <= 0:
        raise ValueError("n must be positive")
    
    for i in range(n):
        roll = single_dice_roll()
        # to insert the result in the dice_results list
        dice_results.append(roll)
        
    return dice_results
    
        

def contains_repetitions(int_list, n, m):
    """
    (list, int, int) -> bool

    This function takes as input a list of integers, an integer n and a positive
    integer m and returns True if n appears in the list at least m times, False otherwise

    >>> contains_repetitions([1,2,1,1,2,1],1,3)
    True
    
    >>> contains_repetitions([1,2,3,4,5],3,8)
    False
    
    >>> contains_repetitions([1,-55,-6,-2,-2],-2,2)
    True
    """
    
    # To create a copy of the list taken as input
    int_list_copy = int_list[:]
    
    # Input validation: the function should work for positive integers values of m
    if m <= 0:
        raise ValueError("m must be positive")
    
    # To count the occurence of n in the list given as input
    n_count = int_list_copy.count(n)
    
    # To return True or False if n is found at least m times in the list
    return n_count >= m



def pick_random_element(int_list):
    """
    (list) -> int

    This function takes a list of integers as input and return a random element from the list

    >>> random.seed(5)
    >>> pick_random_element([15,-5,3])
    3
    
    >>> random.seed(150)
    >>> pick_random_element([1,5,2,89,4])
    2
    
    >>> random.seed(10)
    >>> pick_random_element([1,2,3,4,5,6,7])
    5
    """
    
    # To create a copy of the list taken as input
    int_list_copy = int_list[:]
    
    # The function will return None if the list is empty
    if len(int_list_copy) == 0:
        return
    
    # To select a random element from the list taken as input
    rand_idx = random.randint(0, len(int_list_copy)-1)
    random_element = int_list_copy[rand_idx] 
    
    return random_element



def contains_all(int_list):
    """
    (list) -> bool

    This function takes a list of integers as input and returns True if the
    list contains all unique consecutive positive integers starting from 1
    
    >>> contains_all([1,5,3,2,4])
    True

    >>> contains_all([2,4,1,2,3])
    False

    >>> contains_all([3,2,1])
    True
    """    
    
    # To create a sorted copy of the list taken as input
    sorted_int_list = int_list[:]
    sorted_int_list.sort()
    
    # To create a list of consecutive positive integer starting by 1
    # and to compare it to the sorted_int_list
    consecutive_list = []
    a = 1
    
    for i in range(len(sorted_int_list)):
        consecutive_list.append(a)
        a += 1
    return consecutive_list == sorted_int_list
        


def count_num_of_pairs(int_list):    
    """
    (list) -> int

    This function takes as input a list of integers
    and returns the number of pairs in the list

    >>> count_num_of_pairs([1,1,2,2])
    2
    
    >>> count_num_of_pairs([6,5,6,8,8,8,5])
    3
    
    >>> count_num_of_pairs([1,2,3,4,5])
    0
    """
    
    # To create a sorted copy of the list taken as input
    sorted_int_list = int_list[:]
    sorted_int_list.sort()
    
    pairs_count = 0
    i = 0
    while i < (len(sorted_int_list) - 1):
        
        # If two integers next to eachothers are equal, a pair is found
        if (sorted_int_list[i] == sorted_int_list[i + 1]):
            pairs_count += 1
            
            # We skip both the elements of that pair
            i += 2
        
        # If a pair is not found, we skip to the next element
        else:
            i += 1
            
    return pairs_count



def is_included(n, m1): 
    
    """
    (list,list) -> bool

    This function takes as input two lists of integers and returns
    True if the second one is a subset of the first one

    >>> n = [1,2,4,5,5,5]
    >>> m1 = [1,5,5,5]
    >>> is_included(n, m1)
    True
    >>> n
    [1, 2, 4, 5, 5, 5]
    >>> m1
    [1, 5, 5, 5]

    >>> n = [4,3,3,4,2,1]
    >>> m2 = [1,2,3]
    >>> is_included(n, m2)
    True

    >>> m3 = [1,2,6,6]
    >>> is_included(n, m3)
    False
    
    >>> n = [1,5,6,5]
    >>> m3 = [5,6,5,1,1,1]
    >>> is_included(n, m3)
    False
    """
    
    # To create a copy of the lists taken as input
    n_copy = n[:]    
    m1_copy = m1[:]
    
    # To check if m1_copy is a subset of n_copy
    for element in m1_copy:
        if element not in n_copy:
            return False
        else:
            n_copy.remove(element)
    
    return True
    
    

 
def get_difference(n, m1):    
    """
    (list, list) -> list

    This function takes as input two lists of integers and returns a list that,
    if added to the second one, would result in a list identical as the first one

    >>> get_difference([5,5,5,4,2,1], [5,5])
    [5, 4, 2, 1]

    >>> get_difference([1,2,1,3], [1,3])
    [2, 1]
    
    >>> get_difference([1,2,4,5,5,5], [1,3])
    []
   
    >>> get_difference([5,5], [5,5,6,2,4])
    []
    """
    
    # To create a copy of the lists taken as input
    n_copy = n[:]
    m1_copy = m1[:]
    
    empty_list = []
    
    # To iterate through the elements of the lists
    for x in m1_copy:
        for y in n_copy:
            
            # If both elements compared are identical, the element is removed from int
            if x == y:
                n_copy.remove(y)
                break
    
    # If both elements compared are different, an empty_list is returned
    if x != y:
        return empty_list
    
    return n_copy

    
 
    
    

    
    
    
    
      
    

    
    
    
    
    
    
    
    
    
        
        
        
        
        