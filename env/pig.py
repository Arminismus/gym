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
        self.remaining_turns = self.max_turns  

        self.observation = [self.points[0],self.points[1],self.agent_buffer]
        
        self.reward = 0
        self.terminated = False
        self.truncated = False
        self.info = None

        return self.observation, self.info  

    #There is no decision making in the first step, since, it is always best to roll first. 
    #can this be learned by the agent?
    #Ha! This should(!) be learned by the agent, so we should let it freely choose! This also makes it easy to implement!
    
    def opponent_step(self):
        '''The opponent has a 50/50 policy by default'''
        done = False
        buffer = 0
        while not done:
            #this is the decision 
            #for the next roll, 
            #there will at least be one roll for the opponent
            
            #make the decision
            done = bool(self.opponent_policy(self.observation))
            
            
            self.die = np.random.randint(1, self.die_sides + 1)
            #print('He rolled!:',self.die)
            
            if self.die == PigEnv.LOSE:
                buffer = 0
                done = True
            else:
                buffer += self.die 
       
        #print('he decided to bank!',buffer)
        self.points[0] += buffer                
    
    def step(self,action):
        
       
        if action == PigEnv.BANK:
            self.points[1] += self.agent_buffer
            self.agent_buffer = 0
            #print('I banked!',self.agent_buffer)
            self.opponent_step() #I had forgotten to give the opponent their turn when I banked!
        
        elif action == PigEnv.ROLL:
            self.die = np.random.randint(1, self.die_sides + 1)
            #print('I rolled!:',self.die)
            
            
            if self.die == PigEnv.LOSE:
                self.agent_buffer = 0
                #print('I lost my streak!')
                
                self.opponent_step()

            else:
                self.agent_buffer += self.die

        
        observations = [self.points[0],self.points[1],self.agent_buffer]
        
        #if last step
        if self.remaining_turns == 0:
            self.reward = self.points[1] > self.points[0]
            self.terminated = True
        
        else:
            self.remaining_turns -= 1
            
        
        return observations, self.reward, self.terminated, self.truncated , self.info  
 
    

