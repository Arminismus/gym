import numpy as np
import time
from gymnasium import Env

class PigEnv(Env):
    CHANGE = 1
    STICK = 0
    LOSE = 1
    AGENT_INDEX = 1

    def __init__(self, die_sides = 6,max_turns = 20):
        self.actions_taken = {1:[],0:[]} #a dictionary that can be accessed
        self.points = {1:0,0:0}
        self.agent_buffer = 0

        self.max_turns = max_turns

        self.action_space = ['bank':0, 'roll':1]
        #the state is 
        self.observation_space = np.ones(4)
        #self.points, for the agent and the opponent
        #self.
    
        self.turn = None
        self.die_sides = die_sides
        self.remaining_turns = max_turns
    
    def _get_obs(self):
        pass

    def opponent_step(self):
        '''The opponent has a 50/50 policy'''
        
        #roll die
        die = np.random.randint(1, self.die_sides + 1)
        if die == PigEnv.LOSE:
            #self.points[0] += 0
            done = True
        else:
            buffer += die 
        


        done = False
        buffer = 0


        while not done:
            #roll die
            die = np.random.randint(1, self.die_sides + 1)
            if die == PigEnv.LOSE:
                #self.points[0] += 0
                done = True
            else:
                buffer += die 
        
        self.points[0] += buffer 

    #start of an episode
    def reset(self):
        #for the sake of simplicity, it is always the agent's turn
        #at the begining of the game
        self.turn = PigEnv.AGENT_INDEX
        die = np.random.randint(1, self.die_sides + 1) 
        #all players will want to roll their first time!
        #this is because even if they lose, they haven't 
        #lost any potential points, where as they expose themselves
        #to the possibility of gaining some points!
    
   
    def step(self,action):
        #roll die
        if self.remaining_turns == 0:
            return obs 
        die = np.random.randint(1, self.die_sides + 1)

        #check if lost:
        if die == PigEnv.LOSE:
            self.points[self.turn] = 0
            #print("{} Lost! it's {}'s Turn.".format(self.turn,1-self.turn))
            self.opponent_step()


            return obs, reward, terminated, truncated, info
   
   
   
   
    def time_step(self):
        #roll die
        die = np.random.randint(1, self.die_sides + 1)
        #print('{} got {} points! '.format(self.turn,die))
        
        #if lost, change turn, and reset points to zero.
        if die == PigEnv.LOSE:
            self.points[self.turn] = 0
            #print("{} Lost! it's {}'s Turn.".format(self.turn,1-self.turn))
            self.change_turn()
        else:
            self.points[self.turn] += die

        
        #make decision
        if np.random.random() > 0.5:
            return PigEnv.CHANGE
        else:
            return PigEnv.STICK    
    
    def step(self):
        action = self.player_action()
        if action == PigEnv.CHANGE:
            self.change_turn()

        self.actions_taken[self.turn].append(action)
    
    
    def epsiode_play(self):
        self.start()
        for _ in range(self.game_steps):
            self.step()
        #print("actions:",self.actions_taken)
        #print('points:',self.points)
        
        #our agent is agent 1
        if self.points[0] > self. points[1]:
            return 1
        else:
            return 0
            
game = PigEnv(game_steps=30)
game.play()