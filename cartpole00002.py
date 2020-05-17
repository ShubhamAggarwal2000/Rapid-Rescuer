import os
import random
import gym
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

import numpy as np
from collections import deque
from keras.models import Model, load_model
from keras.layers import Input, Dense
from keras.optimizers import Adam, RMSprop


def Modelnn(input_shape, action_space):
    x_input = Input(input_shape)

    x = Dense(512, input_shape=input_shape, activation='relu', kernel_initializer='he_uniform')(x_input)

    x = Dense(256, activation='relu', kernel_initializer='he_uniform')(x)
    x = Dense(64, activation='relu', kernel_initializer='he_uniform')(x)
    x = Dense(action_space, activation="linear", kernel_initializer='he_uniform')(x)

    model = Model(inputs=x_input, outputs=x, name="cartpolednnv1")
    model.compile(loss="mse", optimizer=RMSprop(lr=0.00025, rho=0.95, epsilon=0.01), metrics=["accuracy"])
    model.summary()
    return model


class dqnagent:

    def __init__(self):
        self.env = gym.make("CartPole-v1")
        self.state_size = self.env.observation_space.shape[0]
        self.action_size = self.env.action_space.n
        self.n_episodes = 1000
        self.memory = deque(maxlen=2000)

        self.gamma = 0.95  # discount factor
        self.epsilon = 1.0  # exploration
        self.epsilon_min = 0.001
        self.epsilon_decay = 0.99
        self.batch_size = 64
        self.train_start = 1000

        self.model = Modelnn(input_shape=(self.state_size,), action_space=self.action_size)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

        if len(self.memory) > self.train_start:
            if self.epsilon > self.epsilon_min:
                self.epsilon = self.epsilon * self.epsilon_decay

    def act(self, state):
        if np.random.random() <= self.epsilon:
            return random.randrange(self.action_size)

        else:
            return np.argmax(self.model.predict(state))

    def replay(self):
        if len(self.memory) < self.train_start:
            return
        minibatch = random.sample(self.memory, min(len(self.memory), self.batch_size))

        state = np.zeros((self.batch_size, self.state_size))
        next_state = np.zeros((self.batch_size, self.state_size))

        action, reward, done = [], [], []

        for i in range(self.state_size):
            state[i] = minibatch[i][0]
            action.append(minibatch[i][1])
            reward.append(minibatch[i][2])
            next_state[i] = minibatch[i][3]
            done.append(minibatch[i][4])

        target = self.model.predict(state)
        target_next = self.model.predict(next_state)

        for i in range(self.batch_size):
            if done[i]:

                target[i][action[i]] = reward[i]

            else:

                target[i][action[i]] = reward[i] + self.gamma * (np.amax(target_next[i]))

            self.model.fit(state, target, batch_size=self.batch_size, verbose=0)

    def load(self, name):
        self.model = load_model(name)

    def save(self, name):
        self.model.save(name)

    def run(self):

        for episode in range(self.n_episodes):
            state = self.env.reset()
            state = np.reshape(state, [1, self.state_size])
            done = False
            i = 0

            while not done:
                # self.env.render()
                action = self.act(state)
                next_state, reward, done, _ = self.env.step(action=action)
                next_state = np.reshape(next_state, [1, self.state_size])

                if not done or i == self.env._max_episode_steps - 1:
                    reward = reward

                else:
                    reward = -100
                self.remember(state, action, reward, next_state, done)
                state = next_state
                i = i + 1

                if done:
                    print("episode : {}/{} , score: {} ,e:{:.2}".format(episode, self.n_episodes, i, self.epsilon))

                    if i == 500:
                        print("Saving trained model as cartpole-dqn.h5")
                        self.save("cartpole0001-dqn.h5")
                        return
                self.replay()

    def test(self):
        self.load("cartpole0001-dqn.h5")

        for ep in range(self.n_episodes):
            state = self.env.reset()
            state = np.reshape(state, [1, self.state_size])
            done = False
            i = 0

            while not done:
                self.env.render()
                action = np.argmax(self.model.predict(state))
                next_state, reward, done, _ = self.env.step(action)
                state = np.reshape(next_state, [1, self.state_size])
                i = i + 1

                if done:
                    print("episode : {}/{} , score: {} ".format(episode, self.n_episodes, i))
                    break


if __name__ == "__main__":
    agent = dqnagent()
    agent.run()
    # agent.test()
