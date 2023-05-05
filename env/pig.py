import numpy as np
from gymnasium import Env


def random_opponent_policy(observations):
    return np.random.randint(0,2)


#implement this later
def optimal_opponent_policy(observations):
    pass

class PigEnv(Env):
    LOSE = 1
    BANK = 1
    ROLL = 0

    def __init__(self, die_sides = 6,max_turns = 20,opponent_policy = random_opponent_policy):
        self.opponent_policy = opponent_policy
        self.max_turns = max_turns
         #implement this
        self.action_space = {'bank':0, 'roll':1}
        self.die_sides = die_sides
        self.observation_space = np.ones(4)


        #set the stage
        self.reset()

    def reset(self):
        self.actions_taken = {1:[],0:[]} #a dictionary that can be accessed
        self.points = {1:0,0:0}
        self.agent_buffer = 0 #current run of points, will be saved in bank
        self.observations = None
        self.remaining_turns = self.max_turns  

        observation = [self.points[0],self.points[1],self.agent_buffer]
        self.reward = 0
        self.terminated = False
        self.truncatued = False
        self.info = None

        return observation, self.info  

    #There is no decision making in the first step, since, it is always best to roll first. 
    #can this be learned by the agent?
    #Ha! This should(!) be learned by the agent, so we should let it freely choose! This also makes it easy to implement!
    def process_game_turn(self):
        self.die = np.random.randint(1, self.die_sides + 1)
        if self.die == PigEnv.LOSE:
            self.agent_buffer = 0
            #print("{} Lost! it's {}'s Turn.".format(self.turn,1-self.turn))
            self.opponent_step() 
        else:
            self.agent_buffer += self.die

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
    
    def first_step(self,action):
        self.process_game_turn()

        observations = [self.points[0],self.points[1],self.agent_buffer]
        reward = 0
        terminated = 0
        truncated = 0
        
        self.remaining_turns -= 1
        return observations, reward, terminated, truncated, self.info 
        
        
                   
    
    def normal_step(self,action):
        self.die = np.random.randint(1, self.die_sides + 1)
        if self.die == PigEnv.LOSE:
            self.agent_buffer = 0
            #print("{} Lost! it's {}'s Turn.".format(self.turn,1-self.turn))
            self.opponent_step()

        else:
            if action == PigEnv.BANK:
                self.points[1] += self.agent_buffer
            if action == PigEnv.ROLL:
                self.process_game_turn()

        observations = [self.points[0],self.points[1],self.agent_buffer]
        reward = 0
        terminated = 0
        truncated = 0
            
        self.remaining_turns -= 1
        return observations, reward, terminated, truncated, self.info  
    

    
    def last_step(self):
       
        observations = [self.points[0],self.points[1],self.agent_buffer]
        reward = self.points[1] > self.points[0]
        terminated = True
        truncated = False

        return observations, reward, terminated, truncated, self.info 

    
    def step(self,action):
        #if the first step
        if self.remaining_turns == self.max_turns:
            return self.first_step(action)
            
        #if the last step
        if self.remaining_turns == 0:
            return self.last_step()
        #Normal case
        self.normal_step()
