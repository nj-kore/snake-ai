import sys
import time

import numpy as np
import torch
import os
import matplotlib.pyplot as plt
#sys.path.append('../Game')
from environment import Environment
from agents import A2CAgent

if __name__ == "__main__":
    T = 1000000
    grid_width = 8
    grid_height = 8
    env = Environment(grid_width, grid_height, render=False)
    # agent = A2CAgent(env.state_space, env.action_space, gamma=0.99, lr=3e-2)
    agent = A2CAgent(env.state_space, env.action_space, gamma=0.999, lr=3e-5)
    observation = env.reset()
    rewards = []
    cum_reward = 0
    completed_games = 0
    next_milestone = 1
    for t in range(T):
        if (t+1) % 2000 == 0:
            print("Iteration: ", t)
            print(np.mean(rewards[:-min(completed_games, 100)]))
        # time.sleep(0.5)
        action = agent.act(observation)

        observation, reward, done = env.step(action)
        cum_reward += reward
        agent.observe(observation, reward, done)

        if done:
            rewards.append(cum_reward)
            if cum_reward >= next_milestone:
                print(f"Snake Length: {cum_reward} achieved at Game: {completed_games}!")
                next_milestone = cum_reward + 1
            cum_reward = 0
            observation = env.reset()
            completed_games += 1

    plt.plot(range(len(rewards)), rewards)
    plt.show()
