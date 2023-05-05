import gymnasium as gym
from env.pig import PigEnv

#This is the opponent's policy, which random for now.
def policy(observation):
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
    action = policy(observation)
    observation, reward, terminated, truncated, info = env.step(action)

    print(observation, reward, terminated, truncated, info)


    if terminated or truncated:
        observation, info = env.reset()


env.close()