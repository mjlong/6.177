"""
6.177 Problem Set (IAP 2014)
Completed by Jilang Miao (jlmiao@mit.edu)
"""

"""
*** Warm-up Exercises ***
"""

### 1. Numerical Operations
def operate(a, b):
  x1 = (a-b)**b
  x2 = (a+b)%10
  if(x1>x2):
    return x1
  else:
    return x2

# Fill in the function below which takes in two positive integers
# and returns either ((a - b) to the power of b) OR ((a + b) modulo 10)
# depending on which formula produces a greater value.
#
operate(10, 2)
# ==> 64
operate(2, 3)
# ==> 5

#    raise NotImplementedError


### 2. String and list operation

# Fill in the function below. It takes in a list of strings (of length >= 3)
# called myStrings and trims the strings to exclude the first and last
# character of each string. It then returns the list in reverse order
# with *only* the first alphabetical letter of each new string capitalized
# (not always the first character!).
# Do NOT modify the original passed-in list.
#
# myList = ['25maroon', 'ComBInE', 'apple', '0315']
# fix_strings(myList) 
# ==> ['31', 'Ppl', 'Ombin', '5Maroo']
# myList 
# ==> ['25maroon', 'ComBInE', 'apple', '0315']

def fix_strings(yourStrings):
    myStrings=yourStrings[:]
    n=len(myStrings)-1
    for i in range(n/2+1):
        element=myStrings[i]
        m=len(element)-1
        element=element[1:m]
        element=element.lower()
        element=element.title()
#        for j in range(m-1):
#            if(element[j].isalpha()):
#                element[j].upper()
#                break
        myStrings[i]=myStrings[n-i]
        myStrings[n-i]=element
        if((n-i)!=i):
            element=myStrings[i]
            m=len(element)-1
            element=element[1:m]
#            for j in range(m-1):
#                if(element[j].isalpha()):
#                    element[j].upper()
#                    break
            element=element.lower()
            element=element.title()
            myStrings[i]=element
            pass
    return myStrings


#    raise NotImplementedError


### 3. Class instances and methods

# Using the Car class defined below as reference, 
# fill in the modify() method below so that it takes in a Car instance
# and changes the name of the instance to 'Python' and its color to 'Ruby'.
# Then, pass in parameters into the combineTrips() method
# so that it sums together all weighted trips (miles divided by
# miles per gallon) and stores the decimal value in self.__combination.
# Your function should return True if successful.
#



class Car(object):
    def __init__(self, name, color):
        self.__name = name
        self.__color = color
        # This dict saves trips in the format (miles, miles_per_gallon).
        self.__trips = {
            "ski trip": (101, 28),
            "groceries": (15, 18),
            "leisure": (3, 9),
            "apple store": (17, 22),
            "airport": (93, 30),
            "canada": (1337, 26),
            "engine check": (0, 0)
        }
        self.__combination = 60.07
#
    def get_color(self):
        return self.__color
    
#
    def change_color(self, color):
        self.__color = color
#
    def get_name(self):
        return self.__name
#
    def new_name(self, name):
        self.__name = name
#                                                                                 
    def get_combination(self):
        return self.__combination
#
    def get_miles_per_gallon(self):
        return self.__mpg
#
    def combine_trips(self, reduce_function):
        self.__combination = reduce_function(self.__trips)


def reduce_function(Trips):
    i=0
    gallon=range(len(Trips)-1)
    for ele in Trips.values()[0:len(Trips)-1]:
      gallon[i]=1.0*ele[0]/ele[1]
      i=i+1
    return reduce(lambda x,y : x+y, gallon)

def modify(carInstance):
    carInstance.new_name('Python')
    carInstance.change_color('Ruby')
    carInstance.combine_trips(reduce_function)
    return True

    

