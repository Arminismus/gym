from collections import defaultdict
from policies.policies import stochastic_policy,heuristic_agent_policy,heuristic_opponent_policy,q_policy
from tables.savetable import q_table

#q_table = defaultdict(lambda:0)

config = {
    "q_table": q_table,
    "opponent_policy": stochastic_policy,
    "agent_policy": q_policy,
    "save": True,
    "load": False,
    "save_name": "my_table",

    "iterations": 10000,
    "max_turns": 300,

    "epsilon": 0.4,
    "learning_rate":0.03,
    "random_policy": stochastic_policy,  
}