import torch
import random as rand
from collections import deque
import numpy as np
from environment import SNAKEGAME, Point, Direction, BLOCK_SIZE
from matplot import plot

LR = 0.001
BATCH_SIZE = 1000


class Agent:

    def __init__(self):
        self.epsilon = 0
        self.gamma = 0
        self.games_played = 0
        # self.model = Linear_QNet(11, 256, 3)
        # self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)
        self.memory = deque(maxlen=100_000)

    def recall(self, current_state, action, next_state, price, game_over):
        self.memory.append((current_state, action, next_state, price, game_over))

    def get_action(self, current_state):
        self.epsilon = 75 - self.games_played  # decreases randomness of moves over time
        move = [0, 0, 0]
        if rand.randint(0, 200) >= self.epsilon:  # predict a good move
            state_0 = torch.tensor(current_state, dtype=torch.float)
            prediction = self.model(state_0)
            move_index = torch.argmax(prediction).item()
        else:  # choose random move
            move_index = rand.randint(0, 2)
        move[move_index] = 1

        return move

    def short_term_memory(self, state, action, next_state, price, game_over):
        self.memory.append((state, action, next_state, price, game_over))

    def long_term_memory(self):
        sample = self.memory if len(self.memory) <= BATCH_SIZE else rand.sample(self.memory, BATCH_SIZE)
        state_list, action_list, next_state_list, price_list, game_over_list = zip(*sample)
        self.trainer.train_step(state_list, action_list, next_state_list, price_list, game_over_list)

    def get_current_state(self, env):
        snake = env.get_snake()
        snake_head = snake[0]

        # determine current snake direction
        snake_direction = env.get_direction
        direction_up, direction_right, direction_down, direction_left = self.get_snake_direction(snake_direction)

        food = env.get_food()

        # get Points around the snake head in all points of the compass
        snake_head_up = Point(snake_head.x, snake_head.y - BLOCK_SIZE)
        snake_head_right = Point(snake_head.x + BLOCK_SIZE, snake_head.y)
        snake_head_down = Point(snake_head.x, snake_head.y + BLOCK_SIZE)
        snake_head_left = Point(snake_head.x - BLOCK_SIZE, snake_head.y)

        state = [
            # Wall or snake ahead
            direction_up and env.has_collided(snake_head_up) or
            direction_right and env.has_collided(snake_head_right) or
            direction_down and env.has_collided(snake_head_down) or
            direction_left and env.has_collided(snake_head_left),

            # Wall or snake to the right
            direction_up and env.has_collided(snake_head_right) or
            direction_right and env.has_collided(snake_head_down) or
            direction_down and env.has_collided(snake_head_left) or
            direction_left and env.has_collided(snake_head_up),

            # Wall or snake to the left
            direction_up and env.has_collided(snake_head_left) or
            direction_right and env.has_collided(snake_head_up) or
            direction_down and env.has_collided(snake_head_right) or
            direction_left and env.has_collided(snake_head_down),

            direction_up, direction_right, direction_down, direction_left,

            food.y < snake_head.y,  # food above snake head
            food.x > snake_head.x,  # food to the right of snake head
            food.y > snake_head.y,  # food below snake head
            food.x < snake_head.x  # food to the left of snake head
        ]

        return np.array(state, dtype=int)

    def get_snake_direction(self, snake_direction):
        # return direction_up, direction_right, direction_down, direction_left
        match snake_direction:
            case Direction.Up:
                return 1, 0, 0, 0
            case Direction.Right:
                return 0, 1, 0, 0
            case Direction.Down:
                return 0, 0, 1, 0
            case Direction.Left:
                return 0, 0, 0, 1
            case _:
                print("There has been an error")
                return 0, 0, 0, 0


def train():
    scores_plot = []
    mean_scores_plot = []
    total = 0
    max_score = 0
    agent = Agent()
    env = SNAKEGAME()

    while True:
        current_state = agent.get_current_state(env)
        action = agent.get_action(current_state)

        game_over, score, price = env.game_iteration(action)
        next_state = agent.get_current_state(env)

        agent.short_term_memory(current_state, action, next_state, price, game_over)
        agent.recall(current_state, action, next_state, price, game_over)

        if game_over:
            env.restart()

            agent.games_played += 1
            agent.long_term_memory()

            if score > max_score:
                max_score = score
                agent.model.save()

            print("Games played: ", agent.games_played, "Score: ", score, "Highscore: ", max_score)

            scores_plot.append(score)
            total += score
            mean_scores_plot.append(total / agent.games_played)
            plot(scores_plot, mean_scores_plot)


if __name__ == '__main__':
    train()
