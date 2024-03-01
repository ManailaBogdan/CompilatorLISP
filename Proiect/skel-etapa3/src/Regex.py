from .NFA import NFA
from .NFA import EPSILON

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