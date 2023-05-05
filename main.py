from env.pig import PigEnv
import numpy as np

import time

#This is the opponent's agnet_policy, which is random for now.
def agent_policy(observation):
    return np.random.randint(0,2)


env = PigEnv(max_turns=500)
observation, info = env.reset()

print(observation)

print("action space ", env.action_space)
print("observation space ", env.observation_space)

for i in range(100):
    action = agent_policy(observation)
    observation, reward, terminated, truncated, info = env.step(action)
    #time.sleep(0.3)

    #print("Visible Game State {}:".format(i),observation, reward, terminated, truncated, info)
    print("Game Points {}:".format(i), env.points)


    #if terminated or truncated:
        #observation, info = env.reset()
        


env.close()