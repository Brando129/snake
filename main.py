# Imports.
import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

# Classes

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
    win.fill((0, 0, 0))
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
