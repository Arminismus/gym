from collections import defaultdict
from policies.policies import stochastic_policy,heuristic_agent_policy,heuristic_opponent_policy


config = {
    "q_table": defaultdict(lambda:0),
    "opponent_policy": stochastic_policy,
    "agent_policy": heuristic_agent_policy,
    "save": True,
    "load": False,
    "save_name": "my_table",

    "iterations": 10000,
    "max_turns": 300,

    "epsilon": 0.1,
    "learning_rate":0.03,
    "random_policy": stochastic_policy,  
}