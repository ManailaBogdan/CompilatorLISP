from dataclasses import dataclass
from collections.abc import Callable
EPSILON = ''  # this is how epsilon is represented by the checker in the transition function of NFAs


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
            if (q, c) not in self.d:
                return False
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
        



A_BIG = "[A-Z]"
A_SMALL = "[a-z]"
NUM = "[0-9]"
CONCAT = "++"

class Regex:
    A_BIG = "[A-Z]"
    A_SMALL = "[a-z]"
    NUM = "[0-9]"
    CONCAT = "++"
    List: []

    def __init__(self, List):
        self.List = List

    def thompson(self) -> NFA[int]:
        if self.List[0] == A_BIG:
            nfa = NFA[int](set(), set(), 0, dict(), set())
            nfa.S = set([chr(i) for i in range(ord('A'), ord('Z')+1)])
            nfa.K = set([0, 1])
            nfa.q0 = 0
            nfa.d = dict()
            for i in range(ord('A'), ord('Z')+1):
                nfa.d[(0, chr(i))] = set([1])
            nfa.F = set([1])
            return nfa
        if self.List[0] == A_SMALL:
            nfa = NFA[int](set(), set(), 0, dict(), set())
            nfa.S = set([chr(i) for i in range(ord('a'), ord('z')+1)])
            nfa.K = set([0, 1])
            nfa.q0 = 0
            nfa.d = dict()
            for i in range(ord('a'), ord('z')+1):
                nfa.d[(0, chr(i))] = set([1])
            nfa.F = set([1])
            return nfa
        if self.List[0] == NUM:
            nfa = NFA[int](set(), set(), 0, dict(), set())
            nfa.S = set([chr(i) for i in range(ord('0'), ord('9')+1)])
            nfa.K = set([0, 1])
            nfa.q0 = 0
            nfa.d = dict()
            for i in range(ord('0'), ord('9')+1):
                nfa.d[(0, chr(i))] = set([1])
            nfa.F = set([1])
            return nfa 
        if '\\' in self.List[0]:
            nfa = NFA[int](set(), set(), 0, dict(), set())
            nfa.S = set([self.List[0][1]])
            nfa.K = set([0, 1])
            nfa.q0 = 0
            nfa.d = dict()
            nfa.d[(0, self.List[0][1])] = set([1])
            nfa.F = set([1])
            return nfa
        if self.List[0] not in [CONCAT, "|", "+", "*", "?"]:
            nfa = NFA[int](set(), set(), 0, dict(), set())
            nfa.S = set([self.List[0]])
            nfa.K = set([0, 1])
            nfa.q0 = 0
            nfa.d = dict()
            nfa.d[(0, self.List[0])] = set([1])
            nfa.F = set([1])
            return nfa
        if self.List[0] == CONCAT:
            nfa1 = Regex(self.List[1]).thompson()
            nfa2 = Regex(self.List[2]).thompson()
            nfa = NFA[int](set(), set(), 0, dict(), set())
            nfa.S = nfa1.S.union(nfa2.S)
            nfa.K = nfa1.K.union(map(lambda x: x+len(nfa1.K), nfa2.K))
            nfa.q0 = 0
            nfa.d = dict()
            for i in nfa1.d:
                nfa.d[i] = nfa1.d[i]
            nfa.d[(len(nfa1.K)-1, EPSILON)] = set([len(nfa1.K)])
            for i in nfa2.d:
                nfa.d[(i[0]+len(nfa1.K), i[1])] = set(map(lambda x: x+len(nfa1.K), nfa2.d[i]))
            nfa.F = set(map(lambda x: x+len(nfa1.K), nfa2.F))  
            return nfa
        if self.List[0] == "|":
            nfa1 = Regex(self.List[1]).thompson()
            nfa2 = Regex(self.List[2]).thompson()
            nfa = NFA[int](set(), set(), 0, dict(), set())
            nfa.S = nfa1.S.union(nfa2.S)
            for i in range(len(nfa1.K) + len(nfa2.K) + 2):
                nfa.K.add(i)
            nfa.q0 = 0
            nfa.d = dict()
            nfa.d[(0, EPSILON)] = set([1, len(nfa1.K)+1])
            for i in nfa1.d:
                nfa.d[i[0]+1, i[1]] = set(map(lambda x: x+1, nfa1.d[i]))
            for i in nfa2.d:
                nfa.d[i[0]+len(nfa1.K)+1, i[1]] = set(map(lambda x: x+len(nfa1.K)+1, nfa2.d[i]))
            nfa.d[len(nfa1.K), EPSILON] = set([len(nfa1.K)+len(nfa2.K)+1])
            nfa.d[len(nfa1.K)+len(nfa2.K), EPSILON] = set([len(nfa1.K)+len(nfa2.K)+1])
            nfa.F = set([len(nfa1.K)+len(nfa2.K)+1])
            return nfa
        if self.List[0] == "*":
            nfa1 = Regex(self.List[1]).thompson()
            nfa = NFA[int](set(), set(), 0, dict(), set())
            nfa.S = nfa1.S
            for i in range(len(nfa1.K) + 2):
                nfa.K.add(i)
            nfa.q0 = 0
            nfa.d = dict()
            nfa.d[(0, EPSILON)] = set([1, len(nfa1.K)+1])
            for i in nfa1.d:
                nfa.d[i[0]+1, i[1]] = set(map(lambda x: x+1, nfa1.d[i]))
            nfa.d[len(nfa1.K), EPSILON] = set([1, len(nfa1.K)+1])
            nfa.F = set([len(nfa1.K)+1])
            return nfa
        if self.List[0] == "+":
            nfa1 = Regex(self.List[1]).thompson()
            nfa = NFA[int](set(), set(), 0, dict(), set())
            nfa.S = nfa1.S
            for i in range(len(nfa1.K) + 2):
                nfa.K.add(i)
            nfa.q0 = 0
            nfa.d = dict()
            nfa.d[(0, EPSILON)] = set([1])
            for i in nfa1.d:
                nfa.d[i[0]+1, i[1]] = set(map(lambda x: x+1, nfa1.d[i]))
            nfa.d[len(nfa1.K), EPSILON] = set([1, len(nfa1.K)+1])
            nfa.F = set([len(nfa1.K)+1])
            return nfa
        if self.List[0] == "?":
            nfa1 = Regex(self.List[1]).thompson()
            nfa = NFA[int](set(), set(), 0, dict(), set())
            nfa.S = nfa1.S
            for i in range(len(nfa1.K) + 2):
                nfa.K.add(i)
            nfa.q0 = 0
            nfa.d = dict()
            nfa.d[(0, EPSILON)] = set([1, len(nfa1.K)+1])
            for i in nfa1.d:
                nfa.d[i[0]+1, i[1]] = set(map(lambda x: x+1, nfa1.d[i]))
            nfa.d[len(nfa1.K), EPSILON] = set([len(nfa1.K)+1])
            nfa.F = set([len(nfa1.K)+1])
            return nfa
        raise NotImplementedError('the thompson method of the Regex class should never be called')

