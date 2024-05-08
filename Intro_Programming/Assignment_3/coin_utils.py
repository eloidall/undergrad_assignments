# Author: Éloi Dallaire
# McGill ID: 260794674

import random
import doctest
from coins import *

# Global Variables
ALPHABET = 'qwertyuiopasdfghjklzxcvbnm1234567890äéèçæœ'
PUNCTUATION = '`~!@#$%^&*()-=_+[]\{}|;\':",./<>? \t\n\r'
ALL_CHARACTERS = ALPHABET + PUNCTUATION
MIN_BASE10_COIN = 0
MAX_BASE10_COIN = 16777215
LETTERS_IN_POPULARITY_ORDER = ' EOTARNLISMHDYFGCWPUBVXK.,\'"-;'


def get_random_comp202coin(index):
    """ (Any) -> str

    This function takes a useless argument and return
    a random integer within the BASE10_COIN limits.

    >>> random.seed(1338)
    >>> get_random_comp202coin(0)
    '0cPMO2C2C0'
    
    >>> random.seed(25)
    >>> get_random_comp202coin(0)
    '0cI0200MIO'
    
    >>> random.seed(125)
    >>> get_random_comp202coin(0)
    '0cON0P000P'
    """
    amt_in_base10 = random.randint(MIN_BASE10_COIN, MAX_BASE10_COIN)
    return base10_to_202(amt_in_base10)


def get_random_character(index):
    """ (Any) -> str

    This function takes a useless argument and
    return a random string from ALL_CHARACTERS.

    >>> random.seed(1338)
    >>> get_random_character(0)
    '!'
    
    >>> random.seed(125)
    >>> get_random_character(0)
    '6'
    
    >>> random.seed(25)
    >>> get_random_character(0)
    '%'
    """
    return ALL_CHARACTERS[random.randint(0, len(ALL_CHARACTERS)-1)]


def get_letter_of_popularity_order(index):
    """ (int) -> str

    This function takes as input a non-negative integer index and returns
    the character of that index in the string LETTERS_IN_POPULARITY_ORDER.

    >>> get_letter_of_popularity_order(5)
    'R'

    >>> get_letter_of_popularity_order(5255)
    '5255'

    >>> get_letter_of_popularity_order(8)
    'I'
    
    >>> get_letter_of_popularity_order(-77)
    Traceback (most recent call last):
    AssertionError: the input must be a non-negative integer
    
    >>> get_letter_of_popularity_order('apple')
    Traceback (most recent call last):
    AssertionError: the input must be a non-negative integer
    """
    # Input validation    
    if type(index) != int or index < 0:
        raise AssertionError("the input must be a non-negative integer")
    if index > len(LETTERS_IN_POPULARITY_ORDER)-1:
        return str(index)
    # To return the appropriate character 
    else:
        return LETTERS_IN_POPULARITY_ORDER[index]


def get_unique_elements(my_list):
    """ (list) -> list

    This function takes as input a list and returns a
    list containing all the unique element of the list.  

    >>> get_unique_elements([1, 4, 5, 1])
    [1, 4, 5]

    >>> get_unique_elements(['ggglll', 'ggglll', 4, 'abc'])
    ['ggglll', 4, 'abc']

    >>> get_unique_elements(['bbb', 2, 89.88, 'ppp','bbb'])
    ['bbb', 2, 89.88, 'ppp']
    
    >>> get_unique_elements(2222)
    Traceback (most recent call last):
    AssertionError: the input must be of type list
    """
    # Input Validation
    if type(my_list) != list:
        raise AssertionError("the input must be of type list")

    # To create a copy of the list taken as input
    my_list_copy = my_list[:]
    
    # To initialize the output list
    unique_elements = []
    for e in my_list_copy:
        if e not in unique_elements:
            unique_elements.append(e)
    return unique_elements


def get_all_coins(text):
    """ (str) -> list

    This function takes as input a string and returns
    a list with all the occurence of COMP202COIN.

    >>> get_all_coins('0c0MPNN0OC-0cM0OCCIOI-0c0MPNN0OC')
    ['0c0MPNN0OC', '0cM0OCCIOI', '0c0MPNN0OC']

    >>> get_all_coins('0cON0P000Ppk0292901021 012901 10cPMO0C2C0IIOMM0qq 9090')
    ['0cON0P000P', '0cPMO0C2C0']

    >>> get_all_coins('Ppk0292901021 012901 1qq 9090')
    ['']
    
    >>> get_all_coins(5555)
    Traceback (most recent call last):
    AssertionError: the input must be of type string
    """
    # Input validation
    if type(text) != str:
            raise AssertionError("the input must be of type string")
    # To create a copy of the string taken as input
    text_copy = text
    
    # To retrieve all valid_COMP202COIN
    valid_COMP202COIN = []
    # To iterate through the elements of the string
    i = 0
    while i < len(text): 
        # To create a 10-character string
        char10_ = text[i:(i+10)]
        # If valid
        if is_base202(char10_):
            valid_COMP202COIN.append(char10_)
            # To skip the already used characters
            i += 10
        else:
            i += 1
    # To return an empty string if the list is empty        
    if len(valid_COMP202COIN) == 0:
        return ['']
    return valid_COMP202COIN


