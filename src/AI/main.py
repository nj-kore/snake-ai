import sys
sys.path.append('../Game')
from environment import Environment
from agents import A2CAgent
import time


if __name__ == "__main__":
    T = 100
    grid_width = 8
    grid_height = 8
    env = Environment(grid_width, grid_height, render=True)
    agent = A2CAgent(env.state_space, env.action_space)
    observation = env.reset()
    for t in range(T):
        time.sleep(0.5)
        action = agent.act(observation)

        observation, reward, done = env.step(action)

        agent.observe(observation, reward, done)

        if done:
            observation = env.reset()

