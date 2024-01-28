import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as funct
import os


class QTrainer:
    def __init__(self, model, lr, gamma):
        self.model = model
        self.lr = lr
        self.gamma = gamma
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

    def training_step(self, state, action, next_state, prize, game_over):
        state = torch.tensor(state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        next_state = torch.tensor(next_state, dtype=torch.float)
        prize = torch.tensor(prize, dtype=torch.float)

        if len(state.shape) == 1:
            state = torch.unsqueeze(state, 0)
            action = torch.unsqueeze(action, 0)
            next_state = torch.unsqueeze(next_state, 0)
            game_over = (game_over,)

        prediction = self.model(state)
        target = prediction.clone()
        for i in range(len(game_over)):
            Q_new = prize[i]
            if not game_over[i]:
                Q_new = Q_new + self.gamma * torch.max(self.model(next_state[i]))

            target[i][torch.argmax(action[i]).item()] = Q_new

        self.optimizer.zero_grad()
        self.criterion(target, prediction).backward()

        self.optimizer.step()


class Linear_QNet(nn.Module):
    def __init__(self, input_len, hidden_len, output_len):
        super().__init__()
        self.linear_1 = nn.Linear(input_len, hidden_len)
        self.linear_2 = nn.Linear(hidden_len, output_len)

    def forward(self, x):
        x = funct.relu(self.linear_1(x))
        return self.linear_2(x)

    def save(self, file='model.path'):
        path_to_folder = './model'
        if not os.path.exists(path_to_folder):
            os.mkdir(path_to_folder)
        file = os.path.join(path_to_folder, file)
        torch.save(self.state_dict(), file)
