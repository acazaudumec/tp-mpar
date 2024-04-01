from needed_files.Transition import *

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