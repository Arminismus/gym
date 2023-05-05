from gym import Env
import numpy as np


class PigEnv(Env):
    """
    ## Description

    This environment is a simple two player game where the goal is to bank as many points as possible.
    Each turn, the player rolls a die. If the player rolls a 1, they lose all points for that turn and the turn ends.
    Otherwise, the player can choose to roll again or bank their points. If the player banks their points, the turn ends.
    If the player rolls again, the points from that roll are added to the turn total and the player can choose to roll again or bank their points.
    When the player busts of banks the opponent takes their turn. The opponent's turns is skipped and the player's next obervation is the state after the opponent's turn.


    ## Observation

    the observation is a numpy array with shape (4, ) where each entry is an integer as follows:
    0. the player's turn total
    1. the player's banked points
    2. the opponent's banked points
    3. the number of turns that have passed


    ## Actions

    The action is an integer with value 0 or 1 where 0 means roll again and 1 means bank points.


    ## Reward

    The reward is 0 if the game is not over and 1 if the player wins and -1 if the player loses.


    ## Starting State

    The starting state is the player's turn total is 0, the player's banked points is 0, and the opponent's banked points is 0.


    ## Episode Termination

    The episode terminates after _max_turns_ at which point the winnter is determined by the player with the most points.
    """
    def __init__(self, max_turns=10, max_points=1000):
        self.max_turns = max_turns
        self.max_points = max_points

        self.action_space = [0, 1]
        self.observation_space = [(0, self.max_points), (0, self.max_points), (0, self.max_points), (0, self.max_turns)]

        self.reset()

    

    def step(self, action):

        reward = 0
        terminated = False
        truncated = False
        info = {}


        if action == 0:
            # roll again
            die = np.random.randint(1, 7)
            if die == 1:
                # bust
                self.observation[0] = 0
                
                # opponent's turn
                self.observation[2] += self._play_opponent()
                self.observation[3] += 1

            else:
                # add to turn total
                self.observation[0] += die

        elif action == 1:
            # bank points
            self.observation[1] += self.observation[0]
            self.observation[0] = 0

            # opponent's turn
            self.observation[2] += self._play_opponent()
            self.observation[3] += 1

        else:
            raise ValueError("Invalid action")
        
        # check if game is over
        if self.observation[3] >= self.max_turns:
            # game is over
            if self.observation[1] > self.observation[2]:
                # player wins
                reward = 1
            elif self.observation[1] < self.observation[2]:
                # player loses
                reward = -1
            else:
                # tie
                reward = 0

            terminated = True



        observation = self.observation[:]

        return observation, reward, terminated, truncated, info


    def reset(self):
        self.observation = np.array([0, 0, 0, 0])
        return self.observation[:], {}



    def render(self, mode="human"):
        raise NotImplementedError


    def close(self):
        pass


    def _play_opponent(self):
        # opponent always banks
        return 0