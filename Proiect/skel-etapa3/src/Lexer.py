from src.DFA import DFA
from src.NFA import EPSILON
from src.NFA import NFA
from src.Regex import Regex
from src.Regex import parse_regex


class Lexer:
    S = DFA[int]()
    T = []

    def __init__(self, spec: list[tuple[str, str]]) -> None:
        # initialisation should convert the specification to a dfa which will be used in the lex method
        # the specification is a list of pairs (TOKEN_NAME:REGEX)
        
        nfa = NFA[int](set(), set(), 0, dict(), set())
        nfa.K.add(0)
     
        initials = []
        self.T = []

        for token_name, regex in spec:
            n = parse_regex(regex).thompson()
            n.K = [x + len(nfa.K) for x in n.K]
            n.F = [x + len(nfa.K) for x in n.F]
            n.q0 = n.q0 + len(nfa.K)
            n.d = {(x + len(nfa.K), y): [z + len(nfa.K) for z in n.d[(x, y)]] for (x, y) in n.d}
            nfa.S = nfa.S.union(n.S)
            nfa.K = nfa.K.union(n.K)
            nfa.F = nfa.F.union(n.F)
            nfa.d = {**nfa.d, **n.d}
            initials.append(n.q0)

            for x in n.F:
                self.T.append((x, token_name))

        nfa.d[(0, EPSILON)] = initials

        self.S = nfa.subset_construction()

        
           
        pass

    def lex(self, word: str) -> list[tuple[str, str]] | None:
        # this method splits the lexer into tokens based on the specification and the rules described in the lecture
        # the result is a list of tokens in the form (TOKEN_NAME:MATCHED_STRING)

       
        rez = []
        last_longest = tuple()
        curent_word = ""
        curent_state = self.S.q0
        last_i = -1
        last_line = 0
        last_character = -1

        character = -1
        line = 0
        i = -1
        while i < len(word) - 1:
            i += 1
            
            curent_word += word[i]
            character += 1
            if word[i] == '\n':
                line += 1
                character = -1

            if(word[i] not in self.S.S):
                error = "No viable alternative at character " + str(character) + ", line " + str(line)
                return [("", error)]
           

            curent_state = self.S.d[(curent_state, word[i])]

            if curent_state in self.S.F:
                token = ""
                for x, y in self.T:
                    if (x in curent_state):
                        token = y
                        break
                last_longest = (token, curent_word)
                last_i = i
                last_line = line
                last_character = character
               
                

            if curent_state == frozenset():
                if(last_longest == tuple()):
                    error = "No viable alternative at character " + str(character) + ", line " + str(line)
                    return [("", error)]
                rez.append(last_longest)
                last_longest = tuple()
                curent_word = ""
                curent_state = self.S.q0
                i = last_i
                line = last_line
                character = last_character

                
                
               
            
        
        if(last_longest != tuple()):
            rez.append(last_longest)
        else:
            error = "No viable alternative at character EOF, line " + str(line)
            return [("", error)]

        if rez != []:
            return rez
        else:
            error = "No viable alternative at character EOF, line " + str(line)
            return [("", error)]

        # if an error occurs and the lexing fails, you should return none # todo: maybe add error messages as a task
        pass

