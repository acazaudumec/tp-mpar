from antlr4 import *
from gramLexer import gramLexer
from gramListener import gramListener
from gramParser import gramParser
import sys
import numpy as np

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

        return cls(states, encoding)
            

    def run(self):
        pass

class State:
    def __init__(self, ID: int, transitions: list, transact: bool):
        self.ID = ID
        self.transitions = transitions
        self.transact = transact

    @classmethod
    def from_initState(cls, state: str, n_states: int, initState: dict, encoding: dict):
        state_ID = encoding[state]
        transitions = []
        list_actions = list(initState.keys())
        n_actions = len(list_actions)

        # For each action in this state
        for l in range(n_actions):
            action = list_actions[l]
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

    mdp = MDP.from_initMDP(initMDP)
    print(mdp.T)
    for state in mdp.S:
        for transition in state.transitions:
            print(transition.matrix)

if __name__ == '__main__':
    main()
