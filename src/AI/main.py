import sys
sys.path.append('../Game')
from environment import Environment
from agents import A2CAgent
import time
import torch
import matplotlib.pyplot as plt

if __name__ == "__main__":
    T = 100000
    grid_width = 8
    grid_height = 8
    env = Environment(grid_width, grid_height, render=False)
    agent = A2CAgent(env.state_space, env.action_space, gamma=0.99, lr=3e-2)
    observation = env.reset()
    rewards = []
    cum_reward = 0
    for t in range(T):
        if t % 500 == 0:
            print("Iteration: ", t)
        #time.sleep(0.5)
        action = agent.act(observation)

        observation, reward, done = env.step(action)
        cum_reward += reward
        agent.observe(observation, reward, done)

        if done:
            rewards.append(cum_reward)
            cum_reward = 0
            observation = env.reset()

    plt.plot(range(len(rewards)), rewards)
    plt.show()