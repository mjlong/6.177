# -*- coding: utf-8 -*-
'''
6.177 Problem Set (IAP 2014)
Completed by Jilang Miao (jlmiao@mit.edu)
             Miaomiao Jin (mmjin@mit.edu)
'''
### Global Variables
#####TODO: fix window size, vary square size
WIDTH = 75  # this is the width of an individual square
HEIGHT = 75 # this is the height of an individual square

# RGB Color definitions
black = (0, 0, 0)
grey = (100, 100, 100)
white = (255, 255, 255)
green = (0, 255, 0)
red   = (255, 0, 0)
blue  = (0, 0, 255)

# 1 - Import library
import pygame, sys, random
import easygui as eg
from pygame.locals import *

# 2 - Initialize the game
pygame.init()
pygame.mixer.init()
pygame.font.init()

# 3 - Load images and audio
# 3.1 - Load audio
pygame.mixer.music.load('images/doudizhu.mp3')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)
match= pygame.mixer.Sound("images/explode.wav") #play when two matches
match.set_volume(1.0)
winning= pygame.mixer.Sound("images/winning.mp3") #play when win
winning.set_volume(1.0)
# 3.2 - Load images
grass = pygame.image.load("images/grass.png")
gameover = pygame.image.load("images/gameover.png")
winner=pygame.image.load("images/winner.jpg")
numImage = 28
images = []
for i in range(0,numImage):
    pic = pygame.image.load("images/"+str(i+1)+".jpg")
    images.append(pygame.transform.scale(pic, (WIDTH, HEIGHT)))

images.append(pygame.transform.scale(\
        pygame.image.load("images/back.jpg"), (WIDTH, HEIGHT)))
images.append(pygame.transform.scale(\
        pygame.image.load("images/background.jpg"), (WIDTH, HEIGHT)))



def initialize_game():
    image   = "images/checkbox.gif"
    title   = "Memory Card"
    msg     = "Please Choose Your Level"
    choices = ["Easy","Medium","Hard","Customize"]

    reply   = eg.buttonbox(msg,image=image,choices=choices)
    
    size = []
    
    if reply=="Easy":
        size=[4,4]
    if reply=="Medium":
        size=[6,6]
    if reply=="Hard":
        size=[8,8]
    if reply=="Customize":
        msg         = "Enter Your Dimensions(at least one even number)"
        title       = "Memory Card"
        fieldNames  = ["row","column"]
        fieldValues = []  # we start with blanks for the values
        fieldValues = eg.multenterbox(msg,title, fieldNames)
        while 1:  # do forever, until we find acceptable values and break out
                if fieldValues == None: 
                    break
                errmsg = ""
                
                # look for errors in the returned values
                for i in range(len(fieldNames)):
                    if fieldValues[i].strip() == "":
                        errmsg = errmsg + ('"%s" is a required field.\n\n' % fieldNames[i])
                        
                if int(fieldValues[0])%2!=0 and int(fieldValues[1])%2!=0:
                    errmsg = ('Please input at least on EVEN number')
                    
                if errmsg == "": 
                    break # no problems found
                else:
                    # show the box again, with the errmsg as the message    
                    fieldValues = eg.multenterbox(errmsg, title, fieldNames, fieldValues)
                
        size=[int(fieldValues[0]),int(fieldValues[1])]
    return size






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

def new_game():
    size = initialize_game()
    
    picArray = construct_pic_array(size, numImage)

  
    window_size = [size[1] * WIDTH + 200, size[0] * HEIGHT + 20] # width, height
    screen = pygame.display.set_mode(window_size)

    pygame.display.set_caption("Memory Card") # caption sets title of Window
    winner=pygame.image.load("images/winner.jpg")
    winner=pygame.transform.scale(winner, (window_size[0],window_size[1]))
    gameover = pygame.image.load("images/gameover.png")
    gameover=pygame.transform.scale(gameover, (window_size[0],window_size[1]))
    background = pygame.image.load('images/background.jpg')
    background=pygame.transform.scale(background, (window_size[0],window_size[1]))
    screen.blit(background,(0,0))
    board = Board(size, picArray, images)
    board.squares.draw(screen)
    pygame.display.update()
    clock = pygame.time.Clock()

    main_loop(picArray, images, screen, board, clock, False,size)
#####TODO: return scores; write scores for later comparison
    
