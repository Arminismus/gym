import numpy as np
import time
from gymnasium import Env


def random_opponent_policy(observations):
    return np.random.randint(0,2)


#implement this later
def optimal_opponent_policy(observations):
    pass

class PigEnv(Env):
    CHANGE = 1
    STICK = 0
    LOSE = 1
    AGENT_INDEX = 1

    def __init__(self, die_sides = 6,max_turns = 20,opponent_policy = random_opponent_policy):
        self.actions_taken = {1:[],0:[]} #a dictionary that can be accessed
        self.points = {1:0,0:0}
        self.agent_buffer = 0 #current run of points, will be saved in bank

        self.observations = None #implement this
        self.opponent_policy = opponent_policy
        self.max_turns = max_turns

        self.action_space = ['bank':0, 'roll':1]
        #the state is 
        self.observation_space = np.ones(4)
        #self.points, for the agent and the opponent
        #self.agent_buffer
    
        self.turn = None
        self.die_sides = die_sides
        self.remaining_turns = max_turns
        
        #the die is rolled automatically on the first try of the 
        #first turn for each player, here only for the agent
        self.die = np.random.randint(1, self.die_sides + 1) 
        self.agent_buffer += self.die
            
    def _get_obs(self):
        pass

    def opponent_step(self):
        '''The opponent has a 50/50 policy by default'''
        
        done = False
        buffer = 0

        while not done:
            #this is the decision 
            #for the next roll, 
            #there will at least be one roll
            
            #make the decision
            done = bool(self.opponent_policy(self.observations)) 
            self.die = np.random.randint(1, self.die_sides + 1)
            
            if self.die == PigEnv.LOSE:
                #self.points[0] += 0
                done = True
            else:
                buffer += self.die 
        
        self.points[0] += buffer 
   
    def step(self,action):
        
        info = None

        #if the first step
        if self.remaining_turns == self.max_turns:
            self.die = np.random.randint(1, self.die_sides + 1)
            if self.die == PigEnv.LOSE:
                #self.agent_buffer = 0
                self.opponent_step()

            observations = [self.points[0],self.points[1],self.agent_buffer]
            reward = 0
            terminated = 0
            truncated = 0
            
            self.remaining_turns -= 1
            return observations, reward, terminated, truncated, info 
            
        
        #if in the midst of play
        if self.remaining_turns == 0:
                
            observations = [self.points[0],self.points[1],self.agent_buffer]
            reward = self.points[1] > self.points[0]
            terminated = 0
            truncated = 0

            return observations, reward, terminated, truncated, info

        #Normal case
        self.die = np.random.randint(1, self.die_sides + 1)
        if self.die == PigEnv.LOSE:
            self.agent_buffer = 0
            #print("{} Lost! it's {}'s Turn.".format(self.turn,1-self.turn))
            self.opponent_step()
                        
        observations = [self.points[0],self.points[1],self.agent_buffer]
        reward = 0
        terminated = 0
        truncated = 0
            
        self.remaining_turns -= 1
        return observations, reward, terminated, truncated, info
   
    def reset(self):
        #for the sake of simplicity, it is always the agent's turn
        #at the begining of the game
        #self.turn = PigEnv.AGENT_INDEX
   
   
    
            
game = PigEnv(game_steps=30)
game.play()