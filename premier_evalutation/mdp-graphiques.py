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

    def run(self,current_state = None):
        correct_answer = False
        names_states_list = [elt.name for elt in self.S]
        
        if current_state == None :
            while not(correct_answer) :
                print("\nThe available states are :")
                print(names_states_list)
                first_state = input("Enter the name of the state you want to start with :\n")
                correct_answer = first_state in names_states_list
        
            for elt in self.S :
                if elt.name == first_state :
                    current_state = elt
                    
            print("\nYou have chosen ", current_state.name)
            
        else :
            print("\nThe current state is :", current_state.name)
        
        if current_state.transact == 2 :
            print("You have reached a terminal state : ", current_state.name)
            return ""

        elif current_state.transact == False :
            print("There is no action possible")
            #On récupère la transition actuelle :
            current_transition = current_state.transitions[0]
        
        else :
            #Dans le cas où il n'y a qu'une seul action possible - idem que pas d'actions mais avec 2 lignes de texte en plus aux lignes 91 et 92
            if len(current_state.transitions) == 1 :
                current_transition = current_state.transitions[0]
                print("There is only one action possible and it's : ", current_transition.name)
                print("You have chosen the action named : ",current_transition.name)
                #On récupère la transition actuelle :
                current_transition = current_state.transitions[0]
                
            #Dans le cas où il ya plusieurs actions possibles
            else :
                print("There are ",len(current_state.transitions)," possible actions")
                possible_transitions = [transi.name for transi in current_state.transitions]
                print("These actions are : ", possible_transitions)
                
                bien_choisi = False
                while not(bien_choisi) :
                    action = input("Choose one action among the possible ones :\n")
                    bien_choisi = action in possible_transitions
                
                i = 0
                current_transition = current_state.transitions[i]
                while action != current_transition.name :
                    i += 1
                    current_transition = current_state.transitions[i]
                
                print("You have chosen the action named : ",current_transition.name)
                #On récupère la transition actuelle :
                current_transition = current_state.transitions[0]
    
        #On affiche les possibilités à l'utilisateur :
        possible_next_states_ID = current_transition.ID_to
        possible_next_states_name = []
        for ID in possible_next_states_ID :
            for elt in self.S :
                if elt.ID == ID :
                    possible_next_states_name.append(elt.name)
        print("The next possible states are : ", possible_next_states_name)
        #On affiche les porbabilités à l'utlisateur :
        list_prob = current_transition.matrix[current_transition.ID_from]
        list_prob = [list_prob[i] for i in possible_next_states_ID]
        print("With a probability respectively of : ",list_prob)
        #On regarde quel sera le prochain état :
        next_state_ID = current_transition.get_next_state_ID(current_state.ID)
        for elt in self.S :
            if next_state_ID == elt.ID :
                next_state = elt
        print("The next state is : ",next_state.name)

        flag = False
        while not(flag) :
            answer = input("Do you want to continue ? (y for yes, n for no) :\n")
            if answer == "y" :
                flag = True
                self.run(next_state)
            elif answer == "n" :
                flag = True
        

class State:

    def __init__(self, ID: int, name : str, transitions: list, transact: int):
        self.ID = ID
        self.name = name
        self.transitions = transitions
        self.transact = transact
    
    def __repr__(self) -> str:
        print("ID : ",self.ID)
        print("name : ", self.name)
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
            if action == "transact":
                pass
            else:
                transitions.append(Transition.from_initTransition(
                    encoding[state + "_" + action],
                    action,
                    state_ID,
                    n_states,
                    initState[action],
                    encoding
                ))

        return cls(state_ID, state, transitions, initState["transact"])

class Transition:
    def __init__(self, ID: int, name : str, ID_from: int, ID_to: list, matrix):
        self.ID = ID
        self.name = name
        self.ID_from = ID_from
        self.ID_to = ID_to
        self.matrix = matrix
    
    def __repr__(self) -> str:
        print("ID : " + str(self.ID))
        print("name : ", self.name)
        print("ID_from : " + str(self.ID_from))
        print("ID_to : " + str(self.ID_to))
        print("matrix :")
        print(self.matrix)
        return ""

    @classmethod
    def from_initTransition(cls, ID: int, name :str, ID_from: int, n_states: int, initTransition: dict, encoding: dict):
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
        
        return cls(ID, name, ID_from, ID_to, new_action)
    
    def get_next_state_ID(self, current_state_ID):
        list_prob = self.matrix[current_state_ID]
        rand = random()
        i = 0
        while i<len(list_prob) and list_prob[i] == 0:
            i += 1
        next_state_ID = i
        s = list_prob[i]
        for i in range(next_state_ID+1,len(list_prob)) :
            if list_prob[i] != 0:
                s += list_prob[i]
                if rand < s and rand >= s-list_prob[i]:
                    next_state_ID = i
        return next_state_ID

    
class gramPrintListener(gramListener):

    def __init__(self, initMDP, defined_actions = [],defined_states = []):
        self.initMDP = initMDP
        self.defined_actions = defined_actions
        self.defined_states = defined_states
        
    def enterDefstates(self, ctx):
        ids = [str(x) for x in ctx.ID()]
        print("States: %s" % str([str(x) for x in ctx.ID()]))
        self.defined_states = [str(x) for x in ctx.ID()]

        # Populate initMDP
        for id in ids:
            self.initMDP[id] = dict()
            self.initMDP[id]["transact"] = 2

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
        if len(self.initMDP[dep]) >= 2 :
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



def main():
    initMDP = dict()

    # lexer = gramLexer(StdinStream())
    lexer = gramLexer(FileStream("ex2.mdp"))
    stream = CommonTokenStream(lexer)
    parser = gramParser(stream)
    tree = parser.program()
    printer = gramPrintListener(initMDP)
    
    walker = ParseTreeWalker()
    walker.walk(printer, tree)
    
    print(initMDP)
    
    mdp = MDP.from_initMDP(initMDP)
    mdp.run()
    """
    for state in mdp.S:
        for transition in state.transitions:
            print(transition.matrix)
    """
   

if __name__ == '__main__':
    main()