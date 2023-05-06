from env.pig import PigEnv
import numpy as np

import time

#This is the opponent's agnet_policy, which is random for now.
def agent_policy(observation):
    return np.random.randint(0,2)


env = PigEnv(max_turns=30)
observation, info = env.reset()



print(observation)

print("action space ", env.action_space)
print("observation space ", env.observation_space)

rewards = []

for i in range(100):
    
    
    terminated = False
    truncated = False
    while not terminated and not truncated:
        action = agent_policy(observation)
        observation, reward, terminated, truncated, info = env.step(action)
        time.sleep(1)

        print("Visible Game State:",observation, reward, terminated, truncated, info)
        print("Game Points:", env.points)
    rewards.append(reward)
    env.reset()
    print("A reset occured!")
    
        
print(len(rewards),sum(rewards))

env.close()