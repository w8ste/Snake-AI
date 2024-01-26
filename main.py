import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()
font = pygame.font.Font('arial.ttf', 25)


# define colors
WHITE = (255, 255, 255)
RED = (255, 99, 71)
BLUE = (65,105,225)
BLACK = (0, 0, 0)

BLOCK_SIZE = 20
SPEED = 15

class Direction(Enum):
    Up = 1
    Right = 2
    Down = 3
    Left = 4


Point = namedtuple('Point', 'x, y')

class SNAKEGAME:
    def __init__(self, w=640, h=480):