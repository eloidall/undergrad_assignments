# Author: Éloi dallaire
# McGill ID: 260794674


#Global Variables
BASE8_CHARS = "01234567"
BASE202_CHARS = "0C2OMPIN"


def base10_to_202(amt_in_base10):
    """
    (int) -> str

    This function takes as input an integer representing an amount in base 10 and
    returns the corresponding amount in base 202 as a a 10-character string

    >>> base10_to_202(1255)
    '0c00002OMN'
    
    >>> base10_to_202(1534)
    '0c00002NNI'
    
    >>> base10_to_202(202)
    '0c00000OC2'
    """
    
    # To convert the amount in base 8
    amt_in_base8 = oct(amt_in_base10)
    
    # To remove the two first characters
    amt_in_base8 = amt_in_base8[2:]
    
    # To replace by the appropriate characters from BASE202_CHARS
    for x in amt_in_base8:
        if x not in BASE202_CHARS:
            index = BASE8_CHARS.find(x)
            amt_in_base8 = amt_in_base8.replace(x, BASE202_CHARS[index])
            
    # To add the missing 0 characters
    missing_zero = 8 - len(amt_in_base8)
    for x in range(missing_zero):
        amt_in_base8 = "0" + amt_in_base8
        
    # To return a 10-character string starting with 0c
    amt_in_base8 = "0c" + amt_in_base8
    return amt_in_base8



def base202_to_10(amt_in_base202):
    """
    (str) -> int

    This function takes as input a string representing an amount in base 202
    and returns the corresponding amount in base 10 as an integer
    
    >>> base202_to_10("0c0022MmIn")
    76087
    
    >>> base202_to_10("0C00000cc0")
    72
    
    >>> base202_to_10("0c00000OC2")
    202
    """
    
    amt_in_base202 = amt_in_base202.upper()
    
    # To remove the first two characters 0 and c
    amt_in_base202 = amt_in_base202[2:]
  
    # To replace by the appropriate characters from BASE8_CHARS
    for x in amt_in_base202:
        if x not in BASE8_CHARS:
            index = BASE202_CHARS.find(x)
            amt_in_base202 = amt_in_base202.replace(x, BASE8_CHARS[index])
    
    # To remove the remaining 0 at the begining
    while amt_in_base202[0] == "0":
        amt_in_base202 = amt_in_base202[1:]
    
    # To return an integer in base 10
    return int(amt_in_base202,8)
   
   
    
def is_base202(text):
    """
    (str) -> bool

    This function takes as input a string of any length or characters
    and returns True if it is a valid 10-character COMP202COIN string
    
    >>> is_base202("0cCMPI00in")
    True
    
    >>> is_base202("0coi125645")
    False
    
    >>> is_base202("0C0MPI00in")
    True
    
    >>> is_base202("11oiCmiOP0")
    False
    
    >>> is_base202("0C0MP")
    False
    
    >>> is_base202("-0C0MPI00in")
    True
    """
    
    # To account for upper and lower cases 
    text = text.upper()
    
    # To account for negative COMP202COIN
    if text[0] == "-" and len(text) == 11:
        text = text[1:]
    
    # To account for all the other needed specifications
    # The lenght need to be 10
    if len(text) != 10:
        return False
    
    # The first two charcaters must be "0c"
    if text[0] != "0" or text[1] != "C":
        return False
    
    # The characters must be a valid one
    for x in text:
        if x not in BASE202_CHARS:
            return False
    else:
        return True
    


