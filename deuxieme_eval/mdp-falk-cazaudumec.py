from antlr4 import *
from gramLexer import gramLexer
from gramListener import gramListener
from gramParser import gramParser
import sys
import numpy as np

from needed_files.Transition import *
from needed_files.State import *
from needed_files.MDP import *
from needed_files.gramPrintListener import *


def main():
    initMDP = dict()

    #lexer = gramLexer(StdinStream())
    lexer = gramLexer(FileStream("../fichiers_test_prof/fichier3-mdp.mdp"))
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
    choose = input("Do you want to calculate the probality to go in a state (without any restiction of the number of transition)?[y/n]\n")
    while choose != "y" and choose != "n" :
        choose = input("Do you want to calculate the probality to go in a state (without any restiction of the number of transition)?[y/n]\n")
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
        print(mdp.calcul_proba_sans_borne(goal,pol))
    ###################################################
    #Partie calcul max proba éventuellement
    choose = input("Do you want to calculate the maximum probality to go in a state (without any restiction of the number of transition)?[y/n]\n")
    while choose != "y" and choose != "n" :
        choose = input("Do you want to calculate the maximum probality to go in a state (without any restiction of the number of transition)?[y/n]\n")
    if choose == "y" :
        #Choose a goal
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
        print(mdp.calcul_max_proba_sans_borne(goal))
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

            print(f"\nLa fonction Q :\n{mdp.Q_learning(alpha,gamma,nb_epochs,max_iter_epoch,explo_decay,min_explo_proba)}")
    
        else :
            print(mdp.Q_learning())


if __name__ == '__main__':
    main()