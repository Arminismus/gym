import gynamsium as gym
import numpy as np

#let's define the game: 
#There are 2 players, and the starting player, rolls dice until his die lands on 1. 
#at each time step, the agent can make 2 decisions: 1. roll again 2. exit and get the sum of the numbers
# he got with his die.
# 
# if he get to a one, his counter is reset and he receives no points,and it's the turn of the other player. 
#  