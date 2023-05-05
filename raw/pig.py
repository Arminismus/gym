import numpy as np
import time
from gymnasium import Env

class PigEnv(Env):
    CHANGE = 1
    STICK = 0

    LOSE = 1
    AGENT_INDEX = 1

    def __init__(self, die_sides = 6,game_steps = 20):
        self.actions = {1:[],0:[]} #a dictionary that can be accessed
        self.points = {1:0,0:0}
        self.game_steps = game_steps
    
        self.turn = None
        self.die_sides = die_sides
    
    def change_turn(self):
        self.turn = 1 - self.turn
    
    def agent_start(self):
        #for the sake of simplicity, it is always the agent's turn
        self.turn = PigEnv.AGENT_INDEX
    
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

        self.actions[self.turn].append(action)
    
    
    def epsiode_play(self):
        self.start()
        for _ in range(self.game_steps):
            self.step()
        #print("actions:",self.actions)
        #print('points:',self.points)
        
        #our agent is agent 1
        if self.points[0] > self. points[1]:
            return 1
        else:
            return 0
            
game = PigEnv(game_steps=30)
game.play()