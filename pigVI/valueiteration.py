
import numpy as np#let us implement value iteration for the game of piglet

class KeepMax:
    def __init__(self):
        self.max = - np.inf
    
    def compare(self,number):
        if self.max < number:
            self.max = number



def return_reward(i,j,k):
    if (i == 2 or k ==2) and j < 2:
        return 1
    else:
        return 0

value_object = KeepMax()

#first, we create a table of all the states:
epsilon = 1e-5
states = np.zeros(shape = (2,2,2))

delta = np.inf
lim = 2
while True:
    if delta < epsilon:
        break
    
    #here, we must use the bellman equation to solve the value iteration problem
    #we start from the inside, and we loop through all states, and keep the maximum of the sum of 
    # bootstrapped values over all states
    for i in range(lim):
        for j in range(lim):
            for k in range(lim):
                print((i,j,k))
                states[i][j][k] = np.max([return_reward(_i,_j,_k)+ states[_i][_j][_k]
                                          for _i in range(i,lim)
                                            for _j in range(j,lim)
                                                for _k in range(k,lim)])
    break
                
print(states)