from env.pig import PigEnv

import time

#This is the opponent's agnet_policy, which is random for now.
def agent_policy(observation):
    if observation[0] < 20:
        return 0
    else:
        return 1


env = PigEnv(max_turns=3)
observation, info = env.reset()

print(observation)

print("action space ", env.action_space)
print("observation space ", env.observation_space)

for _ in range(100):
    action = agent_policy(observation)
    observation, reward, terminated, truncated, info = env.step(action)
    time.sleep(0.3)

    print(observation, reward, terminated, truncated, info)


    if terminated or truncated:
        observation, info = env.reset()


env.close()