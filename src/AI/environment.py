from Game import model, view, controller

class Environment:
    def __init__(self, render = False):
        self.game_model = model.SnakeModel()

        if render:
            self.game_view = view.SnakeView(self.game_model)

    def step(self, action):
        self.game_model.change_direction(action)
        reward_data_before = self.extract_reward_data()
        self.game_model.step()
        reward_data_after = self.extract_reward_data()
        reward = calculate_reward(reward_data_before, reward_data_after)
        state = self.extract_state()
        done = self.game_model.game_status == -1
        return state, reward, done

    def extract_state(self):
        player_body = self.game_model.player_body
        player_head = self.game_model.player_head
        fruit = self.game_model.fruit
        state = [[0 for i in range(self.game_model.grid_width + 2)] for j in range(self.game_model.grid_height + 2)]
        for pos in player_body:
            state[pos[0] + 1][pos[1] + 1] = 1
        state[player_head[0] + 1][player_head[1] + 1] = 2
        state[fruit[0] + 1][fruit[1] + 1] = -1
        return state


    def extract_reward_data(self):
        return RewardData(snake_length=self.game_model.snake_length, game_status=self.game_model.game_status)

    def reset(self):
        self.game_model.reset()
        return self.extract_state()



class RewardData:
    def __init__(self, snake_length, game_status):
       self.snake_length = snake_length
       self.game_status = game_status


def calculate_reward(data_before: RewardData, data_after: RewardData):
    if data_after.game_status == -1:
        return -1
    return data_after.snake_length - data_before.snake_length



