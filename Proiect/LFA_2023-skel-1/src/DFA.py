from collections.abc import Callable
from dataclasses import dataclass


@dataclass
class DFA[STATE]:
    S: set[str]
    K: set[STATE]
    q0: STATE
    d: dict[tuple[STATE, str], STATE]
    F: set[STATE]

    def __init__(self):
        self.S = set()
        self.K = set()
        self.q0 = None
        self.d = dict()
        self.F = set()
        pass

    def __str__(self):
        print("S: ", self.S)
        print("K: ", self.K)
        print("q0: ", self.q0)
        print("d: ", self.d)
        print("F: ", self.F)
        return ""

    
    def accept(self, word: str) -> bool:
        # simulate the dfa on the given word. return true if the dfa accepts the word, false otherwise
        q = self.q0
        for c in word:
            q = self.d[(q, c)]
        
        return q in self.F

    def remap_states[OTHER_STATE](self, f: Callable[[STATE], 'OTHER_STATE']) -> 'DFA[OTHER_STATE]':
        # optional, but might be useful for subset construction and the lexer to avoid state name conflicts.
        # this method generates a new dfa, with renamed state labels, while keeping the overall structure of the
        # automaton.

        # for example, given this dfa:

        # > (0) -a,b-> (1) ----a----> ((2))
        #               \-b-> (3) <-a,b-/
        #                   /     ⬉
        #                   \-a,b-/

        # applying the x -> x+2 function would create the following dfa:

        # > (2) -a,b-> (3) ----a----> ((4))
        #               \-b-> (5) <-a,b-/
        #                   /     ⬉
        #                   \-a,b-/

        dfa = DFA[OTHER_STATE]()

        dfa.S = self.S
        dfa.K = set(map(f, self.K))
        dfa.q0 = f(self.q0)
        dfa.d = DFA[OTHER_STATE].d = dict(map(lambda x: ((f(x[0][0]), x[0][1]), f(x[1]))), self.d)
        dfa.F = set(map(f, self.F))

        pass