# you should extend this class with the type constructors of regular expressions and overwrite the 'thompson' method
# with the specific nfa patterns. for example, parse_regex('ab').thompson() should return something like:

# >(0) --a--> (1) -epsilon-> (2) --b--> ((3))

# extra hint: you can implement each subtype of regex as a @dataclass extending Regex

def help(list):
    aux = list[0]
    list.pop(0)
    if aux in [CONCAT, "|"]:
        return [aux, help(list), help(list)]
    elif aux in ["+", "*", "?"]:
        return [aux, help(list)]
    else:
        return [aux]
    
def parse_regex(regex: str) -> Regex:
    # create a Regex object by parsing the string
    s = regex
    new = []
    ok = True
    for i in range(len(s)):
        if s[i] == '[':
            if s[i+1] == 'A':
                new.append(A_BIG)
            elif s[i+1] == 'a':
                new.append(A_SMALL)
            elif s[i+1] == '0':
                new.append(NUM)
            ok = False
        elif s[i] == ']':
            ok = True
        elif ok:
            new.append(s[i])


    s = new
    new = []
    ok = False
    for i in range(len(s)):
        if ok:
            new.append('\\' + s[i])
            ok = False
        elif s[i] == '\\':
            ok = True
        else:
            new.append(s[i])

    s = new 
    s = [x for x in s if x != ' ']

    new = []

    for i in range(len(s)-1):
        new.append(s[i])
        if s[i] not in ['|', '('] and s[i+1] not in ['|', '+', '*', '?', ')']:
            new.append(CONCAT)

    new.append(s[-1])

    s = new
   
    visited = [False for i in range(len(s))]
    
    while True:
        for i in reversed(range(len(s))):
            if not visited[i]:
                if s[i] in ["+", "*", "?"]:    
                    paranteze = 0
                    for j in reversed(range(i)):
                        if s[j] == ')':
                            paranteze += 1
                        elif s[j] == '(':
                            paranteze -= 1
                
                        if s[j] not in [CONCAT, '|', '+', '*', '?'] and paranteze == 0:
                            s.insert(j, '(')
                            s.insert(j+1, s[i + 1])
                            s.insert(i+2, ')')
                            visited.insert(j, True)
                            visited.insert(j+1, True)
                            visited.insert(i+2, True)
                            s.pop(i+3)
                            visited.pop(i+3)
                            break
                else:
                    visited[i] = True
        if False not in visited:
            break

    

    ok = False
    new = []
    paranteze = 0
    for i in range(len(s)-1):
        if s[i] not in [CONCAT, '|', '(', ')', '*', '+', '?'] and s[i+1] == CONCAT and not ok:
            new.append('(')
            paranteze += 1
            ok = True
        elif ok:
            if s[i] in ['|', ')']:
                new.append(')')
                paranteze -= 1
                ok = False
        if s[i] == '(':
            ok = False
        if s[i] == ')' and paranteze != 0:
            ok = True
        
        new.append(s[i])

    new.append(s[-1])
    
    if paranteze != 0:
        for i in range(paranteze):
            new.append(')')
    
    s = new

    
   
    visited = [False for i in range(len(s))]
    while True:
        for i in reversed(range(len(s))):
            if not visited[i]:
                if s[i] in [CONCAT, "|"]:    
                    paranteze = 0
                    for j in reversed(range(i)):
                        if s[j] == ')':
                            paranteze += 1
                        elif s[j] == '(':
                            paranteze -= 1
                
                        if s[j] not in [CONCAT, '|', '+', '*', '?'] and paranteze == 0:
                            s.insert(j, s[i])
                            visited.insert(j, True)
                            s.pop(i+1)
                            visited.pop(i+1)
                            break
                else:
                    visited[i] = True
        if False not in visited:
            break

    
    
    s = [i for i in s if i not in ['(', ')']]
    s = help(s)
    regex = Regex(s)

    return regex

    # you can define additional classes and functions to help with the parsing process

    # the checker will call this function, then the thompson method of the generated object. the resulting NFA's
    # behaviour will be checked using your implementation form stage 1
    pass


