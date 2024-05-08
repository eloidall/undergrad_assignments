# Author: Éloi dallaire
# McGill ID: 260794674

import turtle
import random
import math





def draw_square(side_lenght, t):
    """
    (int) -> NoneType
    
    This function draws a square with each side equal to the input
    """
  
    for i in range(4):
        t.fd(side_lenght)
        t.lt(90)
    
    

def draw_circle_of_squares(nums_of_squares, side_lenght, t):
    
    """
    (int, int) -> NoneType

    This function draws multiple squares of given side_lenght each time
    rotated by a specific angle to complete a full circle_of_squares
    """
    
    # To set up the turtle position and color
    t.color("red")
    t.fillcolor("green")
    t.begin_fill()
    
    # To draw the several squares 
    for i in range(nums_of_squares):
        draw_square(side_lenght, t)
        
        # To determine the angle of rotation between each squares
        # to ensure a complete 360 degrees rotation is completed
        t.lt(360/nums_of_squares)
    
    t.end_fill() 
   
   
   
def draw_final_circle(side_lenght, t):
    
    """
    (None) -> NoneType
    
    This function draws a circle around the first drawn shape
    """
    
    # To determine the appropriate lenght of the circle radius
    # depending on the side of the squares lenght previously drawn
    radius = math.sqrt(2 * side_lenght**2)
    
    # To set the turtle position and color
    t.color("blue")
    t.rt(90)
    t.pu()
    t.forward(radius)
    t.pd()
    t.lt(90)
    
    # To draw the circle shape around the first shape
    t.circle(radius)
    t.pu()
    t.lt(90)
    t.forward(radius)
    t.rt(90)



def draw_triangle(t):
    """
    (None) -> NoneType
    
    This function draws a pink triangle in the left superior corner of the screen
    """
    
    # To set up the turtle position and color
    t.pu()
    t.goto(-200,200)
    t.pd()
    t.color("orange")
    t.fillcolor("pink")
    t.begin_fill()
    
    # To draw the triangle shape
    for i in range(3):
        t.forward(75)
        t.lt(120)
        t.fd(75)

    t.end_fill()


def draw_signature(t):
    """
    (None) -> NoneType
    
    This function displays the first letter of the author's first name
    as his artist signature
    """
    # To set up the turtle position and color
    t.pu()
    t.goto(400,-300)
    t.pd()
    t.color("black")
    
    # To draw the letter "E"
    t.lt(180)
    t.fd(60)
    t.lt(90)
    t.fd(60)
    t.lt(90)
    t.fd(60)
    t.pu()
    t.goto(340,-330)
    t.pd()
    t.fd(60)
    

    
def my_artwork():
    
    """
    (None) -> NoneType
    
    This function will draw 3 different shapes using the Turtle module
    """
    
    t = turtle.Turtle()
    t.speed(10)
    
    # To get two random integers that will be the first shape parameters
    
    # nums_of_squares in the first shape will be an integer between
    # 15 and 40 (both included) to ensure the drawing is not over charged
    nums_of_squares = random.randint(15,40)
    
    # side_lenght of the squares will be an integer between
    # 75 and 100 (both included) to ensure an apropriate drawing size
    side_lenght = random.randint(75,100)
    
    
    # To draw the first shape
    draw_circle_of_squares(nums_of_squares, side_lenght, t)
    
    # To draw the second shape around the first one
    draw_final_circle(side_lenght, t)
    
    # To draw the third shape on the left superior corner
    draw_triangle(t)
    
    # To draw the artist signature
    draw_signature(t)
    











