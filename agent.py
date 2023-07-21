import random
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense


class Brain:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.model = self._create_model()

    def _create_model(self):
        model = Sequential()
        model.add(Dense(64, input_dim=self.state_size, activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer='adam')
        return model

    def save_model(self, model_name):
        self.model.save(model_name)

    def train(self, x, y, epoch=1, verbose=0):
        self.model.fit(x, y, epochs=epoch, verbose=verbose)

    def predict(self, s):
        return self.model.predict(s)

    def predict_one(self, s):
        return self.predict(s.reshape(1, self.state_size)).flatten()


class ExpReplay:
    def __init__(self, capacity):
        self.capacity = capacity
        self.memory = []

    def add(self, sample):
        self.memory.append(sample)
        if len(self.memory) > self.capacity:
            self.memory.pop(0)

    def sample(self, n):
        n = min(n, len(self.memory))
        return random.sample(self.memory, n)


class Agent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.brain = Brain(self.state_size, self.action_size)
        self.memory = ExpReplay(capacity=1000)
        self.epsilon = 1.0
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.01
        self.batch_size = 512

    def save_model(self, model_name):
        self.brain.save_model(model_name)

    def act(self, s):
        if np.random.rand() <= self.epsilon:
            return np.random.choice(self.action_size)
        else:
            return np.argmax(self.brain.predict_one(s))

    def capture_sample(self, sample):
        self.memory.add(sample)

    def process(self):
        if len(self.memory.memory) < self.batch_size:
            return

        no_state = np.zeros(self.state_size)

        batch = self.memory.sample(self.batch_size)
        states = np.array([sample[0] for sample in batch])
        next_states = np.array([(no_state if sample[3] is None else sample[3]) for sample in batch])

        predicted_q = self.brain.predict(states)
        predicted_next_q = self.brain.predict(next_states)

        x = np.zeros((len(batch), self.state_size))
        y = np.zeros((len(batch), self.action_size))

        for i in range(len(batch)):
            batch_item = batch[i]

            state = batch_item[0]
            action = batch_item[1]
            reward = batch_item[2]
            next_state = batch_item[3]

            target_q = predicted_q[i]
            if next_state is None:
                target_q[action] = reward  # An End state Q[S,A]assumption
            else:
                target_q[action] = reward + 0.95 * np.amax(predicted_next_q[i])

            x[i] = state
            y[i] = target_q

        self.brain.train(x, y)

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
