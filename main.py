from env.pig import PigEnv
import numpy as np

import time

#This is the opponent's agnet_policy, which is random for now.
def agent_policy(observation):
    return np.random.randint(0,2)


env = PigEnv(max_turns=20)
observation, info = env.reset()



print(observation)

print("action space ", env.action_space)
print("observation space ", env.observation_space)


for _ in range(3):
    action = agent_policy(observation)
    observation, reward, terminated, truncated, info = env.step(action)
    
    while not terminated and not truncated:
        action = agent_policy(observation)
        observation, reward, terminated, truncated, info = env.step(action)
        time.sleep(0.2)

        print("Visible Game State {}:",observation, reward, terminated, truncated, info)
        print("Game Points {}:", env.points)
    
    print("A reset occured!")
    env.reset()
        


env.close()