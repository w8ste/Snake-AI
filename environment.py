import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy
pygame.init()
font = pygame.font.Font('arial.ttf', 25)

# define colors
WHITE = (255, 255, 255)
RED = (255, 99, 71)
BLUE = (65, 105, 225)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLOCK_SIZE = 20
SPEED = 20


class Direction(Enum):
    Up = 1
    Right = 2
    Down = 3
    Left = 4


Point = namedtuple('Point', 'x, y')


class SNAKEGAME:
    def __init__(self, w=640, h=480):
        self.snakeHead = None
        self.snake = None
        self.clock = None
        self.direction = None
        self.food = None
        self.score = None
        self.width = w
        self.height = h
        self.iteration = None

        # Create game board
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Snake Game')
        self.restart()

    def restart(self):
        # init game
        self.score = 0
        self.direction = Direction.Up
        self.iteration = 0
        self.clock = pygame.time.Clock()

        self.snakeHead = Point(self.width / 2, self.height / 2)
        self.snake = [self.snakeHead, Point(self.snakeHead.x - BLOCK_SIZE, self.snakeHead.y),
                      Point(self.snakeHead.x - 2 * BLOCK_SIZE, self.snakeHead.y)]
        self._create_food()

    def _create_food(self):
        x = random.randint(0, (self.width - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.height - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._create_food()

    def _has_collided(self):
        return (self.snakeHead.x < 0 or self.snakeHead.x > self.width - BLOCK_SIZE or
                self.snakeHead.y < 0 or self.snakeHead.y > self.height - BLOCK_SIZE
                or self.snakeHead in self.snake[1:])

    def _snake_move(self, action):

        get_direction = [Direction.Right, Direction.Down, Direction.Left, Direction.Up]
        idx = get_direction.index(self.direction)

        if numpy.array_equal(action, [1, 0, 0]):
            new_dir = get_direction[idx]
        elif numpy.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = get_direction[next_idx]
        else:
            next_idx = (idx - 1) % 4
            new_dir = get_direction[next_idx]

        self.direction = new_dir

        x = self.snakeHead.x
        y = self.snakeHead.y
        if self.direction == Direction.Right:
            x += BLOCK_SIZE
        elif self.direction == Direction.Left:
            x -= BLOCK_SIZE
        elif self.direction == Direction.Down:
            y += BLOCK_SIZE
        elif self.direction == Direction.Up:
            y -= BLOCK_SIZE

        self.snakeHead = Point(x, y)

    def game_iteration(self):
        self.iteration += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        self._snake_move()
        self.snake.insert(0, self.snakeHead)

        finished = False
        prize = 0
        if self.iteration > 100*len(self.snake) or self._has_collided():
            finished = True
            prize -= 10
            return finished, self.score, prize

        if self.snakeHead == self.food:
            self.score += 1
            prize += 10
            self._create_food()
        else:
            self.snake.pop()

        self._update_ui()
        self.clock.tick(SPEED)
        return finished, self.score, prize

    def _update_ui(self):
        self.display.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(self.display, GREEN, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE, pygame.Rect(pt.x + 4, pt.y + 4, 12, 12))

        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [self.width / 2 - text.get_width() / 2, 0])

        pygame.display.flip()