#
myCar = Car('Moriarty', 'Sherlock')
modify(myCar)
# ==> True
myCar.get_name()
# ==> 'Python'
myCar.get_color()
# ==> 'Ruby'
myCar.combine_trips(reduce_function)
myCar.get_combination()
# ==> 60.07

#    raise NotImplementedError



"""
***** Langton's Ant *****
"""

# Algorithm described at http://en.wikipedia.org/wiki/Langton%27s_ant

import pygame, sys, random
import tests as T

### Global Variables
WIDTH = 76  # this is the width of an individual square
HEIGHT = 76 # this is the height of an individual square

# RGB Color definitions
black = (0, 0, 0)
grey = (100, 100, 100)
white = (255, 255, 255)
green = (0, 255, 0)
red   = (255, 0, 0)
blue  = (0, 0, 255)

def get_row_top_loc(rowNum, height = HEIGHT):
    """
    Returns the location of the top pixel in a square in
    row rowNum, given the row height.
    """
    return rowNum*height+10
    pass

def get_col_left_loc(colNum, width = WIDTH):
    """
    Returns the location of the leftmost pixel in a square in
    column colNum, given the column width.
    """
    return colNum*width+10 
    pass

def update_text(screen, message, size ):
    """
    Used to display the text on the right-hand part of the screen.
    You don't need to code anything, but you may want to read and
    understand this part.
    """
    textSize = 20
    font = pygame.font.Font(None, 20)
    textY = 0 + textSize
    text = font.render(message, True, white, black)
    textRect = text.get_rect()
    textRect.centerx = (size[1] + 1) * WIDTH + 10
    textRect.centery = textY
    screen.blit(text, textRect)

def new_game():
    """
    Sets up all necessary components to start a new game
    of Langton's Ant.
    """
    isDefault = raw_input("Would you like to use the default board? (Y/N)\n")
    if isDefault == 'Y':
      size = (10,10)
    else:
      rowNum = input('Please input row number:\n')
      colNum = input('Please input column number:\n')
      size = (rowNum, colNum)
    pygame.init() # initialize all imported pygame modules

    window_size = [size[1] * WIDTH + 200, size[0] * HEIGHT + 20] # width, height
    screen = pygame.display.set_mode(window_size)

    pygame.display.set_caption("Langton's Ant") # caption sets title of Window 

    board = Board(size)

    moveCount = 0

    clock = pygame.time.Clock()

    main_loop(screen, board, moveCount, clock, False, False)

def draw_grid(screen, size):
    """
    Draw the border grid on the screen.
    """
    for i in range(size[1]+1):
      pnt1 = (i*WIDTH+10,size[0]*HEIGHT+10)
      pnt2 = (i*WIDTH+10,0+10)
      pygame.draw.line(screen, blue, pnt1, pnt2)
    for i in range(size[0]+1):
      pnt1 = (0+10, i*HEIGHT+10)
      pnt2 = (size[1]*WIDTH+10, i*HEIGHT+10)
      pygame.draw.line(screen, blue, pnt1, pnt2)
    pass

