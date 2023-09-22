# Imports.
import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

# Classes
# Class Snake
class Snake(object):
    body = []
    turns = {}
    def __init__(self, color, position):
        self.color = color
        self.head = Cube(position)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1

    def move(self):
        for event in pygame.events.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_LEFT]:
                    self.dirnx = -1
                    self.dirny = 0
                    self.turns[self.head.position[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1
                    self.dirny = 0
                    self.turns[self.head.position[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_UP]:
                    self.dirnx = 0
                    self.dirny = -1
                    self.turns[self.head.position[:]] = [self.dirnx, self.dirny]

                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0
                    self.dirny = 1
                    self.turns[self.head.position[:]] = [self.dirnx, self.dirny]

        for i, c in enumerate(self.body):
            p = c.position[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(p)

# Functions
# Draws the game grid.
def draw_grid(w, rows, surface):
    size_between = w // rows
    x = 0
    y = 0
    for l in range(rows):
        x = x + size_between
        y = y + size_between

        pygame.draw.line(surface, (255, 255, 255), (x,0), (x, w))
        pygame.draw.line(surface, (255, 255, 255), (0,y), (w, y))

# Redraws all objects on the playing window.
def redraw_window(surface):
    global rows, width
    surface.fill((0, 0, 0))
    draw_grid(width, rows, surface)
    pygame.display.update()

# Main game loop.
def main():
    global width, rows
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    snake = snake((255, 0, 0), (10, 10))
    flag = True

    clock = pygame.time.Clock()

    while flag:
        pygame.time.delay(50)
        clock.tick(10)
        redraw_window(win)


main()
