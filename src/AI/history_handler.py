import numpy as np

class HistoryHandler:
    def __init__(self, max_length):
        self.max_length = max_length
        self.current_length = 0

        self.state_history = []
        self.action_history = []
        self.reward_history = []
        self.done_history = []


    def insert(self, state, action, reward, done):
        self.state_history.append(state)
        self.action_history.append(action)
        self.reward_history.append(reward)
        self.done_history.append(done)

        self.current_length += 1
        if self.current_length > self.max_length:
            self.current_length -= 1
            self.state_history.pop(0)
            self.action_history.pop(0)
            self.reward_history.pop(0)
            self.done_history.pop(0)

    def clear(self):
        self.__init__(self.max_length)

