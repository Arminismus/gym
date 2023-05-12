import numpy as np

def epsilon_greedy(env,policy,observation,random_policy):
    if np.random.random() > env.epsilon: 
        action = policy(observation)
    else:
        action = np.random.randint(0,2)
    return action