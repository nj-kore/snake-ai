import torch
import torch.nn.functional as F
import numpy as np
from networks import Net
from torch.distributions import Categorical
from history_handler import HistoryHandler
from collections import namedtuple

"""
if self.t > self.td_n_steps:
    state_to_update = self.history_handler.state_history[-self.td_n_steps]
    cum_reward = 0
    for i in range(self.td_n_steps):
        cum_reward += (self.gamma ** i) * self.history_handler.reward_history[-self.td_n_steps + i]
"""

eps = np.finfo(np.float32).eps.item()

SavedAction = namedtuple('SavedAction', ['log_prob', 'value'])


class BaseAgent:
    def observe(self, observation, reward, done):
        pass

    def act(self, observation):
        return 0


class A2CAgent(BaseAgent):
    def __init__(self, input_space, action_space, gamma, lr, train=True):
        self.t = 0
        self.input_space = input_space
        self.gamma = gamma
        self.prev_state = None
        self.prev_action = None
        self.model = Net(input_space, action_space)
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=lr)
        # self.history_handler = HistoryHandler(max_length=None)
        self.saved_actions = []
        self.saved_rewards = []
        self.reward_timer = 0
        self.reward_timer_threshold = 100
        self.train = train
        if not self.train:
            # Arbitrary big value
            self.reward_timer_threshold = 1e7

    def observe(self, observation, reward, done):
        if reward > 0:
            self.reward_timer = 0

        self.saved_rewards.append(reward)
        if done:
            self.reward_timer = 0
            if self.train:
                self.finish_episode()
            # reset rewards and action buffer
            del self.saved_rewards[:]
            del self.saved_actions[:]

    def act(self, observation):
        state = observation
        # print(state)
        probs, state_value = self.model(state)
        # create a categorical distribution over the list of probabilities of actions
        m = Categorical(probs)

        # and sample an action using the distribution
        action = m.sample()

        self.reward_timer += 1
        if self.reward_timer >= self.reward_timer_threshold:
            action = torch.tensor([0])

        self.saved_actions.append(SavedAction(m.log_prob(action), state_value))

        self.prev_action = action
        self.prev_state = state

        return action

    def finish_episode(self):
        """
        Training code. Calculates actor and critic loss and performs backprop.
        """
        R = 0
        saved_actions = self.saved_actions
        policy_losses = []  # list to save actor (policy) loss
        value_losses = []  # list to save critic (value) loss
        returns = []  # list to save the true values

        # calculate the true value using rewards returned from the environment
        for r in self.saved_rewards[::-1]:
            # calculate the discounted value
            R = r + self.gamma * R
            returns.insert(0, R)

        returns = torch.tensor(returns)
        if len(self.saved_rewards) == 1:
            returns = (returns - returns.mean())
        else:
            returns = (returns - returns.mean()) / (returns.std() + eps)

        for (log_prob, value), R in zip(saved_actions, returns):
            advantage = R - value.item()

            # calculate actor (policy) loss
            policy_losses.append(-log_prob * advantage)
            # calculate critic (value) loss using L1 smooth loss
            value_losses.append(F.smooth_l1_loss(value[0], torch.Tensor([R])))

        # reset gradients
        self.optimizer.zero_grad()

        # sum up all the values of policy_losses and value_losses
        loss = torch.stack(policy_losses).sum() + torch.stack(value_losses).sum()
        # perform backprop
        loss.backward()
        self.optimizer.step()


    def save_model(self, path):
        # Save parameters of ML model
        torch.save(self.model.state_dict(), path)

    def load_model(self, path):
        # Load parameters of ML model
        self.model.load_state_dict(torch.load(path))

    """
    def get_history_handler(self):
        return self.history_handler
    """
