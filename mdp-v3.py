from antlr4 import *
from gramLexer import gramLexer
from gramListener import gramListener
from gramParser import gramParser
import sys
import numpy as np
from random import random
import sys

class MDP:

    def __init__(self, states: list, encoding):
        self.S = states
        self.T = encoding

    @classmethod
    def from_initMDP(cls, initMDP: dict):

        # Create and populate the routing table
        encoding = dict()
        c_state = 0
        for state in initMDP.keys():
            encoding[state] = c_state
            c_state += 1
            c_action = 0
            for action in initMDP[state].keys():
                encoding[state + "_" + action] = c_action
                c_action += 1
        
        # Create and populate the State objects
        states = []
        list_states = list(initMDP.keys())
        n_states = len(list_states)

        # For each state in initMDP
        for k in range(n_states):
            state = list_states[k]
            states.append(State.from_initState(state, n_states, initMDP[state], encoding))
            #print("")
            #print(states[-1])

        return cls(states, encoding)

    def run(self):
        correct_answer = False
        names_states_list = [str(elt.ID) for elt in self.S]
        while not(correct_answer) :
            print("The available states are :")
            print(names_states_list)
            first_state = input("Enter the name of the state you want to start with")
            correct_answer = first_state in names_states_list
            print("\n",correct_answer)
        
        for elt in self.S :
            if str(elt.ID) == first_state :
                current_state = elt
        
        print(current_state.transitions)
        

class State:

    def __init__(self, ID: int, transitions: list, transact: bool):
        self.ID = ID
        self.transitions = transitions
        self.transact = transact
    
    def __repr__(self) -> str:
        print("ID : ",self.ID)
        print("transitions : ",self.transitions)
        print("transact : ",self.transact)
        return ""

    @classmethod
    def from_initState(cls, state: str, n_states: int, initState: dict, encoding: dict):
        
        state_ID = encoding[state]
        
        #print("from_initState : ",state,state_ID)
        
        transitions = []
        list_actions = list(initState.keys())
        n_actions = len(list_actions)

        # For each action in this state
        for l in range(n_actions):
            action = list_actions[l]
            #print("action : ",action)
            if action == "transact":
                pass
            else:
                transitions.append(Transition.from_initTransition(
                    encoding[state + "_" + action],
                    state_ID,
                    n_states,
                    initState[action],
                    encoding
                ))

        return cls(state_ID, transitions, initState["transact"])

class Transition:
    def __init__(self, ID: int, ID_from: int, ID_to: list, matrix):
        self.ID = ID
        self.ID_from = ID_from
        self.ID_to = ID_to
        self.matrix = matrix
    
    def __repr__(self) -> str:
        print("ID : " + str(self.ID))
        print("ID_from : " + str(self.ID_from))
        print("ID_to : " + str(self.ID_to))
        print("matrix :")
        print(self.matrix)
        return ""

    @classmethod
    def from_initTransition(cls, ID: int, ID_from: int, n_states: int, initTransition: dict, encoding: dict):
        states_to = initTransition["states_to"]
        weights = initTransition["weights"]
        sum_weights = sum(weights)
        new_action = np.zeros((n_states, n_states))
        ID_to = []

        for state in states_to:
            ID_to.append(encoding[state])

        for j in range(len(states_to)):
            column = encoding[states_to[j]]
            probability = weights[j]/sum_weights
            new_action[ID_from][column] = probability
        
        return cls(ID, ID_from, ID_to, new_action)
    
    def get_next_state_ID(self, current_state_ID):
        list_prob = self.matrix[current_state_ID]
        s = 0
        rand = random()
        for i in range(len(list_prob)):
            if list_prob[i] != 0:
                s += list_prob[i]
                if rand < s:
                    next_state_ID = i
        return next_state_ID

    
class gramPrintListener(gramListener):

    def __init__(self, initMDP):
        self.initMDP = initMDP
        
    def enterDefstates(self, ctx):
        ids = [str(x) for x in ctx.ID()]
        print("States: %s" % str([str(x) for x in ctx.ID()]))

        # Populate initMDP
        for id in ids:
            self.initMDP[id] = dict()

    def enterDefactions(self, ctx):
        print("Actions: %s" % str([str(x) for x in ctx.ID()]))

    def enterTransact(self, ctx):
        ids = [str(x) for x in ctx.ID()]
        dep = ids.pop(0)
        act = ids.pop(0)
        weights = [int(str(x)) for x in ctx.INT()]
        print("Transition from " + dep + " with action "+ act + " and targets " + str(ids) + " with weights " + str(weights))

        # Populate initMDP
        self.initMDP[dep][act] = {
            "states_to": ids,
            "weights": weights
        }
        self.initMDP[dep]["transact"] = True
        
    def enterTransnoact(self, ctx):
        ids = [str(x) for x in ctx.ID()]
        dep = ids.pop(0)
        weights = [int(str(x)) for x in ctx.INT()]
        print("Transition from " + dep + " with no action and targets " + str(ids) + " with weights " + str(weights))
        
        # Populate initMDP
        self.initMDP[dep]["tna"] = {
            "states_to": ids,
            "weights": weights,
            "transact": False
        }
        self.initMDP[dep]["transact"] = False



def main():
    initMDP = dict()

    # lexer = gramLexer(StdinStream())
    lexer = gramLexer(FileStream("ex.mdp"))
    stream = CommonTokenStream(lexer)
    parser = gramParser(stream)
    tree = parser.program()
    printer = gramPrintListener(initMDP)
    walker = ParseTreeWalker()
    walker.walk(printer, tree)

    print("\n initMDP:",initMDP,"\n")
    mdp = MDP.from_initMDP(initMDP)
    
    #print("mdp.T : ", mdp.T)
    """
    for state in mdp.S:
        for transition in state.transitions:
            print(transition.matrix)
    """
    mdp.run()

if __name__ == '__main__':
    main()