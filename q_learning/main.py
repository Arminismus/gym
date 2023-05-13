from env.q_pig import PigEnv
import numpy as np
from collections import defaultdict
from tqdm import tqdm
import matplotlib.pyplot as plt
from tables.savetable import save,load
from policies.epsilon_greedy import epsilon_greedy





#This is Q-Learning bitch!
#q_table = defaultdict(lambda:0) 
# #a default dictionary for all states, this means we only keep the values for the states we visit.                                               
#This means we can easily use their values in recurrent formulas without worrying about errors.   
q_table = load('q_table')
import time

#This stochastic policy ties with it's own counter part.
def stochastic_policy(observation):
    return np.random.randint(0,2)

def heuristic_agent_policy(observation):
    if observation[2] > 23:
        return PigEnv.BANK
    else:
        return PigEnv.ROLL
def heuristic_opponent_policy(observation):
    if env.buffers[0] > 23:
        return PigEnv.BANK
    else:
        return PigEnv.ROLL
        
         
env = PigEnv(max_turns=300,opponent_policy=heuristic_opponent_policy,epsilon = 0.4,learning_rate=0.03) #setting this to agent policy will not work
                                                             # as observation[2] is the agent's buffer not the opponent's.

observation, info = env.reset()


def q_policy(observation):
    return np.argmax(q_table[observation])

rewards = []

for i in tqdm(range(100_000)):    
    state,_ = env.reset() #env reset returns observation, info

    terminated = env.terminated
    truncated = env.truncated
    while not terminated and not truncated:
        
        #epsilon greedy
        action = epsilon_greedy(env,policy = q_policy,observation = observation,random_policy = stochastic_policy)
        next_observation, reward, terminated, truncated, info = env.step(action)

        old_value = q_table[state, action]
        
        ##Take the maximum over all possible actions in the next state.
        next_max = np.max([q_table[next_observation, PigEnv.ROLL],q_table[next_observation,PigEnv.BANK]])

        new_value = (1 - env.alpha) * old_value + env.alpha * (reward + env.gamma * next_max)
               
        q_table[state, action] = new_value
        observation = next_observation
      
    rewards.append(reward)
    
save(q_table,'q_table')

print(sum(rewards)/len(rewards))

env.close()