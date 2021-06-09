import pygame, random
import pandas as pd
from sklearn import neighbors
from sklearn.neighbors import KNeighborsRegressor

pygame.init()
pygame.display.set_caption('Pongers!')
# Variables and constants
WIDTH = 1200
HEIGHT = 600
BORDER = 20
VELOCITY = 4
FRAMERATE = 1000
colorOptions = ['blue','red','pink','yellow','green','purple']
bgColor = pygame.Color("black")
fgColor = pygame.Color(random.choice(colorOptions))
clock = pygame.time.Clock()

# Classes
class Ball: # Using a capital for classes
    RADIUS = 15
    # note these are double underscores - they're called 'dunder' functions
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
    def show(self, color):
        global screen
        pygame.draw.circle(screen, color, (self.x, self.y), self.RADIUS)
    def update(self, color):
        global bgColor, paddle1
        # TODO - game over message / response from program         
        nextX = self.x + self.vx
        nextY = self.y + self.vy
        if nextX - Ball.RADIUS < BORDER:
            self.vx = - self.vx
        elif nextY - Ball.RADIUS < BORDER or nextY + Ball.RADIUS > HEIGHT - BORDER:
            self.vy = - self.vy
        elif nextX + Ball.RADIUS > WIDTH - Paddle.PWIDTH and abs( nextY - paddle1.y + (Paddle.PHEIGHT // 2)) <= Paddle.PHEIGHT // 2:
            self.vx = - self.vx
        else:
            # Update the position of the ball
            self.show(bgColor)
            self.x = int(round(nextX,0))
            self.y = int(round(nextY,0))
            self.show(color)
    
class Paddle:
    PWIDTH = 20
    PHEIGHT = 100
    def __init__(self, y):
        self.y = y
    def show(self, color):
        global screen
        pygame.draw.rect(screen, color, pygame.Rect(WIDTH - self.PWIDTH, self.y - self.PHEIGHT, self.PWIDTH, self.PHEIGHT))
    def update(self, prediction):
        # TODO prevent the paddle moving off the screen
        global bgColor
        self.show(bgColor)
        self.y = prediction
        self.show(pygame.Color("white"))


# Create objects
ball = Ball( WIDTH // 2, HEIGHT // 2, -VELOCITY, -VELOCITY ) # '//' returns the integer value of the division only
paddle1 = Paddle( 150 )
# TODO Make a player 2 paddle, controlled by the ML algo

# Draw the screen
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.draw.rect(screen, fgColor, pygame.Rect(0,0,WIDTH-BORDER,BORDER))
pygame.draw.rect(screen, fgColor, pygame.Rect(0,0,BORDER,HEIGHT))
pygame.draw.rect(screen, fgColor, pygame.Rect(0,HEIGHT-BORDER,WIDTH-BORDER,BORDER))

# Show the objects for the first time
ball.show(pygame.Color(random.choice(colorOptions)))
paddle1.show(pygame.Color("white"))

# Phase 1 - producing the data.
# sample = open("sample.csv","w")
# print( "x,y,vx,vy,Paddle.y", file=sample)

# Phase 2 - training the algorithm using the data created
pong = pd.read_csv('test1.csv')
pong = pong.drop_duplicates()
X = pong.drop(columns="Paddle.y") # this removes the Paddle.y column as we only want the inputs
y = pong['Paddle.y'] # this selects the Paddle.y column, our desired output
clf = KNeighborsRegressor(n_neighbors=3) # create classifier using KNeighborsRegressor algorithm
clf = clf.fit(X, y) # 'fit' classifier with necessary X (input) and y (output) data

df = pd.DataFrame(columns=['x','y','vx','vy']) # create an empty Pandas data fram with specified column headers 
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # sample.close()
            running = False
    clock.tick( FRAMERATE )
    pygame.display.flip()
    # add the current ball positions to the dataframe
    toPredict = df.append( {'x': ball.x, 'y': ball.y, 'vx': ball.vx, 'vy': ball.vy}, ignore_index = True)
    # ask the classifier to predict an output based on the input
    newPaddleY = clf.predict( toPredict ) 
    paddle1.update( int(newPaddleY) ) # took 10 minutes to figure out this needed to be an int
    ball.update( pygame.Color(fgColor) )
    # print("{},{},{},{},{}".format(ball.x,ball.y,ball.vx,ball.vy,paddle1.y), file=sample)