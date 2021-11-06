import sys
sys.path.append('../Game')
from environment import Environment
from agents import A2CAgent
import time
import torch

if __name__ == "__main__":
    T = 1000
    grid_width = 8
    grid_height = 8
    env = Environment(grid_width, grid_height, render=False)
    agent = A2CAgent(env.state_space, env.action_space, gamma=0.99, lr=3e-2)
    observation = env.reset()
    for t in range(T):
        #time.sleep(0.5)
        action = agent.act(observation)

        observation, reward, done = env.step(action)

        agent.observe(observation, reward, done)

        if done:
            observation = env.reset()

