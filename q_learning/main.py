from env.q_pig import PigEnv
import numpy as np

from collections import defaultdict
from tqdm import tqdm

import matplotlib.pyplot as plt
from tables.savetable import save,load
from configs.config import config
from numba import jit


class Main:
    def __init__(self,test_config):
        self.q_table = test_config['q_table']
        self.opponent_policy = test_config['opponent_policy']
        self.agent_policy = test_config['agent_policy']
        self._save = test_config['save']
        
        self.save_name = test_config['save_name']

        self.max_turns = test_config['max_turns']
        self.iterations = test_config['iterations']
        self.learning_rate = test_config['learning_rate']

        self.random_policy = test_config['random_policy']

        self._rewards = []

    
    def run(self):
        #create environment
        
        env = PigEnv(max_turns=self.max_turns,opponent_policy=self.opponent_policy,learning_rate = self.learning_rate)
        q_table = self.q_table

        #reset the environment
        observation, info = env.reset()
        for _ in tqdm(range(self.iterations)):
            state,_ = env.reset()

            terminated = env.terminated
            truncated = env.truncated

            while not terminated and not truncated:
                
                if np.random.random() > env.epsilon: 
                    action = self.agent_policy(observation)
                else:
                    action = np.random.randint(0,2)
                
                next_observation, reward, terminated, truncated, info = env.step(action)

                old_value = q_table[state,action]
                next_max = np.max([q_table[next_observation, PigEnv.ROLL],q_table[next_observation,PigEnv.BANK]])
                new_value = (1 - env.alpha) * old_value + env.alpha * (reward + env.gamma * next_max)

                q_table[state, action] = new_value
                observation = next_observation
            
            self._rewards.append(reward)

        
        
        if self._save:
            save(self.q_table,self.save_name)
        print(sum(self._rewards)/len(self._rewards))


run = Main(config)
run.run()
