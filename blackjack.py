from __future__ import annotations
import gymnasium as gym
from collections import defaultdict

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.patches import Patch
from tqdm import tqdm

env = gym.make("Blackjack-v1",sab = True) #sab: sutton and barto

#let's build an agent:

class BlackjackAgent:
    def __init__(
            self,
            learning_rate:float,
            initial_epsilon:float,
            epsilon_decay:float,
            final_epsilon:float,
            discount_factor:float = 0.95,
                 ) -> None:
        self.q_values = defaultdict(lambda: np.zeros(env.action_space.n))

        self.lr = learning_rate
        self.discount_factor = discount_factor

        self.epsilon = initial_epsilon
        self.epsilon_decay = epsilon_decay
        self.final_epsilon = final_epsilon

        self.training_error = []

    def get_action(self,obs:tuple[int,int,bool]) -> int:

        if np.random.random() < self.epsilon:
            return env.action_space.sample()
        
        else:
            return int(np.argmax(self.q_values[obs]))
        
    def update(
            self,
            obs:tuple[int,int,bool],
            action:int,
            reward:float,
            terminated:bool,
            next_obs:tuple[int,int,bool],
            ):
        future_q_vlaue = (not terminated)* np.max(self.q_values[next_obs])
        temporal_difference = (
            reward + self.discount_factor * future_q_vlaue - self.q_values[obs][action]
        )

        self.q_values[obs][action] = (
            self.q_values[obs][action] + self.lr * temporal_difference)

        self.training_error.append(temporal_difference)

    def decay_epsilon(self):
         self.epsilon = max(self.final_epsilon,self.epsilon - epsilon_decay)

#Now let's build the training loop:

learning_rate = 0.01
n_episodes = 100_000
start_epsilon = 1.0
epsilon_decay = start_epsilon /(n_episodes/2)
final_epsilon = 0.1

agent = BlackjackAgent(
    learning_rate= learning_rate,
    initial_epsilon= start_epsilon,
    epsilon_decay= epsilon_decay,
    final_epsilon= final_epsilon,
)

#Now, we are ready to train!
env = gym.wrappers.RecordEpisodeStatistics(env,deque_size =n_episodes)

for episode in tqdm(range(n_episodes)):
    obs, info = env.reset()
    done = False

    while not done:
        action = agent.get_action(obs)
        next_obs, reward, terminated, truncated, info = env.step(action)

        agent.update(obs,action,reward,terminated, next_obs)

        done = terminated or truncated
        obs = next_obs
    
    agent.decay_epsilon() #we do not decay epsilon during an episode, 
    #only after one is finished.

#let's be able to visualize the training.

###COPY PASTED ###
rolling_length = 500
fig, axs = plt.subplots(ncols=3, figsize=(12, 5))
axs[0].set_title("Episode rewards")
# compute and assign a rolling average of the data to provide a smoother graph
reward_moving_average = (
    np.convolve(
        np.array(env.return_queue).flatten(), np.ones(rolling_length), mode="valid"
    )
    / rolling_length
)
axs[0].plot(range(len(reward_moving_average)), reward_moving_average)
axs[1].set_title("Episode lengths")
length_moving_average = (
    np.convolve(
        np.array(env.length_queue).flatten(), np.ones(rolling_length), mode="same"
    )
    / rolling_length
)
axs[1].plot(range(len(length_moving_average)), length_moving_average)
axs[2].set_title("Training Error")
training_error_moving_average = (
    np.convolve(np.array(agent.training_error), np.ones(rolling_length), mode="same")
    / rolling_length
)
axs[2].plot(range(len(training_error_moving_average)), training_error_moving_average)
plt.tight_layout()
plt.show()


