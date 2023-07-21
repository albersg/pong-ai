import random
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import tensorflow as tf

# Define a Brain class that represents the neural network model for the agent.
class Brain:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.model = self._create_model()

    def _create_model(self):
        # Create a feedforward neural network model using Keras Sequential API.
        model = Sequential()
        # Add a fully connected hidden layer with 64 neurons and ReLU activation function.
        model.add(Dense(64, input_dim=self.state_size, activation='relu'))
        # Add another fully connected hidden layer with 32 neurons and ReLU activation function.
        model.add(Dense(32, activation='relu'))
        # Add the output layer with 'action_size' neurons and a linear activation function.
        model.add(Dense(self.action_size, activation='linear'))
        # Compile the model using mean squared error (MSE) loss and Adam optimizer.
        model.compile(loss='mse', optimizer='adam')
        return model

    def save_model(self, model_name):
        # Save the model to a file.
        self.model.save(model_name)

    def load_model(self, model_name):
        # Load the model from a file.
        self.model = tf.keras.models.load_model(model_name)

    def train(self, x, y, epoch=1, verbose=0):
        # Train the model on input data 'x' and target labels 'y' for 'epoch' number of epochs.
        self.model.fit(x, y, epochs=epoch, verbose=verbose)

    def predict(self, s):
        # Make predictions using the model for a given input 's'.
        return self.model.predict(s)

    def predict_one(self, s):
        # Make a single prediction using the model for a given input 's'.
        return self.predict(s.reshape(1, self.state_size)).flatten()


# Define an Experience Replay (ExpReplay) class to store and manage agent's experiences.
class ExpReplay:
    def __init__(self, capacity):
        # Initialize the capacity and an empty memory list to store experiences.
        self.capacity = capacity
        self.memory = []

    def add(self, sample):
        # Add a new experience sample to the memory.
        self.memory.append(sample)
        if len(self.memory) > self.capacity:
            # If the memory exceeds the capacity, remove the oldest experience.
            self.memory.pop(0)

    def sample(self, n):
        # Sample 'n' experiences randomly from the memory.
        n = min(n, len(self.memory))
        return random.sample(self.memory, n)


# Define an Agent class that represents the reinforcement learning agent.
class Agent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        # Create a Brain (neural network) for the agent to make decisions.
        self.brain = Brain(self.state_size, self.action_size)
        # Create an Experience Replay buffer to store agent's experiences.
        self.memory = ExpReplay(capacity=1000)
        self.epsilon = 1.0  # Exploration rate - starts high to encourage exploration
        self.epsilon_decay = 0.995  # Decay rate for exploration rate
        self.epsilon_min = 0.01  # Minimum exploration rate
        self.batch_size = 512  # Batch size for training the neural network

    def save_model(self, model_name):
        # Save the agent's neural network model to a file.
        self.brain.save_model(model_name)

    def load_model(self, model_name):
        # Load the agent's neural network model from a file.
        self.brain.load_model(model_name)

    def act(self, s):
        # The agent takes an action based on the current state 's'.
        # With probability 'epsilon', it explores by selecting a random action,
        # otherwise, it exploits the learned knowledge by choosing the best action.
        if np.random.rand() <= self.epsilon:
            return np.random.choice(self.action_size)  # Explore: choose a random action
        else:
            return np.argmax(self.brain.predict_one(s))  # Exploit: choose the best action

    def capture_sample(self, sample):
        # Capture a new experience sample and store it in the memory buffer.
        self.memory.add(sample)

    def process(self):
        # Process a batch of experiences from the memory and use them for training.
        if len(self.memory.memory) < self.batch_size:
            return

        no_state = np.zeros(self.state_size)  # Dummy state for the terminal state

        # Sample a batch of experiences from the memory.
        batch = self.memory.sample(self.batch_size)

        # Extract states, actions, rewards, and next states from the batch.
        states = np.array([sample[0] for sample in batch])
        next_states = np.array([(no_state if sample[3] is None else sample[3]) for sample in batch])
        rewards = np.array([sample[2] for sample in batch])

        # Predict the Q-values for the current states and the next states.
        predicted_q = self.brain.predict(states)
        predicted_next_q = self.brain.predict(next_states)

        x = np.zeros((len(batch), self.state_size))
        y = np.zeros((len(batch), self.action_size))

        # Prepare the training data for the neural network.
        for i in range(len(batch)):
            batch_item = batch[i]

            state = batch_item[0]
            action = batch_item[1]
            reward = batch_item[2]
            next_state = batch_item[3]

            target_q = predicted_q[i]
            if next_state is None:
                target_q[action] = reward  # For the terminal state, set the Q-value to the received reward.
            else:
                target_q[action] = reward + 0.95 * np.amax(predicted_next_q[i])
                # For non-terminal states, set the Q-value to the immediate reward plus
                # a discounted maximum Q-value for the next state.

            x[i] = state
            y[i] = target_q

        # Train the neural network using the prepared data.
        self.brain.train(x, y)

        # Decay the exploration rate to encourage more exploitation over time.
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
