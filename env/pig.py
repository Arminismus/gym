import numpy as np
from gymnasium import Env


def random_opponent_policy(observations):
    return np.random.randint(0,2) #chagning this affects the number of times we win, indicating that the 
                                  # step/opponent step imbalance created is responsible, because when we increase the chance of banking
                                  #the relative length of the opponent step to our steps is changed.

                                  #after having changed the implementation, we see the normal 50/50 behavior as expected.

#implement this later
def optimal_opponent_policy(observations):
    pass

class PigEnv(Env):
    LOSE = 1
    BANK = 1
    ROLL = 0

    AGENT = 1
    OPPONENT = 0

    def __init__(self, die_sides = 6,max_turns = 20,opponent_policy = random_opponent_policy):
        self.opponent_policy = opponent_policy
        self.max_turns = max_turns
         #implement this
        self.action_space = {'bank':0, 'roll':1}
        self.die_sides = die_sides
        self.observation_space = np.ones(4)
        
        

        #set the stage
        #self.reset()

    def reset(self):
        self.turn = PigEnv.AGENT
        self.actions_taken = {1:[],0:[]} #a dictionary that can be accessed
        self.points = {PigEnv.AGENT:0,PigEnv.OPPONENT:0}
        #self.agent_buffer = 0
        #self.opponent_buffer = 0 #current run of points, will be saved in bank

        self.buffers = [0,0] #
        self.remaining_turns = self.max_turns  

        self.observation = [self.points[0],self.points[1],self.buffers[PigEnv.AGENT]]
        
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
        while True:
            #this is the decision 
            #for the next roll, 
            #there will at least be one roll for the opponent with 
            #while not done
            #This makes him win much more often than the agent!

            #fixing this brought a lot more balance!
            
            #make the decision
            done = bool(self.opponent_policy(self.observation))
            
            if done:
                break
            
            
            self.die = np.random.randint(1, self.die_sides + 1)
            #print('He rolled!:',self.die)
            
            if self.die == PigEnv.LOSE:
                buffer = 0
                done = True
            else:
                buffer += self.die 
       
        #print('he decided to bank!',buffer)
        self.remaining_turns -= 1
        self.points[PigEnv.OPPONENT] += buffer                
    
    
    def actions(self,current_player,action):
        if action == PigEnv.BANK:
                self.points[current_player] += self.buffers[current_player]
                self.buffers[current_player] = 0
                #print('I banked!',self.agent_buffer)
                #self.opponent_step() #I had forgotten to give the opponent their turn when I banked!
                self.turn = 1 - current_player #change turns, 1,0
                self.remaining_turns -= 1   

        elif action == PigEnv.ROLL:
                self.die = np.random.randint(1, self.die_sides + 1)
                #print('I rolled!:',self.die)


                if self.die == PigEnv.LOSE:
                    self.buffers[current_player] = 0
                    #print('I lost my streak!')
                    #self.opponent_step()
                    self.turn = 1 - current_player
                    self.remaining_turns -= 1

                else:
                    self.buffers[current_player] += self.die

    
    
    
    def step(self,action):
        if self.turn == PigEnv.AGENT:
       
            if action == PigEnv.BANK:
                self.points[PigEnv.AGENT] += self.buffers[PigEnv.AGENT]
                self.buffers[Pig] = 0
                #print('I banked!',self.agent_buffer)
                #self.opponent_step() #I had forgotten to give the opponent their turn when I banked!
                self.turn = PigEnv.OPPONENT
                self.remaining_turns -= 1   

            elif action == PigEnv.ROLL:
                self.die = np.random.randint(1, self.die_sides + 1)
                #print('I rolled!:',self.die)


                if self.die == PigEnv.LOSE:
                    self.agent_buffer = 0
                    #print('I lost my streak!')
                    #self.opponent_step()
                    self.turn = PigEnv.OPPONENT
                    self.remaining_turns -= 1

                else:
                    self.agent_buffer += self.die
        
        elif self.turn == PigEnv.OPPONENT:
             action = self.opponent_policy(self.observation)
             if action == PigEnv.BANK:
                self.points[PigEnv.OPPONENT] += self.opponent_buffer
                self.opponent_buffer = 0
                #print('I banked!',self.agent_buffer)
                #self.opponent_step() #I had forgotten to give the opponent their turn when I banked!
                self.turn = PigEnv.AGENT
                self.remaining_turns -= 1   

             elif action == PigEnv.ROLL:
                self.die = np.random.randint(1, self.die_sides + 1)
                #print('I rolled!:',self.die)


                if self.die == PigEnv.LOSE:
                    self.opponent_buffer = 0
                    #print('I lost my streak!')
                    #self.opponent_step()
                    self.turn = PigEnv.AGENT
                    self.remaining_turns -= 1

                else:
                    self.opponent_buffer += self.die



        
        observations = [self.points[0],self.points[1],self.agent_buffer]
        
        #if last step
        if self.remaining_turns == 0:
            self.reward = self.points[PigEnv.AGENT] > self.points[PigEnv.OPPONENT]
            self.terminated = True        
        
        return observations, self.reward, self.terminated, self.truncated , self.info  
 
    

