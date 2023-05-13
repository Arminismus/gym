import sys
args = sys.argv #this will put the entered arguments in a list

class Test:
    def __init__(self,opponent_policy, agent_policy) -> None:
        self.learnable = True
        self.agent_policy = agent_policy
        self.opponent_policy = opponent_policy

print(args)