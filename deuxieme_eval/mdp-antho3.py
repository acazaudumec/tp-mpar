from antlr4 import *
from gramLexer import gramLexer
from gramListener import gramListener
from gramParser import gramParser
import sys
import numpy as np
from random import random, randint
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

    def run(self,nb_states_random = None, current_state = None, chemin = [], reward = 0):
        
        if nb_states_random == None or (type(nb_states_random) == type(1) and nb_states_random > 0) :
        
            if current_state == None :
                current_state = self.S[0]
                current_reward = reward + current_state.reward
                if nb_states_random == None :
                    print(f"The current state is : {current_state.name}, reward : {current_reward}")
                
            else :
                current_reward = reward + current_state.reward
                if nb_states_random == None :
                    print(f"\nThe current state is : {current_state.name}, reward : {current_reward}")
            
            #On vérifie si on a atteint un état terminal
            all_transi_to_same_state = True
            i = 0
            while i < len(current_state.transitions) and all_transi_to_same_state:
                t = current_state.transitions[i]
                j = 0
                while j < len(t.ID_to) and all_transi_to_same_state:
                    ID = t.ID_to[j]
                    if ID != current_state.ID :
                        all_transi_to_same_state = False
                    j += 1
                i += 1
            #Si on en a atteint un , alors on s'arrête
            if current_state.transact == 2 or all_transi_to_same_state :
                if nb_states_random == None :
                    print(f"You have reached a terminal state : {current_state.name}, reward : {current_reward}")
                chemin.append([current_state.name, current_state.transitions[0].name])
                print(chemin)
                return chemin

            elif current_state.transact == False :
                if nb_states_random == None :
                    print("There is no action possible")
                #On récupère la transition actuelle :
                current_transition = current_state.transitions[0]
            
            else :
                #Dans le cas où il n'y a qu'une seul action possible - idem que pas d'actions mais avec 2 lignes de texte en plus aux lignes 91 et 92
                if len(current_state.transitions) == 1 :
                    current_transition = current_state.transitions[0]
                    if nb_states_random == None :
                        print("There is only one action possible and it's : ", current_transition.name)
                        print("You have chosen the action named : ",current_transition.name)
                    #On récupère la transition actuelle :
                    current_transition = current_state.transitions[0]
                    
                #Dans le cas où il ya plusieurs actions possibles
                else :
                    if nb_states_random == None :
                        print("There are ",len(current_state.transitions)," possible actions")
                    possible_transitions = [transi.name for transi in current_state.transitions]
                    if nb_states_random == None :
                        print("These actions are : ", possible_transitions)
                    
                    if nb_states_random == None :
                        bien_choisi = False
                        while not(bien_choisi) :
                            action = input("Choose one action among the possible ones :\n")
                            bien_choisi = action in possible_transitions
                        i = 0
                        current_transition = current_state.transitions[i]
                        while action != current_transition.name :
                            i += 1
                            current_transition = current_state.transitions[i]
                    
                    else :
                        random_transi = randint(0,len(current_state.transitions)-1)
                        current_transition = current_state.transitions[random_transi]
                    
                    if nb_states_random == None :
                        print("You have chosen the action named : ",current_transition.name)
                    #On récupère la transition actuelle :
                    current_transition = current_state.transitions[0]
    
    
            chemin.append([current_state.name, current_transition.name])
        
            #On affiche les possibilités à l'utilisateur :
            possible_next_states_ID = current_transition.ID_to
            possible_next_states_name = []
            for ID in possible_next_states_ID :
                for elt in self.S :
                    if elt.ID == ID :
                        possible_next_states_name.append(elt.name)
            if nb_states_random == None :
                print("The next possible states are : ", possible_next_states_name)
            #On affiche les porbabilités à l'utlisateur :
            list_prob = current_transition.matrix[current_transition.ID_from]
            list_prob = [list_prob[i] for i in possible_next_states_ID]
            if nb_states_random == None :
                print("With a probability respectively of : ",list_prob)
            #On regarde quel sera le prochain état :
            next_state_ID = current_transition.get_next_state_ID(current_state.ID)
            for elt in self.S :
                if next_state_ID == elt.ID :
                    next_state = elt
            if nb_states_random == None :
                print("The next state is : ",next_state.name)

            if nb_states_random == None :
                flag = False
                while not(flag) :
                    answer = input("Do you want to continue ? (y for yes, n for no) :\n")
                    if answer == "y" :
                        flag = True
                        self.run(nb_states_random, next_state, chemin, current_reward)
                    elif answer == "n" :
                        flag = True
                        print(chemin)
                        print(f"Total reward : {current_reward}")
                        return chemin
            
            else :
                self.run(nb_states_random-1,next_state, chemin, current_reward)
            
        else :
            print(f"Total reward : {reward}")
            print(chemin)
    
    
    def adversaire_aleatoire(self):
        """
        Renvoie une politique à suivre construite aléatoirement
        """
        print("Choix d'un adversaire aléatoire")
        politique = dict()
        for state in self.S:
            random_int = np.random.randint(0,len(state.transitions))
            random_transi = state.transitions[random_int]
            politique[state.name] = random_transi.name
        print("politique : ",politique)
        return politique
    
    def adversaire_input(self):
        """
        Demande à l'utilisateur de choisir une politique
        """
        print("\nPlease define a politic")
        politique  = dict()
        for state in self.S:
            list_transition_name = [t.name for t in state.transitions]
            if len(list_transition_name) == 1:
                print(f"\nNo need of a choice for this state : {state.name}")
                politique[state.name] = list_transition_name[0]
            else :
                print(f"\nCurrent state : {state.name}, choose among these transitions :")
                print(list_transition_name)
                correct_anwer = False
                while not correct_anwer :
                    try:
                        print(f"\nChoose among these transitions : {list_transition_name}")
                        answer = input()
                        assert answer in list_transition_name
                        correct_anwer = True
                    except AssertionError:
                        print("\nNot a valid answer")
                        
                politique[state.name] = answer
        return politique
                
    
    def S0_S1_Su_search(self,goal,politique = None) :
        """
        Fonction qui permet de trouver S0,S1 et S? (S unknown)
        
        goal : list(str)
            l'ensemble d'état à atteindre (S1) référencé par leur nom
        
        politique : dict(str:str)
            la politique à adopter lorsque l'on fait un choix
            Si c'est None alors on construit un adversaire aléatoire
        """
        #On vérifie que les états goal appartiennent bien aux états présent dans l'input file
        list_name_state = [s.name for s in self.S]
        try :
            for state in goal:
                assert state in list_name_state
        except AssertionError:
            print("Oops, your goal ins't part of the input file.")
            sys.exit()
        
        #Détection de S0 et S1
        S1 = [goal[i] for i in range(len(goal))]
        S0 = []
        
        finished = False
        
        while not(finished) : #Tant qu'on a pas fini
            changement = 0 #si changement!=0 à la fin de la boucle, alors il y aura eu un ajout dans S0 ou S1
            for state in self.S : #Pour chaque état
                i = 0
                transition = state.transitions[i]
                if politique == None :
                    politique = self.adversaire_aleatoire()
                
                while transition.name != politique[state.name] :
                    i += 1
                    transition = state.transitions[i]
                
                list_possible_next_states_ID = transition.ID_to #on prend la liste des états à suivre
                #Et on retrouve leur nom qu'on met dans list_possible_next_states
                list_possible_next_states = []
                for ID in list_possible_next_states_ID : #FIXME On devrait plutot stcoker les ID et pas chercher les noms à chaque fois
                    for elt in self.S :
                        if elt.ID == ID :
                            list_possible_next_states.append(elt.name)
                
                
                if len(list_possible_next_states) == 0 and (not(state.name in S1)) : #Si pas de successeur et que l'état courant n'est pas dans S1
                    if not(state.name in S0) : #On vérifie qu'on a pas déjà ajouté cet état à la liste
                        S0.append(state.name) #Alors c'est que l'état courant fait partie de S0
                
                elif len(list_possible_next_states) == 1 and (list_possible_next_states[0] == state.name) and (not(state.name in S1)) : #Idem si la seule transition va sur lui-même
                    if not(state.name in S0) : #On vérifie qu'on a pas déjà ajouté cet état à la liste
                        S0.append(state.name)
                
                else :
                    all_S1 = True #Permet de vérifier si tous les états à suivre dans cette transition appartiennent à S1
                    all_S0 = True #idem mais pour S0
                    i = 0 #indice de parcours de la liste des états à suivre
                    while (i < len(list_possible_next_states)) and  (all_S1 or all_S0): #Tant qu'on pas fait tous les états à suivre et que tous ceux qu'on a vu sont soit tous dans S0 soit tous dans S1
                        future_state_name = list_possible_next_states[i] #on prend un état possible
                        if not(future_state_name in S1): #S'il n'est pas dans S1 alors l'état courant n'est pas dans S1
                            all_S1 = False
                        if not(future_state_name in S0):#Idem pour S0
                            all_S0 = False
                        i += 1 #On passe au suivant
                    if all_S1: #Si tous les états à suivre sont dans S1
                        if not(state.name in S1) : #On vérifie qu'on a pas déjà ajouté cet état à la liste
                            S1.append(state.name) #Alors on ajoute l'état actuel dans S1
                            changement += 1 #On fait varier la valeur de la variable changement pour signifier qu'on a ajouté des états dans S1
                    if all_S0 : #Idem dans S0
                        if not(state.name in S0) : #On vérifie qu'on a pas déjà ajouté cet état à la liste
                            S0.append(state.name)
                            changement += 1 #Idem mais pour S0
            if changement == 0 :#Si on a pas eu du changement dans S0 et S1 alors on arrête la recherche de S0 et S1
                finished = True
            
            #On cherche maintenant Su (ie S?,S_unknown)
            Su = []
            for state in self.S:
                if not(state.name in S0) and not(state.name in S1) :
                    Su.append(state.name)

        return S0,S1,Su


    def calcul_proba_inf(self,goal,politique = None):
        """
        Fonction qui calcule la probabilité d'arriver dans un ou plusieurs états sans limite sur le nombre de transitions
        
        goal : list(str)
            l'ensemble d'état à atteindre (S1)
        
        politique : dict(str:str)
            la politique à adopter lorsque l'on fait un choix
            Si c'est None alors on construit un adversaire aléatoire
        """
        #On vérifie que les états goal appartiennent bien aux états présents dans l'input file
        list_name_state = [s.name for s in self.S]
        try :
            for state in goal:
                assert state in list_name_state
        except AssertionError:
            print("Oops, your goal ins't part of the input file.")
            sys.exit()
        
        #On construit l'adversaire aléatoire si la politique n'est pas définie
        if politique == None :
            politique = self.adversaire_aleatoire()
        
        #On vérifie que la politique n'empêche pas d'arriver dans les états goal
        #On récupère les identifiants des états dans goal
        ID_goal = []
        for g in goal :
            i = 0
            possible_name = self.S[i].name
            while possible_name != g :
                i += 1
                possible_name = self.S[i].name
            ID_goal.append(self.S[i].ID)
        accessible = False #Un booléen qui devient vrai si parmi les transitions choisie dans la politique il y en a une qui permet d'aller dans un état de goal
        for name_state in politique.keys():
            if name_state in goal :
                pass
            else :
                name_transition  = politique[name_state]
                #On récupère le bon état
                i = 0
                current_state = self.S[i]
                while current_state.name != name_state :
                    i += 1
                    current_state = self.S[i]
                #On récupère la bonne transition
                i = 0
                current_transi = current_state.transitions[i]
                while current_transi.name != name_transition :
                    i += 1
                    current_transi = current_state.transitions[i]
                #On regarde si les états dans goal sont bien accessibles
                ID_next_states = current_transi.ID_to
                for elt in ID_next_states:
                    if elt in ID_goal:
                        accessible = True
       
        try :
            assert accessible == True
        except AssertionError:
            print("The politic chosen don't lead to the goal you specified")
            sys.exit()
            
        
        #On récupère les informations donnée par la fonction de recherche de S0,S1 et Su
        S0,S1,Su = self.S0_S1_Su_search(goal,politique)
        print(f"Pour cette politique on a trouvé :\tS0 : {S0},\tS1 : {S1},\tSu : {Su}")
        #On récupère les numéros d'ID associé à chaque nom dans Si_ID #FIXME Si on stcoke les numéros d'ID à l'avenir plus besoin de faire ça
        S0_ID,S1_ID,Su_ID = [],[],[]
        List_ID = [S0_ID,S1_ID,Su_ID]
        List_name = [S0,S1,Su]
        for k in range(3) :
            Si = List_name[k]
            Si_ID = List_ID[k]
            for state_name in Si :
                i = 0
                while state_name != self.S[i].name :
                    i += 1
                Si_ID.append(i)
        
        #1ere etape : construire la matrice
        A = np.zeros((len(Su),len(Su)))
        b = np.zeros(len(Su))
        
        #Pour chaque état unknown
        for i in range(len(Su_ID)):
            ID = Su_ID[i]
            #On récupère la bonne transition
            j = 0
            transition = self.S[ID].transitions[j]
            while transition.name != politique[Su[i]] :
                j += 1
                transition = self.S[ID].transitions[j]
            #On récupère la matrice construite pour la transition
            trans_matrix = transition.matrix
            
            #Maintenant on récupère uniquement les informations nécessaires

            #On parcours les états à suivre dans la transition en cours
            for id_to in transition.ID_to:
                #Si létat d'arrivée est dans les états inconnus
                if id_to in Su_ID :
                    #On retrouve le numéro de colonne correspondant dans la matrice A
                    j = 0
                    possible_next_state = Su_ID[j]
                    while id_to != possible_next_state and j < len(Su_ID):
                        j += 1
                        possible_next_state = Su_ID[j]
                        #j contient maintenant le numéro de colonne corespondant dans la matrice A
                    A[i,j] = trans_matrix[ID,id_to]
                    
                #Sinon si l'état d'arrivée est dans les états à atteindre
                elif id_to in S1_ID :
                    #On ajoute la probabilité associée dans b
                    b[i] += trans_matrix[ID,id_to]
                
        #On passe maintenant à la résolution
        Aprime = np.eye(len(A)) - A
        sol = np.linalg.solve(Aprime,b)
        return sol

    
    def Q_learning(self, alpha = 0.1, gamma = 0.99, nb_epochs = 1000, max_iter_episode = 100, exploration_decreasing_decay = 0.001, min_exploration_proba = 0.01):
        """
        Fonction implémentant l'algo de Q-Learning
        alpha : float, 0<alpha<1
            learning rate
        gamma : float, 0<gamma<1
            discounted factor
        """
        
        #Initialisation de la fonction Q
        Q = dict()
        name_to_ID = dict() #Un dictionnaire pour récupérer les identifiants à partir des noms
        for state in self.S:
            Q[state.name] = dict()
            name_to_ID[state.name] = {"ID" : state.ID}
            for transi in state.transitions:
                Q[state.name][transi.name] = 0
                name_to_ID[state.name][transi.name] = transi.ID
        
        #Initialisation pour l'algo
        exploration_proba = 1
        rewards_per_epoch = []
        
        #Début de l'algorithme :
        for e in range(nb_epochs) :
            current_state = self.S[0]
            total_epoch_reward = 0
            for i in range(max_iter_episode) :
                #On choisit une transition aléatoire
                if np.random.uniform(0,1) < exploration_proba :
                    current_transi = current_state.transitions[np.random.randint(0,len(current_state.transitions))]
                #Ou alors on choisit la meilleure transition pour cet état d'après la fonction Q
                else :
                    name_transi_maxi = list(Q[current_state.name].keys())[0]
                    for k in Q[current_state.name].keys():
                        if k == "ID" :
                            pass
                        else :
                            if Q[current_state.name][k] > Q[current_state.name][name_transi_maxi]:
                                name_transi_maxi = k
                    #maintenant on a le nom de la meilleur transition dans name_transi_maxi, il faut retrouver son ID
                    ID_current_transi = name_to_ID[current_state.name][name_transi_maxi]
                    j = 0
                    current_transi = current_state.transitions[j]
                    while current_transi.ID != ID_current_transi:
                        j += 1
                        current_transi = current_state.transitions[j]
                
                #On regarde l'état suivant
                new_state_ID = current_transi.get_next_state_ID()
                new_state = self.S[new_state_ID]
                
                #Mise à jour de la fonction Q
                values_without_ID = [Q[new_state.name][k] for k in Q[new_state.name].keys() if k != "ID"]
                Q[current_state.name][current_transi.name] = (1-alpha)*Q[current_state.name][current_transi.name] + alpha*(new_state.reward + gamma*max(values_without_ID))
                total_epoch_reward += new_state.reward
                
                #Si on est arrivé dans un état finale :
                if new_state.transact == 2 or (len(new_state.transitions)==1 and len(new_state.transitions[0].ID_to)==1 and new_state.transitions[0].ID_to[0]==new_state.ID):
                    break
                current_state = new_state
            
            #On update la fonction de decay
            exploration_proba = max(min_exploration_proba, np.exp(-exploration_decreasing_decay*e))
            rewards_per_epoch.append(total_epoch_reward)
        print("Mean reward per tenth of episodes")
        for i in range(10):
            print((i+1)*len(rewards_per_epoch)//10,": mean espiode reward: " ,np.mean(rewards_per_epoch[len(rewards_per_epoch)//10*i:len(rewards_per_epoch)//10*(i+1)]))
        
        return Q
                
        
        
        

        

class State:

    def __init__(self, ID: int, name : str, reward : float, transitions: list, transact: int):
        self.ID = ID
        self.name = name
        self.reward = reward
        self.transitions = transitions
        self.transact = transact
    
    def __repr__(self) -> str:
        print("ID : ",self.ID)
        print("name : ", self.name)
        print("reward :", self.reward)
        print("transitions : ",self.transitions)
        print("transact : ",self.transact)
        return ""

    @classmethod
    def from_initState(cls, state: str, n_states: int, initState: dict, encoding: dict):
        
        state_ID = encoding[state]
        
        transitions = []
        list_actions = list(initState.keys())
        n_actions = len(list_actions)

        # For each action in this state
        for l in range(n_actions):
            action = list_actions[l]
            if action == "transact" or action == "reward":
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

        return cls(state_ID, state, initState["reward"], transitions, initState["transact"])

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



def main():
    initMDP = dict()

    #lexer = gramLexer(StdinStream())
    lexer = gramLexer(FileStream("../fichiers_test_prof/simu-mdp.mdp"))
    stream = CommonTokenStream(lexer)
    parser = gramParser(stream)
    tree = parser.program()
    printer = gramPrintListener(initMDP)
    
    walker = ParseTreeWalker()
    walker.walk(printer, tree)
    
    mdp = MDP.from_initMDP(initMDP)
    #print(initMDP)
    
    ###################################################
    #Partie run
    choose = input("Do you want to do a simple run of the input file ?[y/n]\n")
    while choose != "y" and choose != "n" :
        choose = input("Do you want to do a simple run of the input file ?[y/n]\n")
    if choose == "y" :
        answer = input("Do you want to play randomly ? [y/n]\n")
        while not(answer == "y" or answer == "n") :
            answer = input("Do you want to play randomly ? [y/n]\n")
        if answer == "n" :
            mdp.run()
        else :
            valid_answer = False
            while not(valid_answer) :
                try:
                    nb_run = int(input("How many states (max) do you want to go through ?:\n"))
                    valid_answer = True
                except ValueError:
                    print("Oops!  That was no valid number.  Try again...")
            mdp.run(nb_run)
    ###################################################
    #Partie calcul proba éventuellement
    choose = input("Do you want to calculate the probality to go in a state ?[y/n]\n")
    while choose != "y" and choose != "n" :
        choose = input("Do you want to calculate the probality to go in a state ?[y/n]\n")
    if choose == "y" :
        #Partie choix d'une politique
        choose = input("Do you want to choose a politic ?[y/n]\n")
        while choose != "y" and choose != "n" :
            choose = input("Do you want to choose a politic ?[y/n]\n")
        if choose == "y":
            pol = mdp.adversaire_input()
        else : 
            pol = mdp.adversaire_aleatoire()
        
        list_name_state = [s.name for s in mdp.S]
        goal = []
        all_chosen = False
        while not all_chosen :
            g = input(f"Choose a state from this list : {list_name_state}[enter to pass]\n")
            if g in goal :
                print("You have already chosen this state")
            elif g in list_name_state:
                    goal.append(g)
                    print(f"The states which are part of the goal are now : {goal}")
            else :
                print(f"This state : {g} isn't a part of the available choice")
                answer = input("Did you have picked all the states ?[y/n]\n")
                while answer != "y" and answer != "n" :
                    answer = input("Did you have picked all the states ?[y/n]\n")
                if answer == "y" :
                    all_chosen = True
        if len(goal) == 0:
            print("You didn't choose any state as a goal, so the calculus is impossible")
            sys.exit()
        print(mdp.calcul_proba_inf(goal,pol))
    ###################################################
    #Partie Q-learning
    choose = input("Do you want to execute Q-Learning ?[y/n]\n")
    while choose != "y" and choose != "n" :
        choose = input("Do you want to execute Q-Learning ?[y/n]\n")
    if choose == "y" :
        
        #choix de alpha
        YN = input("Do you want to choose all the values for Q-Learning ?[y/n]\n")
        while YN != "y" and YN != "n" :
            YN = input("Do you want to choose all the values for Q-Learning ?[y/n]\n")
        if YN == "y" :
            
            #Choix de alpha
            alpha = ""
            while type(alpha) != float:
                alpha = input("Value of alpha :\t")
                try :
                    alpha = float(alpha)
                except ValueError :
                    print("The value of alpha must be a float between 0 and 1, try again")
                
                if type(alpha) == float and not(alpha<1 and alpha>0) :
                    print("The value of alpha must be between 0 and 1, try again")
                    alpha = ""
                    
            #choix de gamma
            gamma = ""
            while type(gamma) != float:
                gamma = input("Value of gamma :\t")
                try :
                    gamma = float(gamma)
                except ValueError :
                    print("The value of gamma must be a float, try again")
        
            #choix de nb_epochs
            nb_epochs = ""
            while type(nb_epochs) != int:
                nb_epochs = input("Value of nb_epochs :\t")
                try :
                    nb_epochs = int(nb_epochs)
                except ValueError :
                    print("The value of nb_epochs must be a int, try again")
        
            #choix de max_iter_epoch
            max_iter_epoch = ""
            while type(max_iter_epoch) != int:
                max_iter_epoch = input("Value of max_iter_epoch :\t")
                try :
                    max_iter_epoch = int(max_iter_epoch)
                except ValueError :
                    print("The value of max_iter_epoch must be a int, try again")
        
            #choix de exploration_decreasing_decay
            explo_decay = ""
            while type(explo_decay) != float:
                explo_decay = input("Value of explo_decay :\t")
                try :
                    explo_decay = float(explo_decay)
                except ValueError :
                    print("The value of explo_decay must be a float, try again")
            
            #choix de min_explo_proba
            min_explo_proba = ""
            while type(min_explo_proba) != float:
                min_explo_proba = input("Value of min_explo_proba :\t")
                try :
                    min_explo_proba = float(min_explo_proba)
                except ValueError :
                    print("The value of min_explo_proba must be a float, try again")
                
                if type(min_explo_proba) == float and not(min_explo_proba<1 and min_explo_proba>0) :
                    print("The value of min_explo_proba must be between 0 and 1, try again")
                    min_explo_proba = ""

            print(mdp.Q_learning(alpha,gamma,nb_epochs,max_iter_epoch,explo_decay,min_explo_proba))
    
        else :
            print(mdp.Q_learning())

    

   

if __name__ == '__main__':
    main()



# try:
#     assert transition.name == "tna" #Si on est pas dans une chaine de markov, alors on ne peut pas utiliser la fonction #FIXME on pourrait suivre une politique dans un MDP
# except AssertionError :
#     print("The input is not a Markov Chain")
#     sys.exit()