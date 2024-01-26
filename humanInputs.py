import pygame
import random
from enum import Enum
from collections import namedtuple

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
        self.width = w
        self.height = h

        # Create game board
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Snake Game')
        # init game
        self.score = 0
        self.food = None
        self.direction = Direction.Up
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

    def _snake_move(self):
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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.Left
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.Right
                elif event.key == pygame.K_UP:
                    self.direction = Direction.Up
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.Down

        self._snake_move()
        self.snake.insert(0, self.snakeHead)

        # 3. check if game over
        game_over = False
        if self._has_collided():
            game_over = True
            return game_over, self.score

        if self.snakeHead == self.food:
            self.score += 1
            self._create_food()
        else:
            self.snake.pop()

        self._update_ui()
        self.clock.tick(SPEED)
        return game_over, self.score

    def _update_ui(self):
        self.display.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(self.display, GREEN, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE, pygame.Rect(pt.x + 4, pt.y + 4, 12, 12))

        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [self.width/2 - text.get_width()/2, 0])

        pygame.display.flip()


if __name__ == '__main__':
    game = SNAKEGAME()

    # game loop
    while True:
        game_over, score = game.game_iteration()

        if game_over == True:
            break

print('Final Score', score)

pygame.quit()
