from Game import model, view

class Environment:
    def __init__(self, render = False):
        self.game_model = model.SnakeModel()

        if render:
            self.game_view = view.SnakeView(self.game_model)

    def step(self, action):
        self.game_model.change_direction(action)
        reward_data_before = extract_reward_data(self.game_model)
        self.game_model.step()
        reward_data_after = extract_reward_data(self.game_model)
        reward = calculate_reward(reward_data_before, reward_data_after)
        state = extract_state(self.game_model)
        done = self.game_model.game_status == -1
        return state, reward, done

    def reset(self):
        self.game_model.reset()
        return extract_state(self.game_model)



class RewardData:
    def __init__(self, snake_length, game_status):
       self.snake_length = snake_length
       self.game_status = game_status


def calculate_reward(data_before: RewardData, data_after: RewardData):
    if data_after.game_status == -1:
        return -1
    return data_after.snake_length - data_before.snake_length

"""
BODY_PLANE = 0
HEAD_PLANE = 1
FRUIT_PLANE = 2
"""

def extract_state(game_model):
    player_body = list(game_model.player_body)
    player_head = list(game_model.player_head)
    fruit = list(game_model.fruit)
    """
    state = [[[0 for i in range(game_model.grid_width + 2)] for j in range(game_model.grid_height + 2)]
             for k in range(3)]

    for pos in player_body:
        state[BODY_PLANE][pos[0] + 1][pos[1] + 1] = 1
    state[HEAD_PLANE][player_head[0] + 1][player_head[1] + 1] = 1
    state[FRUIT_PLANE][fruit[0] + 1][fruit[1] + 1] = 1
    """
    return [player_head, player_body, fruit]


def extract_reward_data(game_model):
    return RewardData(snake_length=game_model.snake_length, game_status=game_model.game_status)



