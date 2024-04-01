from antlr4 import *
from gramLexer import gramLexer
from gramListener import gramListener
from gramParser import gramParser

class gramPrintListener(gramListener):

    def __init__(self, initMDP, defined_actions = [],defined_states = [], rewards = []):
        self.initMDP = initMDP
        self.defined_actions = defined_actions
        self.defined_states = defined_states
        self.rewards = rewards
        
    def enterDefstates(self, ctx):
        ids = [str(x) for x in ctx.ID()]
        rewards = [int(str(r)) for r in ctx.INT()]
        print("States: %s" % str([str(x) for x in ctx.ID()]))
        print(f"Rewards : {rewards}")
        self.defined_states = [str(x) for x in ctx.ID()]
        self.rewards = [int(str(r)) for r in ctx.INT()]

        # Populate initMDP
        for i in range(len(ids)):
            id = ids[i]
            self.initMDP[id] = dict()
            self.initMDP[id]["transact"] = 2
            self.initMDP[id]["reward"] = rewards[i]

    def enterDefactions(self, ctx):
        print("Actions: %s" % str([str(x) for x in ctx.ID()]))
        self.defined_actions = [str(x) for x in ctx.ID()]

    def enterTransact(self, ctx):
        ids = [str(x) for x in ctx.ID()]
        dep = ids.pop(0)
        assert self.verify_states(dep)
        act = ids.pop(0)
        assert self.verify_actions(act)
        weights = [int(str(x)) for x in ctx.INT()]
        print("Transition from " + dep + " with action "+ act + " and targets " + str(ids) + " with weights " + str(weights))

        #On vérifie qu'on a pas deux fois le même nom d'action
        if act in self.initMDP[dep].keys():
            print("2 actions have the same name for this state : ", dep)
            assert True == False
        
        # Populate initMDP
        self.initMDP[dep][act] = {
            "states_to": ids,
            "weights": weights
        }
        self.initMDP[dep]["transact"] = 1
        
        #On vérifie qu'on ne mélange pas les types de transitions
        if "tna" in self.initMDP[dep].keys():
            print("An other kind of transition is already defined for this state : ",dep)
            assert True == False
        
        
    def enterTransnoact(self, ctx):
        ids = [str(x) for x in ctx.ID()]
        dep = ids.pop(0)
        assert self.verify_states(dep)
        weights = [int(str(x)) for x in ctx.INT()]
        print("Transition from " + dep + " with no action and targets " + str(ids) + " with weights " + str(weights))
        
        #On vérifie qu'on ne mélange pas les types de transitions
        if len(self.initMDP[dep]) >= 3 :
            print("An other transition is already defined for this state : ",dep)
            assert False == True
        
        # Populate initMDP
        self.initMDP[dep]["tna"] = {
            "states_to": ids,
            "weights": weights,
            #"transact": False
        }
        self.initMDP[dep]["transact"] = 0
    
    def verify_states(self,name) :
        if not(name in self.defined_states) :
            print("The state ",name," is not defined, please change your input file")
            return False
        else :
            return True
        
    def verify_actions(self,name):
        if not(name in self.defined_actions) :
            print("The action ",name," is not defined, please change your input file")
            return False
        else :
            return True