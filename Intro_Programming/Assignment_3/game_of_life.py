# Author: Éloi Dallaire
# McGill ID: 260794674

import doctest

def create_deep_copy_list(my_list):
    """(list) -> list

    This function takes as input a 2D list and returns a deep copy of that list.

    >>> create_deep_copy_list([[1, 1, 2], [2, 0, 0], [1, 2]])
    [[1, 1, 2], [2, 0, 0], [1, 2]]

    >>> create_deep_copy_list([[1], [2], [0]])
    [[1], [2], [0]]

    >>> create_deep_copy_list([[22, 2], [0], []])
    [[22, 2], [0], []]
    """
    my_list_copy = []
    
    # To create copies of each sublist
    for sublist in my_list:
        new_sublist = []
        # To add every element in the new sublist
        for element in sublist:
            new_sublist.append(element) 
        my_list_copy.append(new_sublist)
    
    return my_list_copy


def is_valid_universe(matrice):
    """(list) -> bool
    
    This function returns True if the input is a valid representation of a universe.
    It returns False if the input is not a matrice and if it contains elements
    different from 0s and 1s.
    
    >>> a = [[0, 0, 1], [1, 0, 1], [1, 2, 3], [4, 5, 0]]
    >>> is_valid_universe(a)
    False
    
    >>> b = [[1, 1], [0, 0], [0, 1]]
    >>> is_valid_universe(b)
    True
    
    >>> c = [[1], [1, 0, 1], [0, 0, 0]]
    >>> is_valid_universe(c)
    False
    """    
    # To retrieve the length of the first sublist 
    length = len(matrice[0])
    
    # To iterate through each sublists
    for rows in matrice[1:]:
        if len(rows) != length:
            return False
        
        # To ensure each sublists strictly contains 0s and 1s
        for elements in rows:
            if elements not in [0,1]:
                return False
    return True


def universe_to_str(valid_universe):
    """ (list) -> str

    This function takes as input a 2D list representing a
    valid universe and returns its string representation

    >>> block = [[0, 0, 0, 0], [0, 1, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0]]
    >>> str_block = universe_to_str(block)
    >>> print(str_block)
    +----+
    |    |
    | ** |
    | ** |
    |    |
    +----+

    >>> block1 = [[1, 0, 1], [0, 1, 0], [1, 0, 1], [0, 1, 0]]
    >>> str_block1 = universe_to_str(block1)
    >>> print(str_block1)
    +---+
    |* *|
    | * |
    |* *|
    | * |
    +---+

    >>> block2 = [[1, 1, 1, 1], [0, 0, 0, 0], [1, 1, 1, 1], [0, 0, 0, 0]]
    >>> str_block2 = universe_to_str(block2)
    >>> print(str_block2)
    +----+
    |****|
    |    |
    |****|
    |    |
    +----+
    """
    # To create a copy of the list taken as input
    valid_universe_copy = create_deep_copy_list(valid_universe)
    # Input validation
    if not is_valid_universe(valid_universe_copy):
        raise ValueError("The input must represent a valid universe.")
   
    # To create a str_list with every element converted in string
    str_list = []
    for sublist in valid_universe_copy:
        new_element = ""
        for element in sublist:
            new_element += str(element)
        str_list.append(new_element)

    # To replace with apropriate symbols
    final_str_list = []
    for element in str_list:
        element = element.replace("0", " ")
        element = element.replace("1", "*")
        element = "|" + element + "|"
        final_str_list.append(element)
                
    universe = "\n".join(final_str_list)
    
    # To create the box surroundings
    box_surroundings = "+" + len(valid_universe_copy[0]) * "-" + "+"
    
    return box_surroundings + "\n" + universe + "\n" + box_surroundings
    

