import gymnasium as gym
from gymnasium import spaces
import numpy as np

#let's define the game: 
#There are 2 players, and the starting player, rolls dice until his die lands on 1. 
#at each time step, the agent can make 2 decisions: 1. roll again 2. exit and get the sum of the numbers
# he got with his die.
# 
# if he get to a one, his counter is reset and he receives no points,and it's the turn of the other player. 
#  

#We will just implement the agent, the envoironment comes in later

class PigAgent:
    NUM_STATES = 4
    def __init__(
            self,
            learning_rate,
            discount_factor,
            epsilon,
            ):
       
       self.lr = learning_rate
       self.discount_factor = discount_factor

       self.weights = np.zeros(PigAgent.NUM_STATES)


       self.epsilon = epsilon

       self.training_error = []

    def get_value(self,obs):
        return np.dot(obs,self.weights)

    def get_action(self,obsgit ) -> int:
        pass



    #We need to know what the observation space of the 
    #game is: "What's its state"

    #1.my bank_score
    #2.opponent_bank score
    #3. my current buffer score
    #4. Buffer length


    