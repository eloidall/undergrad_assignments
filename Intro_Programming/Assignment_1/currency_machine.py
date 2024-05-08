#Author: Éloi Dallaire
#McGill ID: 260794674

#A program simulates a virtual currency machine on planet Orion IX


SUN1_SET = False
SUN2_SET = True
SOLAR_OBSERVATION_FEE_MULTIPLIER = 0.05
COMP202_FLAT_FEE = 10
COMP202COIN_DOLLAR_EXCHANGE_RATE = 0.05
DOLLAR_COMP202COIN_EXCHANGE_RATE = 0.01
COMP202COIN_SUPPLY = "64"

def display_welcome_menu():
    """
    () -> NoneType
    This function displays the currency machine welcome menu and offers the user with 3 available options
    >>> display_welcome_menu()
    Welcome to the Orion IX COMP202COIN virtual exchange machine. 
     Available options: 
     1. Convert dollars into COMP202COIN 
     2. Convert COMP202COIN into dollars 
     3. Exit program
    """
    print("Welcome to the Orion IX COMP202COIN virtual exchange machine."
    "\n Available options:"
    "\n 1. Convert dollars into COMP202COIN"
    "\n 2. Convert COMP202COIN into dollars \n 3. Exit program")



def convert_dollar_to_COMP202COIN(amount_of_dollars):
    """
    num -> num
    
    This function uses the DOLLAR_COMP202COIN_EXCHANGE_RATE to convert an amount_of_dollars
    as input and to return an amount_of_COMP202COIN
    
    DOLLAR_COMP202COIN_EXCHANGE_RATE = 0.01
    >>> convert_dollar_to_COMP202COIN(2000)
    20.0
    >>> convert_dollar_to_COMP202COIN(25)
    0.25
    >>> convert_dollar_to_COMP202COIN(152.25)
    1.52
    """
    amount_of_COMP202COIN = float(amount_of_dollars) * DOLLAR_COMP202COIN_EXCHANGE_RATE
    return amount_of_COMP202COIN


def operation_availability(amount_of_COMP202COIN):
    """
    num -> num
    This function will check if the currency machine is able to convert the dollar amount requested in COMP202COIN

    DOLLAR_COMP202COIN_EXCHANGE_RATE = 0.01
    COMP202COIN_SUPPLY = "64"
    >>> operation_availability(458.52)
    1
    >>> operation_availability(25)
    1
    >>> operation_availability(178)
    0
    """
    #The program will check if the transaction can be completed and will terminate if
    #the amount to convert is to small or to big
    
    if amount_of_COMP202COIN < 1:
        return 0
    elif amount_of_COMP202COIN > int(COMP202COIN_SUPPLY,16):
        return 2
    else:
        return 1




def get_excess_dollars_after_conversion(amount_of_dollars):
    """
    num -> num
    This function takes as input an amount of dollars and returns the amount of dollars that will be returned to the user
    after the program rounded the conversion into COMP202COIN
    
    DOLLAR_COMP202COIN_EXCHANGE_RATE = 0.01
    >>> get_excess_dollars_after_conversion(156.25)
    56.25
    >>> get_excess_dollars_after_conversion(2545)
    45.0
    >>> get_excess_dollars_after_conversion(11001)
    1.00
    """
    
    #Computes the difference between the conversion from dollars to COMP202COIN with and without rounding down
    amount_of_COMP202COIN = convert_dollar_to_COMP202COIN(amount_of_dollars)
    rounded_amount_of_COMP202COIN = int(convert_dollar_to_COMP202COIN(amount_of_dollars))
    
    excess_COMP202COIN_after_conversion = amount_of_COMP202COIN - rounded_amount_of_COMP202COIN
    
    #Re-converts the COMP202COIN in excess in a dollar amount
    excess_dollars_after_conversion = excess_COMP202COIN_after_conversion / DOLLAR_COMP202COIN_EXCHANGE_RATE
    return round(excess_dollars_after_conversion,2)
 

def get_solar_observation_fee(amount_of_comp202coin):

    """
    str -> num
    This function uses the amount_of_comp202coin to return the solar_observation_fee to apply to the transaction
    
    SUN1_SET = False
    SUN2_SET = True
    SOLAR_OBSERVATION_FEE_MULTIPLIER = 0.05
    >>> get_solar_observation_fee("cd140")
    0
    
    SUN1_SET = True
    SUN2_SET = False
    SOLAR_OBSERVATION_FEE_MULTIPLIER = 0.05
    >>> get_solar_observation_fee("4d1")
    0
    
    SUN1_SET = False
    SUN2_SET = False
    SOLAR_OBSERVATION_FEE_MULTIPLIER = 0.05
    >>> get_solar_observation_fee("ba57")
    0
    
    SUN1_SET = True
    SUN2_SET = True
    SOLAR_OBSERVATION_FEE_MULTIPLIER = 0.05
    >>> get_solar_observation_fee("ff3")
    204.15
    """
    #Checks values of SUN1_SET and SUN2_SET to determine the value of SOLAR_OBSERVATION_FEE_MULTIPLIER and compute solar_observation_fee
    if (SUN1_SET == False) or (SUN2_SET == False):
        solar_observation_fee = 0
        return solar_observation_fee
    else:
        solar_observation_fee = SOLAR_OBSERVATION_FEE_MULTIPLIER * int(amount_of_comp202coin,16)
        return solar_observation_fee


