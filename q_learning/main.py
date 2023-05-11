from env.q_pig import PigEnv
import numpy as np
from collections import defaultdict
from tqdm import tqdm
#from tqdm import tqdm

#This is Q-Learning bitch!
q_table = defaultdict(lambda:0) #a default dictionary for all states, this means we only keep the values for the states we visit. 
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
        return PigEnv.BANK
    else:
        return PigEnv.ROLL
         
env = PigEnv(max_turns=30,opponent_policy=stochastic_policy,epsilon = 0.2,learning_rate=0.15) #setting this to agent policy will not work
                                                             # as observation[2] is the agent's buffer not the opponent's.

observation, info = env.reset()



print(observation)

#print("action space ", env.action_space)
#print("observation space ", env.observation_space)

rewards = []
#epsilon = 0.05
#q_table = np.zeros([env.observation_space.n, env.action_space.n])

for i in tqdm(range(10000)):    
    state,_ = env.reset() #env reset returns observation, info

    terminated = False
    truncated = False
    while not terminated and not truncated:
        
        #epsilon greedy
        if np.random.random() > env.epsilon: 
            action = agent_policy(observation)
        else:
            action = np.random.randint(0,2)
        next_observation, reward, terminated, truncated, info = env.step(action)

        old_value = q_table[state, action]
        #Take the maximum over all possible actions in the next state.
        next_max = np.max([q_table[next_observation, PigEnv.ROLL],q_table[next_observation,PigEnv.BANK]])

        new_value = (1 - env.alpha) * old_value + env.alpha * (reward + env.gamma * next_max)
        #print(new_value)
        
        q_table[state, action] = new_value
        state = next_observation
        #print(env.observation_space)
        #print(env.observation)

        #print("Visible Game State:",observation, reward, terminated, truncated, info)
        #print("Game Points:", env.points)
    rewards.append(reward)
    
    #print("A reset occured!")
    
print(len(q_table))
print(np.max(list(q_table.values()))) #the value of the q_tables is stuck at the learning rate, this probably means each state is rarely vistied again...
       
#print("Policy Success Rate:",sum(rewards)/len(rewards)*100)

env.close()