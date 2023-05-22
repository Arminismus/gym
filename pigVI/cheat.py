import numpy as np
import pprint
import sys

#fix this later
env = PigEnv()

def value_iteration(env,theta = 0.0001, discount_factor = 1.0):


    def one_step_lookahed(state,V):
        A = np.zeros(env.nA)
        for a in range(env.nA):
            for prob, next_state, reward, done in env.P[state][a]:
                A[a] += prob* (reward + discount_factor*V[next_state])
        return A
    
    V = np.zeros(env.nS)

    while True:


        delta = 0

        for s in range(env.nS):
            #Do one step lookahead
            A = one_step_lookahed(s,V)
            best_action_value = np.max(A)

            delta = max(delta,np.abs(best_action_value  - V[S]))

            V[s] = best_action_value
        
        if delta < theta:
            break

    #value iteration over
    policy = np.zeros([env.nS,env.nA])
    for s in range(env.nS):
        A = one_step_lookahed(s,V)
        best_action =np.argmax(A)

        policy[s,best_action] = 1.0
    
    return policy, V