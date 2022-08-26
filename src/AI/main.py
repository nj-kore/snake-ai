import sys
import time

import numpy as np
import argparse
import torch
import os
import matplotlib.pyplot as plt
#sys.path.append('../Game')
from environment import Environment
from agents import A2CAgent

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model-path', type=str, default=None)
    parser.add_argument('--train', action='store_true')
    args = parser.parse_args()

    render = not args.train

    T = 1000000
    grid_width = 8
    grid_height = 8
    env = Environment(grid_width, grid_height, render=render)
    # agent = A2CAgent(env.state_space, env.action_space, gamma=0.99, lr=3e-2)
    agent = A2CAgent(env.state_space, env.action_space, gamma=0.99, lr=0.005, train=args.train)

    completed_games = 0

    if args.model_path is not None:
        agent.load_model(args.model_path)
        completed_games = int(args.model_path.split('_')[-1])

    observation = env.reset()
    rewards = []
    cum_reward = 0
    next_milestone = 1
    for t in range(T):
        if (t+1) % 2000 == 0:
            print("Iteration: ", t)
            print(np.mean(rewards[-min(len(rewards) - 1, 100):]))

        if args.train:
            if (t+1) % 25000 == 0:
                # render = True
                # env.toggle_render(True)
                agent.save_model(f'saved_models/model_{completed_games}')
        # time.sleep(0.5)
        action = agent.act(observation)

        observation, reward, done = env.step(action)
        cum_reward += reward
        agent.observe(observation, reward, done)

        if done:
            rewards.append(cum_reward)
            if cum_reward >= next_milestone:
                print(f"Snake Length: {env.game_model.snake_length} achieved at Game: {completed_games}!")
                next_milestone = cum_reward + 1
            cum_reward = 0
            observation = env.reset()
            completed_games += 1
            if args.train:
                if render:
                    render = False
                    env.toggle_render(False)


    plt.plot(range(len(rewards)), rewards)
    plt.show()
