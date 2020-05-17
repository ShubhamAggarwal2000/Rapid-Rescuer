import gym
import random

env = gym.make("CartPole-v1")
print(env.action_space.sample())

def random_game():

    for episode in range(10):
        env.reset()

        for t in range(500):
            env.render()
            action = env.action_space.sample()

            next_state , reward , done , info = env.step(action=action)
            print(t , next_state , reward , done , info , action)

            if done :
                break

random_game()