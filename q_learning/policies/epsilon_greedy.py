import numpy as np

def epsilon_greedy(env,policy,observation,random_policy):
    if np.random.random() > env.epsilon: 
        return policy(observation)
    else:
        return random_policy(observation)