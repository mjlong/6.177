# -*- coding: utf-8 -*-
# 1 - Import library
import pygame, sys, random
from Tkinter import *  
from pygame.locals import *
import Tkinter as tk



### Global Variables

WIDTH = 75  # this is the width of an individual square
HEIGHT = 75 # this is the height of an individual square

# RGB Color definitions
black = (0, 0, 0)
grey = (100, 100, 100)
white = (255, 255, 255)
green = (0, 255, 0)
red   = (255, 0, 0)
blue  = (0, 0, 255)





def construct_pic_array(size, numImage):
    sizeArray = size[0]*size[1]
    remainder = sizeArray/2
    images = []
    picVector = []
    batchSequence = range(numImage)
    while(remainder != 0):
        batchSize = random.randint(1,min(numImage,remainder))
        batchIndex= random.sample(batchSequence, batchSize)
        for i in range(batchSize):
            picVector.append(batchIndex[i])
            picVector.append(batchIndex[i])
        remainder = remainder - batchSize
    sequence = range(sizeArray)
    index = random.sample(sequence, sizeArray)
    picArray = [[picVector[index[size[1]*row+col]] for col in range(size[1])] for row in range(size[0])]
    return picArray



def new_game():


# 2 - Initialize the game

    pygame.init()
    pygame.mixer.init()
    pygame.font.init()

# 3 - Load images and audio

# 3.1 - Load audio
    pygame.mixer.music.load('images/doudizhu.mp3')
    pygame.mixer.music.play(-1, 0.0)
    pygame.mixer.music.set_volume(0.25)

#3.2 - Load images
    grass = pygame.image.load("images/grass.png")
    background = pygame.image.load('images/background.jpg')
    numImage = 8
    size = (4,5)
    images = []
    for i in range(0,numImage):
        pic = pygame.image.load("images/"+str(i+1)+".jpg")
        images.append(pygame.transform.scale(pic, (WIDTH, HEIGHT)))

    images.append(pygame.transform.scale(pygame.image.load("images/back.jpg"), (WIDTH, HEIGHT)))
    images.append(pygame.transform.scale(pygame.image.load("images/background.jpg"), (WIDTH, HEIGHT)))


    picArray = construct_pic_array(size, numImage)


    window_size = [size[1] * WIDTH + 200, size[0] * HEIGHT + 20] # width, height
    screen = pygame.display.set_mode(window_size)

    pygame.display.set_caption("Memory Card") # caption sets title of Window 

    board = Board(size, picArray, images)

    moveCount = 0

    clock = pygame.time.Clock()

    main_loop(picArray, images, screen, board, moveCount, clock, False, False)


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

def update_flip(screen, message, size ):
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

def update_clock(screen, message, size ):
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
    textRect.centery = textY+50
    screen.blit(text, textRect)

