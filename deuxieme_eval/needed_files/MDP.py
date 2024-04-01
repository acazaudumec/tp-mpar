import sys
import numpy as np
from random import randint

from needed_files.Transition import *
from needed_files.State import *

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
            Si c'est None alors on regarde si toutes les transitions amènent forcément à un état goal, et si oui alors on le rajoute dans goal
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
                
                if politique != None :
                
                    while transition.name != politique[state.name] :
                        i += 1
                        transition = state.transitions[i]
                    
                    list_possible_next_states_ID = transition.ID_to #on prend la liste des états à suivre
                    #Et on retrouve leur nom qu'on met dans list_possible_next_states
                    list_possible_next_states = []
                    for ID in list_possible_next_states_ID :
                        for elt in self.S :
                            if elt.ID == ID :
                                list_possible_next_states.append(elt.name)
                    
                    
                    if len(list_possible_next_states) == 0 and (not(state.name in S1)) : #Si pas de successeur et que l'état courant n'est pas dans S1
                        if not(state.name in S0) : #On vérifie qu'on a pas déjà ajouté cet état à la liste
                            S0.append(state.name) #Alors c'est que l'état courant fait partie de S0
                            changement += 1
                    
                    elif len(list_possible_next_states) == 1 and (list_possible_next_states[0] == state.name) and (not(state.name in S1)) : #Idem si la seule transition va sur lui-même
                        if not(state.name in S0) : #On vérifie qu'on a pas déjà ajouté cet état à la liste
                            S0.append(state.name)
                            changement += 1
                    
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
                
                
                #Si on a pas défini de politique, alors on fait à peu près la même chose qu'au dessus mais pour chaque transition
                else :
                    nb_transi_in_S0 = 0
                    nb_transi_in_S1 = 0
                    for transition in state.transitions :
                        list_possible_next_states_ID = transition.ID_to #on prend la liste des états à suivre
                        #Et on retrouve leur nom qu'on met dans list_possible_next_states
                        list_possible_next_states = []
                        for ID in list_possible_next_states_ID :
                            for elt in self.S :
                                if elt.ID == ID :
                                    list_possible_next_states.append(elt.name)
                        
                        if len(list_possible_next_states) == 0 and (not(state.name in S1)) : #Si pas de successeur et que l'état courant n'est pas dans S1
                            nb_transi_in_S0 += 1 #Alors c'est que la transition courante permet d'aller vers S0
                        
                        elif len(list_possible_next_states) == 1 and (list_possible_next_states[0] == state.name) and (not(state.name in S1)) : #Idem si la seule transition va sur lui-même
                            nb_transi_in_S0 += 1
                        
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
                            
                            if all_S0 : #Si tous les états à suivre sont dans S0
                                nb_transi_in_S0 += 1 
                            if all_S1 : #Si tous les états à suivre sont dans S1
                                nb_transi_in_S1 += 1
                    
                    if nb_transi_in_S1 == len(state.transitions) :
                        if not(state.name in S1) : #On vérifie qu'on a pas déjà ajouté cet état à la liste
                            S1.append(state.name)
                            changement += 1 #On fait varier la valeur de la variable changement pour signifier qu'on a ajouté des états dans S1
                    if nb_transi_in_S0 == len(state.transitions) :
                        if not(state.name in S0) : #On vérifie qu'on a pas déjà ajouté cet état à la liste
                            S0.append(state.name)
                            changement += 1 #On fait varier la valeur de la variable changement pour signifier qu'on a ajouté des états dans S0
            
            if changement == 0 :#Si on a pas eu du changement dans S0 et S1 alors on arrête la recherche de S0 et S1
                finished = True
            
        #On cherche maintenant Su (ie S?,S_unknown)
        Su = []
        for state in self.S:
            if not(state.name in S0) and not(state.name in S1) :
                Su.append(state.name)

        return S0,S1,Su


    def calcul_proba_sans_borne(self,goal,politique = None):
        """
        Fonction qui calcule, pour une politique donnée, la probabilité d'arriver dans un ou plusieurs états sans limite sur le nombre de transitions
        
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
                #Si l'état d'arrivée est dans les états inconnus
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

    
    def calcul_max_proba_sans_borne(self,goal):
        """
        Fonction calcule la probabilité maximale d'arriver dans un état (ie résolution de A.x >= b)
        
        goal : list(str)
            l'ensemble d'état à atteindre (S1)
        """
        #On vérifie que les états goal appartiennent bien aux états présents dans l'input file
        list_name_state = [s.name for s in self.S]
        try :
            for state in goal:
                assert state in list_name_state
        except AssertionError:
            print("Oops, your goal ins't part of the input file.")
            sys.exit()
        
        #On récupère les informations donnée par la fonction de recherche de S0,S1 et Su
        S0,S1,Su = self.S0_S1_Su_search(goal)
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
        nb_row_A = 0 #Le nombre de ligne de la matrice A
        #Pour chaque état unknown
        for ID in Su_ID :
            current_state = self.S[ID]
            #On regarde le nombre de transitions qui existe à partir de cet état et on l'ajoute à nb_row_A
            nb_row_A += len(current_state.transitions)
            #On ajoute les deux lignes pour que x soit compris dans [0,1]
            nb_row_A += 2
            
        A = np.zeros((nb_row_A,len(Su)))
        b = np.zeros(nb_row_A)
        
        #Etape 1bis: remplir la matrice A
        row_matrix_A = 0 #L'indice de parcours des lignes de la matrice A
        for i in range(len(Su_ID)):
            ID = Su_ID[i]
            current_state = self.S[ID]
            for t in current_state.transitions :
                trans_matrix = t.matrix
                #Maintenant on récupère uniquement les informations nécessaires
                #On parcours les états à suivre dans la transition en cours
                for id_to in t.ID_to:
                    #Si l'état d'arrivée est dans les états inconnus
                    if id_to in Su_ID :
                        #On retrouve le numéro de colonne correspondant dans la matrice A
                        j = 0
                        possible_next_state = Su_ID[j]
                        while id_to != possible_next_state and j < len(Su_ID):
                            j += 1
                            possible_next_state = Su_ID[j]
                            #j contient maintenant le numéro de colonne corespondant dans la matrice A
                        A[row_matrix_A,j] = -trans_matrix[ID,id_to]
                        
                    #Sinon si l'état d'arrivée est dans les états à atteindre
                    elif id_to in S1_ID :
                        #On ajoute la probabilité associée dans b
                        b[row_matrix_A] += trans_matrix[ID,id_to]
                        
                #Quand on fait la transition pour cet état, on passe à la trnsition d'après
                row_matrix_A += 1
                
            #Quand on a fait toutes les transitions de l'état courant on peut rajouter les valeurs correspondantes pour que x appartiennent à [0,1]
            row_matrix_A += 1 #On passe à la ligne suivante parce que celle pour >0 est vide
            #On doit mettre -1 à la bonne colonne dans A (pour x<1) et -1 dans b à cette même ligne
            j = 0
            possible_correct_col = Su_ID[j]
            while current_state.ID != possible_correct_col and j < len(Su_ID):
                j += 1
                possible_correct_col = Su_ID[j]
                #j contient maintenant le numéro de colonne corespondant dans la matrice A
            A[row_matrix_A,j] = -1
            b[row_matrix_A] = -1
            #Une fois qu'on a mis les -1 on peut passer à la ligne suivante
            row_matrix_A += 1
        
        #2e etape : après avoir rempli A et b, il faut résoudre Ax = b
        x,residu,rank,s = np.linalg.lstsq(A,b,rcond=None)
        return x
    
    
    
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
        print("Mean reward per tenth of number of epochs")
        for i in range(10):
            print((i+1)*len(rewards_per_epoch)//10,": mean espiode reward: " ,np.mean(rewards_per_epoch[len(rewards_per_epoch)//10*i:len(rewards_per_epoch)//10*(i+1)]))
        
        return Q