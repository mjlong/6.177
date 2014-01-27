# 1 - Import library
import pygame, sys, random

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
    picArray = [[picVector[index[size[0]*row+col]] for col in range(size[1])] for row in range(size[0])]
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
    images = []
    for i in range(0,numImage):
        images.append(pygame.image.load("images/"+str(i+1)+".jpg"))
    images.append(pygame.image.load("images/back.jpg"))
    images.append(pygame.image.load("images/background.jpg"))

    size = (6,6)
    picArray = construct_pic_array(size, numImage)


    window_size = [size[1] * WIDTH + 200, size[0] * HEIGHT + 20] # width, height
    screen = pygame.display.set_mode(window_size)

    pygame.display.set_caption("Memory Card") # caption sets title of Window 

    board = Board(size, picArray, images)

    moveCount = 0

    clock = pygame.time.Clock()

    main_loop(screen, board, moveCount, clock, False, False)


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
#            board.theAnt.draw(screen) # draw ant Sprite
        
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
    def __init__(self, row, col, picIndex, image):
        pygame.sprite.Sprite.__init__(self)
        self.row = row
        self.col = col 
        self.image = pygame.transform.scale(image, (WIDTH, HEIGHT))
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

    def set_image(self, fileName):
        self.image = pygame.image.load(fileName).convert_alpha()
   
class Board:
    def __init__(self, size, picArray,images):

        self.size = size
        
        #---Initializes Squares (the "Board")---#
        self.squares = pygame.sprite.RenderPlain()
        self.boardSquares = [[Square(row,col, picArray[row][col], images[picArray[row][col]]) for col in range(size[1])] for row in range(size[0])]
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



if __name__ == "__main__":

     new_game()
    
     pass
