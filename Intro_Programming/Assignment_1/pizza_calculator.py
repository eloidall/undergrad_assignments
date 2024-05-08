#Author: Éloi Dallaire
#McGill ID: 260794674

# A program that __________

import math


def display_welcome_menu():
    """
    () -> NoneType
    This function displays the pizza calculator welcome menu and offers the user with the 2 available modes
    
    >>> display_welcome_menu()
    Welcome to the COMP 202 fair pizza calculator!
    Please choose one of the following modes:
    A. "Quantity mode"
    B. "Price mode"
    """
    
    print("Welcome to the COMP 202 fair pizza calculator!"
    "\nPlease chose one of the following modes:"
    "\nA." """ "Quantity mode" """
    "\nB." """ "Price mode" """)

def get_area_large_pizza(diameter_large_pizza):
    """
    num -> num
    This function computes the area of a large pizza

    >>> get_area_large_pizza(16)
    201.06192982974676
    >>> get_area_large_pizza(14)
    153.93804002589985
    >>> get_area_large_pizza(24)
    452.3893421169302
    """
    
    area_large_pizza = math.pi * (diameter_large_pizza/2)**2
    return area_large_pizza


def get_area_small_pizza(diameter_small_pizza):
    """
    num -> num
    This function computes the area of a small pizza

    >>> get_area_small_pizza(6)
    28.274333882308138
    >>> get_area_small_pizza(9)
    63.61725123519331
    >>> get_area_small_pizza(11)
    95.03317777109125
    """
    
    area_small_pizza = math.pi * (diameter_small_pizza/2)**2
    return area_small_pizza




def get_fair_quantity_in_order(diameter_large_pizza, diameter_small_pizza):
    """
    (num, num) -> num
    This function will compute the fair quantity of small pizzas only by taking as inputs
    the diameter of the large pizza first and the diameter of the small pizza second

    >>> get_fair_quantity_in_order(16,4)
    16
    >>> get_fair_quantity_in_order(24,11)
    5
    >>> get_fair_quantity_in_order(9,5)
    4
    """

    number_small_pizza = 1
    while (number_small_pizza * get_area_small_pizza(diameter_small_pizza)) < get_area_large_pizza(diameter_large_pizza):
        number_small_pizza += 1
    return number_small_pizza





def get_fair_quantity(diameter_pizza1, diameter_pizza2):
    """
    num -> num
    This function compute minimum number of small pizza to order to get at least the same amount as on a large pizza
    
    >>> get_fair_quantity(20,7)
    9
    >>> get_fair_quantity(10,24)
    6
    >>> get_fair_quantity(24,10)
    6
    """
    #To determine which of the pizza1 or pizza2 is the large pizza
    if diameter_pizza1 >= diameter_pizza2:
        
        #To assign pizza1 and pizza2 to their appropriate and relative size
        diameter_large_pizza = diameter_pizza1
        diameter_small_pizza = diameter_pizza2
        
        #To recall the area of the pizzas
        area_large_pizza = get_area_large_pizza(diameter_large_pizza)   
        area_small_pizza = get_area_small_pizza(diameter_small_pizza)
        
        #To compute the fair quantity
        return get_fair_quantity_in_order(diameter_large_pizza, diameter_small_pizza)
    
    else:
        #To assign pizza1 and pizza2 to their appropriate and relative size
        diameter_large_pizza = diameter_pizza2
        diameter_small_pizza = diameter_pizza1
        
        #To recall the area of the pizzas
        area_large_pizza = get_area_large_pizza(diameter_large_pizza)   
        area_small_pizza = get_area_small_pizza(diameter_small_pizza)
        
        #To compute the fair quantity
        return get_fair_quantity_in_order(diameter_large_pizza, diameter_small_pizza)



def get_fair_price(diameter_large_pizza, price_large_pizza, diameter_small_pizza, number_small_pizza):
    """
    (num, float, num, num) -> num
    This function compute the fair price the user should pay for small pizzas in order
    to have the same amount of pizza per dollar than for the large pizza
    
    >>> get_fair_price(22,27.56,12,2)
    16.4
    >>> get_fair_price(16,14.99,9,3)
    14.23
    >>> get_fair_price(18,22.49,7,4)
    13.61
    """

    #To compute the amount of large pizza per dollar
    large_pizza_area_per_dollar = get_area_large_pizza(diameter_large_pizza) / price_large_pizza
    
    #To compute the total amount for small pizzas
    area_small_pizza = get_area_small_pizza(diameter_small_pizza)
    
    #To compute the total price the user should pay for small pizzas in order to have the same amount of pizza per dollar for both sizes
    fair_price_small_pizzas = (area_small_pizza / large_pizza_area_per_dollar) * number_small_pizza
    
    return round(fair_price_small_pizzas, 2)
    
    


