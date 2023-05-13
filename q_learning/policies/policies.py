import numpy as np
from env.q_pig import PigEnv

def stochastic_policy(observation):
    return np.random.randint(0,2)

def heuristic_agent_policy(observation):
    if observation[2] > 23:
        return PigEnv.BANK
    else:
        return PigEnv.ROLL
def heuristic_opponent_policy(observation):
    if observation[3] > 23:
        return PigEnv.BANK
    else:
        return PigEnv.ROLL
#def q_policy(observation):
    #return np.argmax(q_table[observation])