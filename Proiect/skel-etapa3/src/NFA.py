from .DFA import DFA

from dataclasses import dataclass
from collections.abc import Callable

EPSILON = ''  # this is how epsilon is represented by the checker in the transition function of NFAs


@dataclass
class NFA[STATE]:
    S: set[str]
    K: set[STATE]
    q0: STATE
    d: dict[tuple[STATE, str], set[STATE]]
    F: set[STATE]

    

    def __str__(self):
        print("S: ", self.S)
        print("K: ", self.K)
        print("q0: ", self.q0)
        print("d: ", self.d)
        print("F: ", self.F)
        return ""

    def epsilon_closure_help(self, state: STATE, visited: set[STATE]):

        if state not in visited:
            visited.add(state)
            if (state, EPSILON) in self.d:
                for s in self.d[(state, EPSILON)]:
                    self.epsilon_closure_help(s, visited)
        pass

    def epsilon_closure(self, state: STATE) -> set[STATE]:
        # compute the epsilon closure of a state (you will need this for subset construction)
        # see the EPSILON definition at the top of this file

        epsilon_set = set()
        self.epsilon_closure_help(state, epsilon_set)
        return epsilon_set
        

    def subset_construction(self) -> DFA[frozenset[STATE]]:
        # convert this nfa to a dfa using the subset construction algorithm
        dfa = DFA[frozenset[STATE]]()
        dfa.S = self.S
        dfa.K = set()
        dfa.q0 = frozenset(self.epsilon_closure(self.q0))
        dfa.K.add(dfa.q0)
        dfa.d = dict()
        dfa.F = set()

        queue = [dfa.q0]
        sink: STATE
        
        while queue:
            state = queue.pop(0)
            
            for c in dfa.S:
                next = set()
                for s in state:
                    if (s, c) in self.d:
                        for x in self.d[(s, c)]:
                            next.add(x)
                            next = next.union(self.epsilon_closure(x))
                next = frozenset(next)
                if next not in dfa.K:
                    dfa.K.add(next)
                    queue.append(next)
                dfa.d[(state, c)] = next
        
        for state in dfa.K:
            for s in state:
                if s in self.F:
                    dfa.F.add(state)
                    break

        return dfa
        

    def remap_states[OTHER_STATE](self, f: 'Callable[[STATE], OTHER_STATE]') -> 'NFA[OTHER_STATE]':
        # optional, but may be useful for the second stage of the project. Works similarly to 'remap_states'
        # from the DFA class. See the comments there for more details.

        dfa = DFA[OTHER_STATE]()

        dfa.S = self.S
        dfa.K = set(map(f, self.K))
        dfa.q0 = f(self.q0)
        dfa.d = DFA[OTHER_STATE].d = dict(map(lambda x: ((f(x[0][0]), x[0][1]), set(map(f, x[1])))), self.d)
        dfa.F = set(map(f, self.F))

        return dfa
        