def reverse_dict(my_dict):
    """ (dict) -> dict

    This function takes as input a dictionary and returns
    the dictionary with the values and keys swapped.

    >>> reverse_dict({'a': 52, 'b': 23, 'd': 4})
    {52: 'a', 23: 'b', 4: 'd'}

    >>> reverse_dict({'a': 25, 'b': 25, 'c': 8, 'd': 78})
    Traceback (most recent call last):
    AssertionError: the dictionary had duplicate values
    
    >>> reverse_dict([2, 0, 99, 'snoopy'])
    Traceback (most recent call last):
    AssertionError: the input must be of type dictionary

    >>> reverse_dict({'a': [1, 2, 3, 4], 'b': 25, 'c': {'a': 1, 'b': 2}, 'd': 78})
    Traceback (most recent call last):
    AssertionError: the input dictionary must have immutable values
    """
    # To create a copy of the dictionary taken as input
    my_dict_copy = my_dict
    # Input validation
    if type(my_dict_copy) != dict:
            raise AssertionError("the input must be of type dictionary")
    for v in my_dict_copy.values():
        if type(v) == (list or dict):
            raise AssertionError("the input dictionary must have immutable values")
    
    # To create the final dictionary with swapped key-values 
    output_dict = {}
    for k, v in my_dict_copy.items():
        output_dict[v] = k
    # To raise AssertionError if there was duplicate values
    if len(output_dict) != len(my_dict_copy):
        raise AssertionError("the dictionary had duplicate values")
    
    return output_dict
   
   
def get_frequencies(my_list):
    """ (list) -> dict

    This function takes as input a list and returns a dictionary with
    each key and value respectively represented by the element of the list
    and the corresponding percentage of that element in the list.

    >>> get_frequencies(['a', 'b', 'c'])
    {'a': 0.3333333333333333, 'b': 0.3333333333333333, 'c': 0.3333333333333333}

    >>> get_frequencies([22, 'p', 55, 'p'])
    {22: 0.25, 'p': 0.5, 55: 0.25}

    >>> get_frequencies([1,1,1,1,1])
    {1: 1.0}

    >>> get_frequencies(23435)
    Traceback (most recent call last):
    AssertionError: the input must be of type list
    """
    # Input Validation
    if type(my_list) != list:
        raise AssertionError("the input must be of type list")
     
    # To create a copy of the list taken as input
    my_list_copy = my_list[:]
    
    # To create a dict with occurence of each keys as values
    converted_dict = {}
    for e in my_list_copy:
        if e in converted_dict:
            converted_dict[e] += 1
        else:
            converted_dict[e] = 1
    # To update every values with the proportion of each value in the initial list
    for k in converted_dict:
        converted_dict[k] = converted_dict[k] / len(my_list_copy)
    
    return converted_dict
  
  
def sort_keys_by_values(my_dict):
    """ (dict) -> list

    This function takes as input a dictionary with numbers as values and
    returns a list of the keys sorted in descending order by their values.

    >>> sort_keys_by_values({'mmm': 5, 'zzz': 5, 'abc': 5})
    ['zzz', 'mmm', 'abc']

    >>> sort_keys_by_values({'ee': 152, 'ff': 5698, 'gg': 88})
    ['ff', 'ee', 'gg']

    >>> sort_keys_by_values({'ee': 12, 'ff': -988, 'gg': 12})
    ['gg', 'ee', 'ff']

    >>> sort_keys_by_values({'ee': 'a', 'ff': 45, 'gg': 'c'})
    Traceback (most recent call last):
    AssertionError: the input dictionary values must be numerical
    
    >>> sort_keys_by_values(20202)
    Traceback (most recent call last):
    AssertionError: the input must be of type dict
    
    >>> sort_keys_by_values({'ee': 12, 'ff': -988, 55: 12})
    Traceback (most recent call last):
    AssertionError: all keys mapping to the same values must be of same type
    """
    # Input Validation
    if type(my_dict) != dict:
        raise AssertionError("the input must be of type dict")
    # Assertion Error
    for v in my_dict.values():
        if type(v) != int and type(v) != float:
            raise AssertionError("the input dictionary values must be numerical")
        
    # To create a copy of the dictionary taken as input
    my_dict_copy = my_dict
    
    # To create a dictionary where the keys and values are swapped
    reversed_dict = {}
    for k, v in my_dict_copy.items():
        if v in reversed_dict:
            reversed_dict[v] += [k]
        else:
            reversed_dict[v] = [k]
            
    # To sort in descending order by keys (initial values)
    reversed_sorted_dict = {}
    while len(reversed_dict) != 0:
        for k, v in list(reversed_dict.items()):
            if k == max(reversed_dict):
                reversed_sorted_dict[k] = v
                reversed_dict.pop(k)
    
    # To sort in descending order when there's more than one values mapping to the same key
    for v in reversed_sorted_dict.values():
        if len(v) > 1:
            for sub_values in v:
                if type(sub_values) != type(v[0]):
                    raise AssertionError("all keys mapping to the same values must be of same type")
            v.sort()
            v[:] = v[::-1]        
    
    # To return the final output list
    output_list = []
    for v in reversed_sorted_dict.values():
        output_list += v
    return output_list

                    