# Main program Loop: (called by new_game)
def main_loop(screen, board, moveCount, clock, stop, pause):
    board.squares.draw(screen) # draw Sprites (Squares)
    draw_grid(screen, board.size)
    board.theAnt.draw(screen) # draw ant Sprite
    pygame.display.flip() # update screen
    
    if stop == True:
        again = raw_input("Would you like to run the simulation again? If yes, type 'yes'\n")
        if again == 'yes':
            new_game()
    while stop == False:        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #user clicks close
                stop = True
                pygame.quit()
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_p:
                    if pause:
                        pause = False
                    else:
                        pause = True

        if stop == False and pause == False: 
            board.squares.draw(screen) # draw Sprites (Squares)
            # ** TODO: draw the grid **
            draw_grid(screen,board.size)
            board.theAnt.draw(screen) # draw ant Sprite
        
            update_text(screen, "Move #" + str(moveCount), board.size)
            pygame.display.flip() # update screen
            clock.tick(10)

            #--- Do next move ---#

            # Step 1: Rotate class Ant(pygame.sprite.Sprite):
            # ** TODO: rotate the ant and save it's current square **
            board.squares.draw(screen) # draw Sprites (Squares) - they should cover up the ant's previous position
            curSquare=board.rotate_ant_get_square()
            # ** TODO: draw the grid here **
            draw_grid(screen,board.size)
            board.theAnt.draw(screen) # draw ant Sprite (rotated)
            
            pygame.display.flip() # update screen
            clock.tick(5)
            
            # Step 2: Flip color of square:
            # ** TODO: flip the color of the square here **
            board.squares.draw(screen) # draw Sprites (Squares) - they should cover up the ant's previous position
            curSquare.flip_color()
            # ** TODO: draw the grid here **
            draw_grid(screen,board.size)
            board.theAnt.draw(screen) # draw ant Sprite (rotated)
            
            pygame.display.flip() #update screen
            clock.tick(5)
            
            # Step 3: Move Ant
            # ** TODO: make the ant step forward here **
            board.ant.step_forward(board)
            board.squares.draw(screen) # draw Sprites (Squares) - they should cover up the ant's previous position
            # ** TODO: draw the grid here **
            draw_grid(screen,board.size)
            board.theAnt.draw(screen) # draw ant Sprite (rotated)
            
            pygame.display.flip() # update screen
            clock.tick(5)
            
            moveCount += 1
            # ------------------------

    pygame.quit() # closes things, keeps idle from freezing

class Square(pygame.sprite.Sprite):
    def __init__(self, row, col, color):
        pygame.sprite.Sprite.__init__(self)
        self.row = row
        self.col = col 
        self.image = pygame.Surface([WIDTH, HEIGHT])
        self.image.fill(color)
        self.rect = self.image.get_rect() # gets a rect object with width and height specified above
                                            # a rect is a pygame object for handling rectangles
        self.rect.x = get_col_left_loc(col)
        self.rect.y = get_row_top_loc(row)
        self.color = color

    def get_rect_from_square(self):
        """
        Returns the rect object that belongs to this Square
        """
        return self.rect;
        pass

    def flip_color(self):
        """
        Flips the color of the square (white -> black or 
        black -> white)
        """
        if(self.color is black):
          self.color = white
        else:
          self.color = black
        self.image.fill(self.color)
        pass
   
class Board:
    def __init__(self, size):

        self.size = size
        
        #---Initializes Squares (the "Board")---#
        self.squares = pygame.sprite.RenderPlain()
        self.boardSquares = [[Square(row,col,white) for col in range(size[1])] for row in range(size[0])]
        for row in range(size[0]):
          for col in range(size[1]):
            self.squares.add(self.boardSquares[row][col])
        #---Populate boardSquares with Squares---#
        pass

        #---Initialize the Ant---#
        indexRow = int(random.uniform(0, size[0]))/2
        indexCol = int(random.uniform(0, size[1]))/2
        self.ant = Ant(self, indexRow, indexCol)
                          
        #---Adds Ant to the "theAnt" Sprite List---#
        self.theAnt = pygame.sprite.RenderPlain()
        self.theAnt.add(self.ant)

    def get_square(self, x, y):
        """
        Given an (x, y) pair, return the Square at that location
        """
        return self.boardSquares[x][y]
        pass

    def rotate_ant_get_square(self):
        """ 
        Rotate the ant, depending on the color of the square that it's on,
        and returns the square that the ant is currently on
        """
        color = self.ant.get_current_square().color;

        if(color is white):
          self.ant.rotate_right()
        else:
          self.ant.rotate_left()
        return self.get_square(self.ant.row, self.ant.col)
        pass 

class Ant(pygame.sprite.Sprite):
    def __init__(self, board, col, row):
        pygame.sprite.Sprite.__init__(self)
        self.col = col
        self.row = row
        yourSquare = board.get_square(row,col)
        self.rect = yourSquare.get_rect_from_square()
