from env.q_pig import PigEnv
import numpy as np

from collections import defaultdict
from tqdm import tqdm

#import matplotlib.pyplot as plt
from tables.savetable import save,load
from configs.config import config


_load = config['load']
if _load:
    q_table = load('q_table')
else:
    q_table = config['q_table']

opponent_policy = config['opponent_policy']
agent_policy = config['agent_policy']
_save = config['save']
gamma = config['discount_factor']


save_name = config['save_name']
max_turns = config['max_turns']
iterations = config['iterations']
learning_rate = config['learning_rate']
random_policy = config['random_policy']
rewards = []



    #create environment
    
env = PigEnv(max_turns=max_turns,opponent_policy=opponent_policy,learning_rate = learning_rate,discount_factor= gamma)

    
    #reset the environment
observation, info = env.reset()
for _ in tqdm(range(iterations)):
    state,_ = env.reset()
        
    terminated = False
    truncated = False
    while not terminated and not truncated:
            
        if np.random.random() > env.epsilon: 
            action = agent_policy(observation)
        else:
            action = np.random.randint(0,2)
            
        next_observation, reward, terminated, truncated, info = env.step(action)
        old_value = q_table[state,action]
        next_max = np.max([q_table[next_observation, PigEnv.ROLL],q_table[next_observation,PigEnv.BANK]])
        new_value = (1 - env.alpha) * old_value + env.alpha * (reward + env.gamma * next_max)
            
        q_table[state, action] = new_value
        observation = next_observation
        
    rewards.append(reward)
    
    
if _save:
    save(q_table,save_name)
print(sum(rewards)/len(rewards))