def count_live_neighbors(valid_universe, x, y):
    """ (list, int, int) -> int

    This function takes as input a 2D list representing a valid universe and two integers
    x and y representing the position of a cell in the universe.
    It returns the number of live neighboring cells

    >>> beehive = [[0, 0, 0, 0], \
                   [0, 0, 1, 0], \
                   [0, 1, 0, 1], \
                   [1, 1, 1, 0]]
    >>> count_live_neighbors(beehive, 0, 2)
    1
    >>> count_live_neighbors(beehive, 3, 1)
    3

    >>> beehive = [[1, 0, 1], \
                   [0, 0, 0], \
                   [1, 1, 1], \
                   [1, 1, 1]]
    >>> count_live_neighbors(beehive, 1, 1)
    5
    """
    # To create a copy of the list taken as input
    valid_universe_copy = create_deep_copy_list(valid_universe)
    # Input validation
    if not is_valid_universe(valid_universe_copy):
        raise ValueError("The input must represent a valid universe.")
    
    # To retrive the universe dimensions
    num_of_columns = len(valid_universe_copy[0])
    num_of_rows = len(valid_universe_copy)
        
    neighbors = []
    # To iterate through all the neighboring cells, skipping over it falls out of the universe
    for x1 in range(max(0,x-1), min(num_of_rows, x+2)):
        for y1 in range(max(0, y-1), min(num_of_columns, y+2)):
            # To skip over the (y,y)
            if x == x1 and y == y1:
                continue
            neighbors.append(valid_universe_copy[x1][y1])
            
    # To return the number of live neighboring cells
    return neighbors.count(1)
  
  
def get_next_gen_cell(valid_universe, x, y):
    """ (list, int, int) -> int

    This function takes as input a 2D list representing a valid universe and
    two integers x and y representing the position of a cell in the universe.
    It returns 1 if the cell is alive in the next generation and 0 otherwise. 

    >>> beehive = [[0, 0, 0, 0, 0, 0], \
                   [0, 0, 1, 1, 0, 0], \
                   [0, 1, 0, 0, 1, 0], \
                   [0, 0, 1, 1, 0, 0], \
                   [0, 0, 0, 0, 0, 0]]
    >>> get_next_gen_cell(beehive, 1, 3)
    1

    >>> toad = [[0, 0, 0, 0, 0, 0], \
                [0, 1, 1, 1, 1, 0], \
                [0, 1, 1, 1, 1, 0], \
                [0, 1, 1, 1, 1, 0], \
                [0, 0, 0, 0, 0, 0]]
    >>> get_next_gen_cell(toad, 2, 2)
    0
    >>> get_next_gen_cell(toad, 4, 3)
    1
    """
    # To create a copy of the list taken as input
    valid_universe_copy = create_deep_copy_list(valid_universe)
    # Input validation
    if not is_valid_universe(valid_universe_copy):
        raise ValueError("The input must represent a valid universe.")    
    
    # To account for live cells
    if valid_universe_copy[x][y] == 1:
        if count_live_neighbors(valid_universe_copy, x, y) < 2:
            return 0
        if count_live_neighbors(valid_universe_copy, x, y) > 3:
            return 0
        else:
            return 1

    # To account for dead cells
    if valid_universe_copy[x][y] == 0:
        if count_live_neighbors(valid_universe_copy, x, y) == 3:
            return 1
        else:
            return 0


