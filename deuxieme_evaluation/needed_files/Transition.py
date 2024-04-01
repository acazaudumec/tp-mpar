from random import random
import numpy as np

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
    
    def get_next_state_ID(self, current_state_ID = None):
        
        if current_state_ID == None :
            current_state_ID = self.ID_from
        
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