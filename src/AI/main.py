import sys
sys.path.append('../Game')
import time
from environment import Environment

if __name__ == "__main__":
    T = 10
    env = Environment(render=True)
    observation = env.reset()
    for t in range(T):
        time.sleep(env.game_model.game_tick_seconds)
        action = 0
        observation, reward, done = env.step(action)
        if done:
            observation = env.reset()

