import numpy as np
import time
class Pig:
    CHANGE = 1
    STICK = 0

    LOSE = 1



    def __init__(self, die_sides = 6,game_steps = 20):
        self.actions = {1:[],0:[]} #a dictionary that can be accessed
        self.points = {1:0,0:0}
        self.game_steps = game_steps
    
        self.turn = None
        self.die_sides = die_sides

    def determine_turn(self):
        #we return the keys to easily use them elsewhere
        players = list(self.actions.keys())
        self.turn = np.random.choice(players)
    
    def change_turn(self):
        self.turn = 1 - self.turn
    
    def player_action(self):
        #roll die
        die = np.random.randint(1, self.die_sides + 1)
        #print('{} got {} points! '.format(self.turn,die))
        
        #if lost, change turn, and reset points to zero.
        if die == Pig.LOSE:
            self.points[self.turn] = 0
            #print("{} Lost! it's {}'s Turn.".format(self.turn,1-self.turn))
            self.change_turn()
        else:
            self.points[self.turn] += die

        
        #make decision
        if np.random.random() > 0.5:
            return Pig.CHANGE
        else:
            return Pig.STICK    
    
    def play(self):

        #determine how long the game is
        #determine whose turn it is

        #for the person whose turn it is, takes his action.
        # if he is continuing, it is still their turn, 
        # if he changes, we change the turn.
        #
        self.determine_turn()
        
        for _ in range(self.game_steps):
            action = self.player_action()
            if action == Pig.CHANGE:
                self.change_turn()

            self.actions[self.turn].append(action)

            time.sleep(1)

        #print("actions:",self.actions)
        #print('points:',self.points)
        return self.actions,self.points
            
game = Pig(game_steps=30)
game.play()