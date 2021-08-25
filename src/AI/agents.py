import torch
from networks import Net
from torch.distributions import Categorical

class BaseAgent:
    def observe(self, observation, reward, done):
        pass

    def act(self, observation):
        return 0


class A2CAgent(BaseAgent):
    def __init__(self, input_space, action_space):
        self.input_space = input_space
        self.gamma = 0.99
        self.lr = 0.001
        self.prev_state = None
        self.prev_action = None
        self.net = Net(input_space, action_space)
        self.optimizer = torch.optim.Adam(self.net.parameters(), lr=self.lr)

    def observe(self, observation, reward, done):
        state = observation

    def act(self, observation):
        state = observation
        probs, state_value = self.net(state)

        # create a categorical distribution over the list of probabilities of actions
        m = Categorical(probs)

        # and sample an action using the distribution
        action = m.sample()

        self.prev_action = action
        self.prev_state = state

        return action








