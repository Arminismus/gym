

from ..env.pig import PigEnv
import numpy as np
from tqdm import tqdm

import time

#This stochastic policy ties with it's own counter part.
def stochastic_policy(observation):
    return np.random.randint(0,2)


#we want to use another policy, called: hold until 21 policy.
#has a success rate of 96% against random chance.
#if both are using an optimal policy, then, since the agent goes
#first, it has an advantage and wins.
def agent_policy(observation,k):
    if observation[2] > k:
        return PigEnv.BANK
    else:
        return PigEnv.ROLL
         
env = PigEnv(max_turns=30,opponent_policy=stochastic_policy)
observation, info = env.reset()



print(observation)

print("action space ", env.action_space)
print("observation space ", env.observation_space)

rewards = []
rates = []
for k in tqdm(range(0,100)):
    for _ in range(10000):
    
    
        terminated = False
        truncated = False
        while not terminated and not truncated:
            #action = stochastic_policy(observation)
            action = agent_policy(observation,k)
            observation, reward, terminated, truncated, info = env.step(action)
            #time.sleep(0.5)

            #print("Visible Game State:",observation, reward, terminated, truncated, info)
            #print("Game Points:", env.points)
        rewards.append(reward)
        env.reset()
        #print("A reset occured!")
    
    
    rates.append(sum(rewards)/len(rewards)*100)

print(np.argmax(rates))
env.close()