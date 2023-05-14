import numpy as np
from env.q_pig import PigEnv
#from configs.config import q_table
from tables.savetable import q_table
from numba import jit

@jit(nopython = True)
def stochastic_policy(observation):
    return np.random.randint(0,2)

@jit(nopython = True)
def heuristic_agent_policy(observation):
    if observation[2] > 23:
        return PigEnv.BANK
    else:
        return PigEnv.ROLL
    
@jit(nopython = True)
def heuristic_opponent_policy(observation):
    if observation[3] > 23:
        return PigEnv.BANK
    else:
        return PigEnv.ROLL

#@jit(nopython = True)
def q_policy(observation):
    return np.argmax(q_table[observation])