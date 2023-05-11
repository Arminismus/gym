import numpy as np
from gymnasium import Env
#from q_learning. import TileCoder


def random_opponent_policy(observation):
    return np.random.randint(0,2) #chagning this affects the number of times we win, indicating that the 
                                  # step/opponent step imbalance created is responsible, because when we increase the chance of banking
                                  #the relative length of the opponent step to our steps is changed.

                                  #after having changed the implementation, we see the normal 50/50 behavior as expected.

#implement this later
def optimal_opponent_policy(observation):
    pass

class PigEnv(Env):
    LOSE = 1
    
    BANK = 1
    ROLL = 0

    AGENT = 1
    OPPONENT = 0

    NUM_ACTIONS = 2
    NUM_STATES = 101*101*101
    def __init__(
              self,
                die_sides = 6,
                max_turns = 20,
                max_points = 100,
                opponent_policy = random_opponent_policy,

                learning_rate = 0.01,
                epsilon = 0.05,
                discount_factor = 0.9
                         ):

        self.opponent_policy = opponent_policy
        self.max_turns = max_turns
        self.action_space = {'bank':0, 'roll':1}
        self.die_sides = die_sides
        self.max_points = max_points
        
        self.alpha = learning_rate
        self.epsilon = epsilon
        self.gamma = discount_factor
        
       
    def reset(self):
        #self.turn = PigEnv.AGENT
        self.turn = np.random.randint(0,2)
        self.actions_taken = {1:[],0:[]} #a dictionary that can be accessed
        self.points = {PigEnv.AGENT:0,PigEnv.OPPONENT:0}
       

        self.buffers = [0,0] 
        self.remaining_turns = self.max_turns  

        self.observation = (self.points[PigEnv.AGENT],self.points[PigEnv.OPPONENT],self.buffers[PigEnv.AGENT])
       


        self.reward = 0
        self.terminated = False
        self.truncated = False
        self.info = None

        return self.observation, self.info  
    
    def get_player_actions(self,current_player,action):
        if action == PigEnv.BANK:
                self.points[current_player] += self.buffers[current_player]
                self.buffers[current_player] = 0
               
                self.turn = 1 - current_player 
                self.remaining_turns -= 1   

        elif action == PigEnv.ROLL:
                self.die = np.random.randint(1, self.die_sides + 1)
                
                if self.die == PigEnv.LOSE:
                    self.buffers[current_player] = 0
                    
                    self.turn = 1 - current_player
                    self.remaining_turns -= 1

                else:
                    self.buffers[current_player] += self.die
    
    
    def step(self,action):
        if self.turn == PigEnv.AGENT:
           self.get_player_actions(PigEnv.AGENT,action) 
            
        elif self.turn == PigEnv.OPPONENT:
             action = self.opponent_policy(self.observation)
             self.get_player_actions(PigEnv.OPPONENT,action)
        
        self.observation = (self.points[0],self.points[1],self.buffers[PigEnv.AGENT])
        

        #if last step
        if self.remaining_turns == 0:
            self.reward = self.points[PigEnv.AGENT] > self.points[PigEnv.OPPONENT]
            self.terminated = True   

        #if either player reaches 100 points, the game is over
        if self.points[PigEnv.AGENT] > self.max_points or self.points[PigEnv.OPPONENT] > self.max_points:
             self.reward = self.points[PigEnv.AGENT] > self.points[PigEnv.OPPONENT]
             self.terminated = True
                  
        
        return self.observation, self.reward, self.terminated, self.truncated , self.info  
 
    