def get_next_gen_universe(valid_universe):
    """ (list) -> list

    This functions takes as input a 2D list representing a valid universe and
    returns a 2D list representing the universe in its next generation.

    >>> tud = [[1, 1, 1], \
               [0, 0, 0], \
               [0, 0, 0], \
               [1, 1, 1]]
    >>> get_next_gen_universe(tud)          
    [[0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0]]

    >>> beehive = [[0, 1, 1, 0], \
                   [0, 1, 1, 0], \
                   [0, 1, 1, 0], \
                   [0, 1, 1, 0]]
    >>> get_next_gen_universe(beehive)
    [[0, 1, 1, 0], [1, 0, 0, 1], [1, 0, 0, 1], [0, 1, 1, 0]]
    
    >>> pentadec= [[0, 0, 0, 0, 0, 0, 0, 0, 0], \
                   [0, 0, 0, 0, 0, 0, 0, 0, 0], \
                   [0, 0, 0, 0, 0, 0, 0, 0, 0], \
                   [0, 0, 0, 0, 1, 0, 0, 0, 0], \
                   [0, 0, 0, 0, 1, 0, 0, 0, 0], \
                   [0, 0, 0, 1, 0, 1, 0, 0, 0], \
                   [0, 0, 0, 0, 1, 0, 0, 0, 0], \
                   [0, 0, 0, 0, 1, 0, 0, 0, 0], \
                   [0, 0, 0, 0, 1, 0, 0, 0, 0], \
                   [0, 0, 0, 0, 1, 0, 0, 0, 0], \
                   [0, 0, 0, 1, 0, 1, 0, 0, 0], \
                   [0, 0, 0, 0, 1, 0, 0, 0, 0], \
                   [0, 0, 0, 0, 1, 0, 0, 0, 0],\
                   [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    >>> pentadec_gen2 = get_next_gen_universe(pentadec)
    >>> pentadec_gen2[6:9]
    [[0, 0, 0, 1, 1, 1, 0, 0, 0], [0, 0, 0, 1, 1, 1, 0, 0, 0], [0, 0, 0, 1, 1, 1, 0, 0, 0]]
    """
    # To create a copy of the list taken as input
    valid_universe_copy = create_deep_copy_list(valid_universe)
    # Input validation
    if not is_valid_universe(valid_universe_copy):
        raise ValueError("The input must represent a valid universe.")    
    
    # To initialize the final list
    next_gen_universe = create_deep_copy_list(valid_universe)
    
    # To get the next_gen_cell for every cell
    for i, sublist in enumerate(valid_universe_copy):
        for j, cell in enumerate(sublist):  
            next_gen_universe[i][j] = get_next_gen_cell(valid_universe_copy, i, j)

    return next_gen_universe

   
def get_n_generations(valid_universe, n):
    """
    This functions takes as input a 2D list representing a valid universe and an integer n
    and returns a list containing m strings which represents the first m generations of the input.

    >>> beehive = [[0, 1, 1, 0], \
                   [1, 1, 1, 1], \
                   [1, 1, 1, 1], \
                   [0, 1, 1, 0]]
    >>> b = get_n_generations(beehive, 3)
    >>> len(b)
    3
    >>> print(b[1])
    +----+
    |*  *|
    |    |
    |    |
    |*  *|
    +----+
    >>> print(b[2])
    +----+
    |    |
    |    |
    |    |
    |    |
    +----+
    
    >>> toad = [[0, 0, 0, 0, 0, 0], \
                [0, 0, 1, 1, 1, 0], \
                [0, 1, 1, 1, 0, 0], \
                [0, 0, 0, 0, 0, 0]]
    >>> t = get_n_generations(toad, 5)
    >>> len(t)
    2
    >>> print(t[1])
    +------+
    |   *  |
    | *  * |
    | *  * |
    |  *   |
    +------+
    """
    # To create a copy of the list taken as input
    valid_universe_copy = create_deep_copy_list(valid_universe)

    # Input validation
    if type(valid_universe_copy) != list:
        raise TypeError("The first input must be a list.")
    if type(n) != int:
        raise TypeError("The second input must be an integer.")
    
    if not is_valid_universe(valid_universe_copy):
        raise ValueError("The first input must represent a valid universe.")
    if n <= 0:
        raise ValueError("The second input must a positive number greater than 0.")

    # To keep track of the previous generation
    old_generation = valid_universe_copy
    # To initialize the final output with the generation 0
    new_generations = []
    new_generations.append(universe_to_str(valid_universe_copy))
    # To add the next generations in the final output
    for x in range(1, n):
        old_generation = get_next_gen_universe(old_generation)
        new_generations.append(universe_to_str(old_generation))
    
    # To shorten the final output if the period m is reached before n
    for m, generation in enumerate(new_generations[1:]):
        if generation == new_generations[0]:
            new_generations = new_generations[:m+1]
    
    # To return the final generations as a string
    return new_generations
    

if __name__ == '__main__':
    doctest.testmod()
    