def get_nth_base202_amount(text, n):   
    """
    (str, int) -> str

    This function takes as input a string of any length or characters and a non-negative
    integer n and returns the n'th 10-character COMP202COIN substring contained wihtin the string
    
    >>> get_nth_base202_amount("lklokk 0C0000000C poop ", 0)
    '0C0000000C'
    
    >>> get_nth_base202_amount("skldklsd 0C0C0C0C0C 0cMIOPPP00 djkjdk dd0CMiiiMOP0sss",2)
    '0CMIIIMOP0'
    
    >>> get_nth_base202_amount("skldkl sjhdjshdjshdjsd jdhjs dhjshdjshdjsdh j",3)
    ''
    
    >>> get_nth_base202_amount("skldklsdksldk sldk sldksldk sld lsdk l 0c00000CMI popopp p02902390c000Miopo ere ",1)
    '0C000MIOPO'
    """
    
    text = text.upper()
    
    # Input validation    
    if n < 0:
        raise ValueError("the integer must be non-negative")
    
    list_of_valid = []
    
    # To iterate through the elements of the string
    i = 0
    while i < len(text): 
        
        # To store the created 10-character string if valid
        char10_ = text[i:(i+10)]
        if is_base202(char10_):
            list_of_valid.append(char10_)
            
            # To skip the already used characters
            i += 10
        else:
            i += 1
    
    # To display the nth element if available
    if len(list_of_valid) < (n+1):
        return ""
    else:
        return list_of_valid[n]
            
       
       
def get_total_dollar_amount(text):
    """
    (str) -> int

    This function takes as input a string of any length or characters
    and returns the total dollar amount in base 10 of COMP202COIN in the string

    >>> get_total_dollar_amount("lklokk 0C0000000C poop ")
    1
    
    >>> get_total_dollar_amount("skldklsd 0C0C0C0C0C 0cMIOPPP00 djkjdk dd0CMiiiMOP0sss")
    20534377
    
    >>> get_total_dollar_amount("skldklsdksldk sldk sldksldk sld lsdk l 0c00000CMI popopp p02902390c000Miopo ere ")
    19793
    
    >>> get_total_dollar_amount("skldkl sjhdjshdjshdjsd jdhjs dhjshdjshdjsdh j")
    0
    """
    
    total_amount = 0
    n = 0
    while get_nth_base202_amount(text, n) != '':
        total_amount += base202_to_10(get_nth_base202_amount(text, n))
        n += 1
    
    return total_amount



def reduce_amounts(text, limit):
    """
    (str, int) -> str

    This function takes as input string of any length or characters and a non-negative integer limit.
    It returns the orignal string with all the COMP202COIN amounts updated if the total limit was exceeded

    >>> reduce_amounts("skldkl sjhdjshdjshdjsd jdhjs dhjshdjshdjsdh j", 150000)
    'skldkl sjhdjshdjshdjsd jdhjs dhjshdjshdjsdh j'
    
    >>> reduce_amounts("skldklsd 0C0C0C0C0C 0cMIOPPP00 djkjdk dd0CMiiiMOP0sss", 150000)
    'skldklsd 0c0000OIOC 0c002CNIIN djkjdk dd0c0022C2ONsss'
    
    >>> reduce_amounts("0cCCMMPP22      0cOCOCOCOC", 9000000)
    '0cCCOCMCI0      0cO0NOPNCN'
    """
    
    # To find the total account's holding
    total_holdings = get_total_dollar_amount(text)
    
    if total_holdings <= limit:
        return text
        
    else:
        # To compute the percent decrease
        decrease_percentage = (total_holdings - limit) / total_holdings
        final_proportion = 1 - decrease_percentage
        
        text_copy = ""
        
        i = 0
        while len(text) != len(text_copy):
            
            # If the string is a valid COMP202COIN
            if is_base202(text[i:i+10]) == True:
            
                # To find the str to be updated
                str_to_update = text[i:i+10]
                
                # To convert in base 10
                amt_in_base10 = base202_to_10(str_to_update)

                # To decrease by the percentage
                amt_in_base10 = int(amt_in_base10 / (1 / final_proportion))
                
                # To reconvert in base 202
                amt_in_base202 = base10_to_202(amt_in_base10)
                
                # To modify the related string with the updated amount
                text_copy += amt_in_base202
                i += 10
                
            # If the string is not a valid COMP202COIN, simply return it unchanged
            else:
                text_copy += text[i]                
                i += 1
                
        # To return the final updated string    
        return text_copy
    