def swap_letters(s, letter1, letter2):
    """ (str, str, str) -> str

    This function takes as input three strings where the two last
    one are only one character. It returns a string where all occurence
    of the letter1 are swapped by the occurence of the letter2

    >>> swap_letters("ABCDEF abcdef", 'a', 'f')
    'ABCDEF fbcdea'

    >>> swap_letters("ABCDEF abcdef", 'y', 'z')
    'ABCDEF abcdef'

    >>> swap_letters("1223 aaacc bbbCC d", '2', 'C')
    '1CC3 aaacc bbb22 d'

    >>> swap_letters([1, 2, 4], '2', 'c')
    Traceback (most recent call last):
    AssertionError: all the inputs must be of type string

    >>> swap_letters("1223 aaa bbbcc d", 'bc', 'a')
    Traceback (most recent call last):
    AssertionError: the last two inputs must be single string character
    """
    # Input Validation
    if (type(s), type(letter1), type(letter2)) != (str, str, str):
        raise AssertionError("all the inputs must be of type string")
    if (len(letter1), len(letter2)) != (1, 1):
        raise AssertionError("the last two inputs must be single string character")
    
    # To create a copy of the first string 
    s_copy = s
    
    # To return the updated string
    final_string = ''
    for e in s_copy:
        if e == letter1:
            final_string += letter2
            continue
        if e == letter2:
            final_string += letter1
            continue
        else:
            final_string += e
    return final_string  
       

def get_pct_common_words(text, common_words_filename):
    """ (str, str) -> float

    This function takes as input two strings and returns the percentage of
    characters from the first string that are part of common_words.txt.

    >>> s = "The quick brown fox jumps over the lazy dog."
    >>> get_pct_common_words(s, 'common_words.txt')
    0.22727272727272727
 
    >>> s1 = "Me, myself and I."
    >>> get_pct_common_words(s1, 'common_words.txt')
    0.6470588235294118
    
    >>> s3 = "1721726 ssss 2919191 11 %%%^^^^"
    >>> get_pct_common_words(s3, 'common_words.txt')
    0.0
    
    >>> s4 = [1, 2, 3, 4]
    >>> get_pct_common_words(s4, 'common_words.txt')
    Traceback (most recent call last):
    AssertionError: the first input must be of type string
    
    >>> s5 = ''
    >>> get_pct_common_words(s5, 'common_words.txt')
    Traceback (most recent call last):
    AssertionError: the first input must contain at least one character
    """
    # Input Validation
    if type(text) != str:
        raise AssertionError("the first input must be of type string")   
    if len(text) == 0:
        raise AssertionError("the first input must contain at least one character")
    
    # To create a copy of the first string 
    text_copy = ''
    # To make all punctuation signs identical
    for e in text:
        if e in PUNCTUATION:
            text_copy += '+'  
        else:
            text_copy += e
    
    # To create a list with every words and to remove any ''
    text_copy = text_copy.split('+')
    text_words = []
    for e in text_copy:
        if len(e) != 0:
            text_words.append(e)
    
    # To lower all charcaters of the words
    text_words_lower = []
    for word in text_words:
        text_words_lower.append(word.lower())
        
    # To check membership of words in common_words.txt      
    char_count = 0
    fobj = open(common_words_filename, 'r')
    text_file = fobj.read().strip().split()
    
    for word in text_words_lower:
        if word in text_file:
            char_count += len(word)
    fobj.close()
    
    return char_count / len(text)
    

if __name__ == '__main__':
    doctest.testmod()




