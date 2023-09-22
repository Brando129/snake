# Imports
import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

# Classes
# Cube class.
class cube(object):
    rows = 20
    w = 500
    def __init__(self,start,dirnx=1,dirny=0,color=(255,0,0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color


    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny) # Change our position

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows # Width/height of each cube
        i = self.pos[0] # Current row
        j = self.pos[1] # Current column

        # By multiplying the row and column value of our cube by the width and height of each cube we can determine where to draw it
        pygame.draw.rect(surface, self.color, (i*dis+1,j*dis+1, dis-2, dis-2))

        # Draw the eyes
        if eyes:
            centre = dis//2
            radius = 3
            circleMiddle = (i*dis+centre-radius,j*dis+8)
            circleMiddle2 = (i*dis + dis -radius*2, j*dis+8)
            pygame.draw.circle(surface, (0,0,0), circleMiddle, radius)
            pygame.draw.circle(surface, (0,0,0), circleMiddle2, radius)



# Snake Class
class snake(object):
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos) # Front of the snake
        self.body.append(self.head) # Adds a body part to the snakes head

        # Direction the snake is moving
        self.dirnx = 0
        self.dirny = 1

    def move(self):
        # Check if the user hit the red x
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed() # Determine which keys are being pressed

            # Loop through all the keys
            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]

            for i, c in enumerate(self.body):  # Loop through every cube in our body
                p = c.pos[:]  # This stores the cubes position on the grid
                if p in self.turns:  # If the cubes current position is one where we turned
                    turn = self.turns[p]  # Get the direction we should turn
                    c.move(turn[0],turn[1])  # Move our cube in that direction
                    if i == len(self.body)-1:  # If this is the last cube in our body remove the turn from the dict
                        self.turns.pop(p)
                else:  # If we are not turning the cube
                    # If the cube reaches the edge of the screen we will make it appear on the opposite side
                    if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.rows-1, c.pos[1])
                    elif c.dirnx == 1 and c.pos[0] >= c.rows-1: c.pos = (0,c.pos[1])
                    elif c.dirny == 1 and c.pos[1] >= c.rows-1: c.pos = (c.pos[0], 0)
                    elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0],c.rows-1)
                    else: c.move(c.dirnx,c.dirny)  # If we haven't reached the edge just move in our current direction


    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1


    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny

        # We need to know which side of the snake to add the cube to
        # So we check what direction we are currently moving in to determine if we
        # need to add the cube to the left, right, above or below.
        if dx == 1 and dy == 0:
            self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0],tail.pos[1]+1)))

        # We then set the cubes direction to the direction of the snake.
        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy


    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i ==0: # Draw eyes on the first cube
                c.draw(surface, True) # Adding the true as an argument will tell us to draw eyes
            else:
                c.draw(surface) # Otherwise we just draw a cube


def drawGrid(w, rows, surface):
    sizeBtwn = w // rows # Gives us the distance between lines

    x = 0 # Keeps track of the current x
    y = 0 # Keeps track of the current y

    # Draws one vertical and horizontal line each loop
    for l in range(rows):
        x = x + sizeBtwn
        y = y + sizeBtwn

        pygame.draw.line(surface, (255,255,255), (x,0),(x,w))
        pygame.draw.line(surface, (255,255,255), (0,y),(w,y))


def redrawWindow(surface):
    global rows, width, s, snack
    surface.fill((0,0,0)) # Fills the screen with black
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width,rows, surface) # Draws the grid lines
    pygame.display.update() # Update the screen


def randomSnack(rows, item):

    positions = item.body # Get all the positions of the cubes in our snake

    # Keep generating random positions until we get a valid one
    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)

        # This wll check if the position we generated is occupied by the snake
        if len(list(filter(lambda z:z.pos == (x,y), positions))) > 0:
            continue
        else:
            break

    return (x,y)


def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass

# Main game loop
def main():
    global width, rows, s, snack
    width = 500 # Width of our screen
    rows = 20 # Amount of rows
    win = pygame.display.set_mode((width, width)) # Creates our screen instance
    s = snake((255,0,0), (10,10)) # Creates the snake instance
    snack = cube(randomSnack(rows, s), color=(0,255,0))
    flag = True

    clock = pygame.time.Clock() # Creates a clock instance

    # Starts the main game loop
    while flag:
        pygame.time.delay(50) # Delays the game so it doesn't run too quickly
        clock.tick(10) # Makes the game run at 10 FPS
        s.move()
        if s.body[0].pos == snack.pos: # Check if the head collides with the snack
            s.addCube() # Add a new cube to the snake body
            snack = cube(randomSnack(rows, s), color=(0,255,0))

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])): # This will check if any of the positions in our body list overlap
                print('Score: ', len(s.body))
                message_box('You Lost!', 'Play again...')
                s.reset((10,10))
                break


        redrawWindow(win) # Refreshes game screen
pygame.display.set_caption("Tetris")
main()