def update_remainder(screen, message, size ):
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
    textRect.centery = textY+100
    screen.blit(text, textRect)


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
def main_loop(picArray, images, screen, board, moveCount, clock, stop, pause):
    board.squares.draw(screen) # draw Sprites (Squares)
    draw_grid(screen, board.size)
    pygame.display.flip() # update screen
    clock.tick(4)
    board.show_back(images[len(images)-2])
    board.squares.draw(screen)
    pygame.display.flip()
    isFirst = -1
    cardRemain =  board.size[0]*board.size[1]/2
    if stop == True:
        again = raw_input("Would you like to run the simulation again? If yes, type 'yes'\n")
        if again == 'yes':
            new_game()
    while stop == False:        
        clock.tick(1)
        isPressed = False
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
            elif event.type==pygame.MOUSEBUTTONDOWN:
                    position=pygame.mouse.get_pos()
                    isPressed = True


        if stop == False and pause == False: 


            board.squares.draw(screen) # draw Sprites (Squares)
            draw_grid(screen,board.size)
            pygame.display.flip()

            if(isPressed == True):
                moveCount += 1
                isFirst = -1*isFirst #isFirst == 1 ==> this is the first click
                row = position[1]/HEIGHT
                col = position[0]/WIDTH

                if(isFirst == 1):
                    firstRow = row
                    firstCol = col
                    board.show_card(row, col)
                else:
                    secondRow = row
                    secondCol = col
                    board.show_card(row, col)
                    pass
                board.squares.draw(screen)
                pygame.display.flip()

                if(isFirst == -1):
                    clock.tick(1)
                    if( picArray[firstRow][firstCol] != \
                        picArray[secondRow][secondCol]):
                        board.hide_card(firstRow, firstCol)
                        board.hide_card(secondRow, secondCol)
                    else:
                        cardRemain = cardRemain - 1
                board.squares.draw(screen)
                pygame.display.flip()

                if(cardRemain == 0):
                    stop = True
        
            update_remainder(screen, "Remain pair:" + str(cardRemain), board.size)
            update_flip(screen, "Try times: " + str(moveCount), board.size)
            update_clock(screen, "Time #"+str((pygame.time.get_ticks())/60000)\
                                       +":"+str((pygame.time.get_ticks())/1000%60)\
                                       .zfill(2), board.size)

            pygame.display.flip() # update screen
            clock.tick(10)



            draw_grid(screen,board.size)
            
            pygame.display.flip() # update screen
            clock.tick(5)
            
            # Step 2: Flip color of square:
            # ** TODO: flip the color of the square here **
            board.squares.draw(screen) 
            # ** TODO: draw the grid here **
            draw_grid(screen,board.size)
    
            
            pygame.display.flip() #update screen
            clock.tick(5)
            
            # Step 3: Move Ant
            board.squares.draw(screen) #
            # ** TODO: draw the grid here **
            draw_grid(screen,board.size)

            
            pygame.display.flip() # update screen
            clock.tick(5)
            
            # ------------------------

    pygame.quit() # closes things, keeps idle from freezing

class Square(pygame.sprite.Sprite):
    def __init__(self, row, col, picIndex, image):
        pygame.sprite.Sprite.__init__(self)
        self.row = row
        self.col = col 
        self.image = image
        self.rect = self.image.get_rect() # gets a rect object with width and height specified above
                                            # a rect is a pygame object for handling rectangles
        self.rect.x = get_col_left_loc(col)
        self.rect.y = get_row_top_loc(row)
        self.picIndex = picIndex


    def get_rect_from_square(self):
        """
        Returns the rect object that belongs to this Square
        """
        return self.rect;
        pass

    def flip_image(self):
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
    def __init__(self, size, picArray,images):

        self.size = size
        
        #---Initializes Squares (the "Board")---#
        self.squares = pygame.sprite.RenderPlain()
        self.images = images

        self.boardSquares = [[Square(row,col, picArray[row][col], images[picArray[row][col]]) for col in range(size[1])] for row in range(size[0])]

        for row in range(size[0]):
          for col in range(size[1]):
            self.squares.add(self.boardSquares[row][col])
        #---Populate boardSquares with Squares---#
        pass

        #---Initialize the Ant---#
        indexRow = int(random.uniform(0, size[0]))/2
        indexCol = int(random.uniform(0, size[1]))/2
                          


    def get_square(self, x, y):
        """
        Given an (x, y) pair, return the Square at that location
        """
        return self.boardSquares[x][y]
        pass
    def show_back(self, image):
        for row in range(self.size[0]):
            for col in range(self.size[1]):
                self.boardSquares[row][col].image = image

    def show_card(self, x, y):
        square = self.boardSquares[x][y]
        square.image = self.images[square.picIndex]
        
    def hide_card(self, x, y):
        square = self.boardSquares[x][y]
        square.image = self.images[len(self.images)-2]
                

if __name__ == "__main__":

     new_game()
    
     pass
