from env.sarsapig import PigEnvSarsa
import numpy as np
from collections import defaultdict
#from tqdm import tqdm

#This is Q-Learning bitch!
q_values = defaultdict(lambda:0) #a default dictionary for all states, this means we only keep the values for the states we visit. 
                                              #This means we can easily use their values in recurrent formulas without worrying about errors.
        


import time

#This stochastic policy ties with it's own counter part.
def stochastic_policy(observation):
    return np.random.randint(0,2)


#we want to use another policy, called: hold until 21 policy.
#has a success rate of 96% against random chance.
#if both are using an optimal policy, then, since the agent goes
#first, it has an advantage and wins.
def agent_policy(observation):
    if observation[2] > 23:
        return PigEnvSarsa.BANK
    else:
        return PigEnvSarsa.ROLL
         
env = PigEnvSarsa(max_turns=30,opponent_policy=stochastic_policy) #setting this to agent policy will not work
                                                             # as observation[2] is the agent's buffer not the opponent's.

observation, info = env.reset()



print(observation)

print("action space ", env.action_space)
print("observation space ", env.observation_space)

rewards = []
#epsilon = 0.05

#N of possible observations 
#does it make more sense to use linear function approximation? let's try


#q_table = np.zeros([env.observation_space.n, env.action_space.n])

for i in range (3):    
    
    terminated = False
    truncated = False
    while not terminated and not truncated:
        
        #epsilon greedy
        if np.random.random() > env.epsilon: 
            action = agent_policy(observation)
        else:
            action = np.random.randint(0,2)
        next_observation, reward, terminated, truncated, info = env.step(action)

       
        time.sleep(0.4)
        
        
        print(env.observation_space)
        print(env.observation)

        #print("Visible Game State:",observation, reward, terminated, truncated, info)
        #print("Game Points:", env.points)
    rewards.append(reward)
    env.reset()
    #print("A reset occured!")
    
        
print("Policy Success Rate:",sum(rewards)/len(rewards)*100)

env.close()