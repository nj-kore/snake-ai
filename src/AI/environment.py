import time

from Game.model import SnakeModel
from Game.view import SnakeView
import torch

BODY_PLANE = 0
HEAD_PLANE = 1
FRUIT_PLANE = 2


class Environment:
    def __init__(self, grid_width, grid_height, render):
        self.game_model = SnakeModel(grid_width, grid_height)
        self.state_space = [3, self.game_model.grid_width + 2, self.game_model.grid_height + 2]
        self.action_space = 4
        self.render = False
        self.game_view = None

        if render:
            self.toggle_render(True)

    def step(self, action):
        if self.render:
            time.sleep(0.25)
        self.game_model.change_direction(action)
        reward_data_before = extract_reward_data(self.game_model)
        self.game_model.step()
        reward_data_after = extract_reward_data(self.game_model)
        reward = calculate_reward(reward_data_before, reward_data_after)
        state = self.extract_state(self.game_model)
        done = self.game_model.game_status == -1
        return state, reward, done

    def reset(self):
        self.game_model.reset()
        # if self.render:
        # self.game_view.draw_game()
        return self.extract_state(self.game_model)

    def extract_state(self, game_model):
        player_body = list(game_model.player_body)
        player_head = list(game_model.player_head)
        fruit = list(game_model.fruit)
        state_tensor = torch.zeros([1, *self.state_space])

        for pos in player_body:
            state_tensor[0][BODY_PLANE][pos[0] + 1][pos[1] + 1] = 1

        state_tensor[0][HEAD_PLANE][player_head[0] + 1][player_head[1] + 1] = 1
        state_tensor[0][FRUIT_PLANE][fruit[0] + 1][fruit[1] + 1] = 1

        return state_tensor

    def toggle_render(self, render):
        if render:
            if self.render:
                # Already rendering
                return
            self.render = True
            self.game_view = SnakeView(self.game_model)
        else:
            if not self.render:
                # Already not rendering
                return
            self.render = False
            self.game_view.kill_view()


class RewardData:
    def __init__(self, snake_length, game_status):
        self.snake_length = snake_length
        self.game_status = game_status


def calculate_reward(data_before: RewardData, data_after: RewardData):
    if data_after.game_status == -1:
        return -1
    return 10*(data_after.snake_length - data_before.snake_length)


def extract_reward_data(game_model):
    return RewardData(snake_length=game_model.snake_length, game_status=game_model.game_status)