class Lexer:
    S = DFA[int]()
    T = []
    character = -1
    line = 0
   

    def __init__(self, spec: list[tuple[str, str]]) -> None:
        # initialisation should convert the specification to a dfa which will be used in the lex method
        # the specification is a list of pairs (TOKEN_NAME:REGEX)
        
        nfa = NFA[int](set(), set(), 0, dict(), set())
        nfa.K.add(0)
     
        initials = []

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

def verify(lexer: Lexer, tests):
	results = []
	for word, ref in tests:
		results.append(lexer.lex(word) == ref)
        
	return results


spec = [
			("SPACE", "\\ "),
			("NEWLINE", "\n"),
			("ABC", "a(b+)c"),
			("AS", "a+"),
			("BCS", "(bc)+"),
			("DORC", "(d|c)+")
		]

lexer = Lexer(spec)

tests = [
			("abcbcbcaabaad dccbca", [("", "No viable alternative at character 10, line 0")]),
			("d abdbc ccddabbbc", [("", "No viable alternative at character 4, line 0")]),
			("d a\nbdbc ccddabbbc", [("", "No viable alternative at character 1, line 1")]),
			("e abbbcbcaadc c", [("", "No viable alternative at character 0, line 0")]),  # this has a char not in the spec
			("dccbcbcaaaa abbcf", [("", "No viable alternative at character 16, line 0")]),  # this has a char not in the spec
			("abbcaaabc dcccabcb", [("", "No viable alternative at character EOF, line 0")]),
			("abbc\naaabc dcccabcb", [("", "No viable alternative at character EOF, line 1")]),
			("dcdccaabcabb dcaabc", [("", "No viable alternative at character 11, line 0")]),
			("\naaa\nbabbcbcbc abbbcaabc", [("", "No viable alternative at character 1, line 2")])
		]

for word, ref in tests:
    print(word)
    print(lexer.lex(word))
    print(ref)
    print(lexer.lex(word) == ref)
