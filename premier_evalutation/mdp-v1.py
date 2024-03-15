from antlr4 import *
from gramLexer import gramLexer
from gramListener import gramListener
from gramParser import gramParser
import sys

class MDP:
    def __init__(self, states: dict):
        self.states = states
        self.nStates = len(states.keys())

    @classmethod
    def from_initMDP(cls, initMDP: dict):
        states = dict()
        for key in initMDP:
            state = State.from_initState(key, initMDP[key])
            states[key] = state
        return cls(states)
    

class Transition:

    def __init__(self, ID, state_from: str, state_to: list(str), weights: list)-> None:
        self.ID = ID
        self.state_from = state_from
        self.state_to = state_to
        self.weights = weights

    @classmethod
    def from_initTransition(cls, state_from: str, transitionID: str, initTransition: dict):
        return cls(transitionID, state_from, initTransition["state_to"], initTransition["weights"])
    

class State:

    def __init__(self, ID: str, transitions: dict)-> None:
        self.ID = ID
        self.transitions = transitions

    @classmethod
    def from_initState(cls, stateID: str, initState: dict):
        transitions = dict()
        for key in initState.keys():
            transition = Transition.from_initTransition(stateID, key, initState[key])
            transitions[key] = transition
        return cls(stateID, transitions)
    
        
class gramPrintListener(gramListener):

    def __init__(self, initMDP: dict):
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
            "state_to": ids,
            "weights": weights
        }
        
    def enterTransnoact(self, ctx):
        ids = [str(x) for x in ctx.ID()]
        dep = ids.pop(0)
        weights = [int(str(x)) for x in ctx.INT()]
        print("Transition from " + dep + " with no action and targets " + str(ids) + " with weights " + str(weights))

        # Populate initMDP
        self.initMDP[dep]["tna"] = {
            "state_to": ids,
            "weights": weights
        }



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

if __name__ == '__main__':
    main()