def run_pizza_calculator():
    
    """
    () -> NoneType
    This function operates a pizza calculator that lets the user know how many small pizzas should he buy to be satisifed
    or how much should he pay for a specified number of small pizzas

    
    >>> run_pizza_calculator()
    Welcome to the COMP 202 fair pizza calculator!
    Please chose one of the following modes:
    A. "Quantity mode" 
    B. "Price mode" 

    Enter your choice: A

    You selected "Quantity mode" 

    Enter the diameter of the large pizza: 19
    Enter the diameter of the small pizza: 5
    To be fully satisfied you should order 15 small pizzas
    >>> run_pizza_calculator()
    Welcome to the COMP 202 fair pizza calculator!
    Please chose one of the following modes:
    A. "Quantity mode" 
    B. "Price mode" 

    Enter your choice: A

    You selected "Quantity mode" 

    Enter the diameter of the large pizza: 12
    Enter the diameter of the small pizza: 10
    To be fully satisfied you should order 2 small pizzas
    >>> run_pizza_calculator()
    Welcome to the COMP 202 fair pizza calculator!
    Please chose one of the following modes:
    A. "Quantity mode" 
    B. "Price mode" 

    Enter your choice: B

    You selected "Price mode" 

    Enter the diameter of the large pizza: 24
    Enter the price of the large pizza: 45.25
    Enter the diameter of the small pizza: 12
    Enter the number of small pizzas you'd like to buy: 3

    The fair price to pay for 3 small pizzas is $33.94    
    
    >>> run_pizza_calculator()
    Welcome to the COMP 202 fair pizza calculator!
    Please chose one of the following modes:
    A. "Quantity mode" 
    B. "Price mode" 

    Enter your choice: B

    You selected "Price mode" 

    Enter the diameter of the large pizza: 14
    Enter the price of the large pizza: 18.55
    Enter the diameter of the small pizza: 9
    Enter the number of small pizzas you'd like to buy: 2

    The fair price to pay for 2 small pizzas is $15.33
    
    >>> run_pizza_calculator()
    Welcome to the COMP 202 fair pizza calculator!
    Please chose one of the following modes:
    A. "Quantity mode" 
    B. "Price mode" 

    Enter your choice: a
    This mode is not supported
    """
    display_welcome_menu()
    
    #The user will first input the mode desired
    first_input = str(input("\nEnter your choice: "))
    
    #If mode A is selected, the program will run the "Quantity mode" and will retrieve two integer as input from the user
    #that represent the diameter of the large and small pizza
    if first_input == "A":
        print("\nYou selected" """ "Quantity mode" """)
        
        diameter_large_pizza = int(input("\nEnter the diameter of the large pizza: "))
        diameter_small_pizza = int(input("Enter the diameter of the small pizza: "))
        
        #The program will display the number of small pizzas the user
        #should get to have at least the same amount of pizza as one large pizza      
        print("To be fully satisfied you should order", get_fair_quantity(diameter_large_pizza, diameter_small_pizza), "small pizzas")
        
    
    #If mode B is selected, the program will run the "Price mode" and will retrieve rspectively the
    #diameter and the price of the larger pizza and the diameter and the amount desired of small pizzas
    elif first_input == "B":
        print("\nYou selected" """ "Price mode" """)
        
        diameter_large_pizza = int(input("\nEnter the diameter of the large pizza: "))
        price_large_pizza = float(input("Enter the price of the large pizza: "))
        
        diameter_small_pizza = int(input("Enter the diameter of the small pizza: "))
        number_small_pizza = int(input("Enter the number of small pizzas you'd like to buy: "))
    
        #To display the fair price
        print("\nThe fair price to pay for", number_small_pizza, "small pizzas is $"
              +str(get_fair_price(diameter_large_pizza, price_large_pizza, diameter_small_pizza, number_small_pizza)))
    
    
    
    #If any other mode is selected, the user will be informed that its selected mode is not supported and the program will terminate   
    else:
        print("This mode is not supported")
        return
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