#        center = self.rect.center
#        self.rect = yourSquare.get_rect_from_square(center=center)
        self.rotation = (0, 1) # pointing up
        self.board = board
        self.set_pic()
        
    def get_current_square(self):
        return self.board.get_square(self.row, self.col)
        pass
        
    def rotate_left(self):
        """
        Rotates the ant 90 degrees counterclockwise
        """
        self.image = pygame.transform.rotate(self.image, 90)        
#        r0 = self.rotation[0]
#        r1 = self.rotation[1]
#        self.rotation[0] = r1
#        self.rotation[1] =-r0
        pass

    def rotate_right(self):
        """
        Rotates the ant 90 degrees clockwise
        """
        self.image = pygame.transform.rotate(self.image,-90)
#        r0 = self.rotation[0]
#        r1 = self.rotation[1]
#        self.rotation[0] =-r1
#        self.rotation[1] = r0
        pass
    
    def step_forward(self, board):
        """
        Make the ant take a step forward in whatever direction it's currently pointing.
        Don't forget - row numbers increase from top to bottom and column numbers
        increase from left to right!
        """
        r0 = self.rotation[0]
        r1 = self.rotation[1]
        color = self.get_current_square().color
# movement is determined by the original color
        if(color is black):
          self.rotation = (r1, -r0)
          self.row = (self.row + r0 + board.size[0])%board.size[0]
          self.col = (self.col + r1 + board.size[1])%board.size[1]
          self.rect = board.get_square(self.row,self.col).get_rect_from_square()
        else:
          self.rotation = (-r1, r0)
          self.row = (self.row - r0 + board.size[0])%board.size[0]
          self.col = (self.col - r1 + board.size[1])%board.size[1]
          self.rect = board.get_square(self.row,self.col).get_rect_from_square()
        pass
    
    def set_pic(self):
        """
        Sets the picture that represents our Ant.
        If you want to use a new picture, you'll need to change
        this method.
        """
        self.image = pygame.image.load("ant.png").convert_alpha()

if __name__ == "__main__":
    # Uncomment this line to test your warmup answers:
     T.test_warmup()

    # Uncomment this line to test Part 2:
# Note: the code accepts size as a tuple, please modify tests.py before check
#def test_part_two(size):
#    import runAnt as P
#    P.pygame.init()
#    window_size = [size[1] * P.WIDTH + 20, size[0] * P.HEIGHT + 20]
#    screen = P.pygame.display.set_mode(window_size)
#    P.pygame.display.set_caption("Langton's Ant")
#    board = P.Board(size)
#    moveCount = 0
#    clock = P.pygame.time.Clock()
#    P.draw_grid(screen,board.size)
#    P.pygame.display.flip()
#    time.sleep(2)
#    P.pygame.quit()
#
#     T.test_part_two((10,10))

    # Uncomment this line to test Part 3:
# Note: the code accepts size as a tuple, please modify tests.py before check
#def test_part_three(size):
#    import runAnt as P
#    P.pygame.init()
#    window_size = [size[1] * P.WIDTH + 20, size[0] * P.HEIGHT + 20]
#    screen = P.pygame.display.set_mode(window_size)
#    P.pygame.display.set_caption("Langton's Ant")
#    board = P.Board(size)
#    moveCount = 0
#    clock = P.pygame.time.Clock()
#    for sprite in board.squares:
#        g = P.pygame.sprite.Group(sprite)
#        g.draw(screen)
#        P.pygame.display.flip()
#        time.sleep(.05)
#    P.draw_grid(screen,board.size)
#    P.pygame.display.flip()
#    time.sleep(1.5)
#    P.pygame.quit()
#
#     T.test_part_three((10,10))

    # Uncomment this line to call new_game when this file is run:
     new_game()
    
     pass