def get_flat_fee():
    """
    () -> num
    This function simply retrieves the flat_fee as the global variable
    
    COMP202_FLAT_FEE = 10
    >>> get_flat_fee()
    10
    """
    
    flat_fee = COMP202_FLAT_FEE
    return flat_fee


def convert_COMP202COIN_to_dollars(amount_of_comp202coin):
    """
    str -> num
    This function takes as input the amount_of_comp202coin as a string containing a integer in base 16
    and converts it in the amount of dollars the user will receive after applying the appropriate fees

    >>> convert_COMP202COIN_to_dollars("4d3")
    51.75
    >>> convert_COMP202COIN_to_dollars("aa")
    -1.5
    >>> convert_COMP202COIN_to_dollars("455")
    45.45
    """
    amount_of_dollars = (int(amount_of_comp202coin, 16) * COMP202COIN_DOLLAR_EXCHANGE_RATE) - get_solar_observation_fee(amount_of_comp202coin)- get_flat_fee()
    return amount_of_dollars




#This function is the final one that would make the whole currency machine process the user's inquiries

def operate_machine():
    """
    () -> NoneType
    This function operates a currency machine that lets the user convert both dollars or COMP202COIN
    
    >>> operate_machine()
    Welcome to the Orion IX COMP202COIN virtual exchange machine.
    Available options:
    1. Convert dollars into COMP202COIN
    2. Convert COMP202COIN into dollars
    3. Exit program
    > 1
    Enter the amount of dollars to convert: 179
    You have deposited 179.0 dollars. You will receive 0x1 COMP202COIN,
    and 79.0 dollars will be returned to you.
    
    >>> operate_machine()
    Welcome to the Orion IX COMP202COIN virtual exchange machine.
    Available options:
    1. Convert dollars into COMP202COIN
    2. Convert COMP202COIN into dollars 
    3. Exit program
    > 1
    Enter the amount of dollars to convert: 75000
    Your transaction cannot be completed due to insufficient funds.
    
    >>> operate_machine()
    Welcome to the Orion IX COMP202COIN virtual exchange machine.
    Available options:
    1. Convert dollars into COMP202COIN
    2. Convert COMP202COIN into dollars 
    3. Exit program
    > 1
    Enter the amount of dollars to convert: 67
    Your transaction cannot be completed. Please select a greater amount of dollars to convert.
    
    >>> operate_machine()
    Welcome to the Orion IX COMP202COIN virtual exchange machine.
    Available options:
    1. Convert dollars into COMP202COIN
    2. Convert COMP202COIN into dollars 
    3. Exit program
    > 2
    Enter the amount of COMP202COIN to convert: ad5
    You have deposited ad5 COMP202COIN. You will receive 128.65 dollars.
    """
    
    display_welcome_menu()
    
    #The user will first input the type of operation desired
    first_input = int(input("> "))

    #If option 1 is chosen, the program will ask the user to input the dollar amount that he wishes to convert in COMP202COIN
    if first_input == 1:
        amount_of_dollars = float(input("Enter the amount of dollars to convert: "))
        
        #The dollar amount inputed will be converted into COMP202COIN
        amount_of_COMP202COIN = convert_dollar_to_COMP202COIN(amount_of_dollars)
        
        #The program will verify that the currency machine is able to process the requested dollar amount
        #The program will terminate if it cannot process it
        if operation_availability(amount_of_COMP202COIN) == 0:
            print("Your transaction cannot be completed. Please select a greater amount of dollars to convert.")
            return
        elif operation_availability(amount_of_COMP202COIN) == 2:
            print("Your transaction cannot be completed due to insufficient funds.")
            return
        
        #If the program can process the operation, it will compute the amount of COMP202COIN and dollars to return to the user
        else:
            #To compute the rounded down amoun of COMP202COIN
            converted_COMP202COIN = int(convert_dollar_to_COMP202COIN(amount_of_dollars))
            
            #To get the amount of dollars to returned
            dollars_returned = get_excess_dollars_after_conversion(amount_of_dollars)
            
            #To display the result
            print("You have deposited", amount_of_dollars, "dollars. You will receive", hex(converted_COMP202COIN), "COMP202COIN,"
                  "\nand", dollars_returned, "dollars will be returned to you.")
            
        
    #If option 2 is chosen, the program will ask the user to input the COMP202COIN amount that he wishes to convert in dollars
    elif first_input == 2:
        amount_of_comp202coin = input("Enter the amount of COMP202COIN to convert: ")
        
        #The program will convert this amount in dollars by applying the appropriate fees
        amount_of_dollars = convert_COMP202COIN_to_dollars(amount_of_comp202coin)
        
                
        #If the net amount to receive is negative, the program will not process it and will inform the user before terminating
        if amount_of_dollars <= 0:
            print("Your transaction cannot be completed. Please select a greater amount of COMP202COIN to convert.")
        
        #The program will display the amount of dollars the user will receive
        else:
            print("You have deposited", amount_of_comp202coin, "COMP202COIN. You will receive", round(amount_of_dollars,2),"dollars.")     
     
     
    #If option 3 is chosen, the program will terminate
    elif first_input == 3:
        return



        

        


        


    
    
    
    