# Main program Loop: (called by new_game)
def main_loop(picArray, images, screen, board, clock, stop,size):
    board.squares.draw(screen) 
    draw_grid(screen, board.size)
    pygame.display.flip() 
    clock.tick(2)
    board.show_back(images[len(images)-2])
    board.squares.draw(screen)
    pygame.display.flip()
    arrayFliped = []
    isFirst = -1
    cardRemain =  board.size[0]*board.size[1]/2
    running=1
    moveCount = 0
    start_time = pygame.time.get_ticks()
#####TODO: replace with ESCAPE, write a new check
#####TODO: reminder after time of no move

    while running:
        pygame.display.update()
        if stop == True:
            #pygame.display.quit()
            
            title   = "Memory Card"
            msg     = "Would you like to try again?"
            choices = ["Yes, I like it!","No, maybe later~"]
            reply   = eg.buttonbox(msg,choices=choices)
            if reply=="Yes, I like it!":
                pygame.init()
                new_game()
            else:
                running=0
                pygame.quit() # closes things, keeps idle from freezing
                exit(0)
        else:
            isPressed = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT: #user clicks close
                    title   = "Memory Card"
                    msg     = "Are you sure to quit?"
                    choices = ["Yes, busy now","No, continue please"]
                    reply   = eg.buttonbox(msg,choices=choices)
                    if reply == "Yes, busy now":
                        pygame.quit()
                        exit(0)
                    else:
                        pass
                if event.type==pygame.MOUSEBUTTONDOWN:
                    position=pygame.mouse.get_pos()
                    row = position[1]/HEIGHT
                    col = position[0]/WIDTH
                    print position, row, col
                    # clicks beyond board of squares will not effect
                    if (row <= size[0]-1) and (col <= size[1] -1):
                        isPressed = True
          
            board.squares.draw(screen) 
            pygame.display.flip()

            if(isPressed == True):
                if((row,col) in arrayFliped):
                    continue
                moveCount += 1
                isFirst = -1*isFirst #isFirst == 1 ==> this is the first click

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
                    if( (firstRow == secondRow) and (firstCol == secondCol)):
                        board.hide_card(firstRow, firstCol)
                    elif( picArray[firstRow][firstCol] != \
                        picArray[secondRow][secondCol]):
                        board.hide_card(firstRow, firstCol)
                        board.hide_card(secondRow, secondCol)
                    else:
                        cardRemain = cardRemain - 1
                        arrayFliped.append((firstRow, firstCol))
                        arrayFliped.append((secondRow, secondCol))
                        match.play()
                    clock.tick(1)
                board.squares.draw(screen)
                pygame.display.flip()
          
            board.squares.draw(screen) 
            if(cardRemain == 0):
                pygame.font.init()
                font = pygame.font.Font(None, 24)
                text = font.render("Remain pairs: " + str(cardRemain), True, (255,0,0))
                textRect = text.get_rect()
                textRect.centerx = screen.get_rect().centerx
                textRect.centery = screen.get_rect().centery+24
                screen.blit(winner,(0,0))
                screen.blit(text, textRect) 
                
                winning.play()
                pygame.display.flip()
                clock.tick(0.5)
                stop = True
                
            if (pygame.time.get_ticks()-start_time > 10000):
                pygame.font.init()
                font = pygame.font.Font(None, 24)
                text = font.render("Remain pairs: " + str(cardRemain), True, (255,0,0))
                textRect = text.get_rect()
                textRect.centerx = screen.get_rect().centerx
                textRect.centery = screen.get_rect().centery+24
                screen.blit(gameover, (0,0))
                screen.blit(text, textRect)
                winning.play()
                pygame.display.flip()
                clock.tick(1)
                stop = True

            update_remainder(screen, "Remain pairs: " + str(cardRemain), board.size)
            update_flip(screen, "Try times: " + str(moveCount), board.size)
            #TODO : update_remainder leaves last image
            update_clock(screen, "Time : "+str((pygame.time.get_ticks()-start_time)/60000)\
                                       +":"+str((pygame.time.get_ticks()-start_time)/1000%60)\
                                       .zfill(2), board.size)
            pygame.display.flip() # update screen

class Square(pygame.sprite.Sprite):
    def __init__(self, row, col, picIndex, image):
        pygame.sprite.Sprite.__init__(self)
        self.row = row
        self.col = col 
        self.image = image
        self.rect = self.image.get_rect() 
        self.rect.x = get_col_left_loc(col)
        self.rect.y = get_row_top_loc(row)
        self.picIndex = picIndex

   
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
