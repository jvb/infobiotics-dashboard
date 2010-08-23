'''
Some common, and not so common, sequence operations.
'''

def copy(l):
    '''
    Returns a copy of the list l. 
    '''
    return l[:]


def unique(l):
    '''
    From http://stackoverflow.com/questions/89178/#91430
    Returns list of unique items from a list with duplicates.
    Warning: this modifies the list in-place for speed, use unique(copy(l)) 
    if you don't want your list modified.
    '''
    s = set(); n = 0
    for x in l:
        if x not in s: s.add(x); l[n] = x; n += 1
    del l[n:]
    return l


def overlapping(left, right):
    for c in reversed(range(len(right))):
        c += 1
        r = right[0:c]
        l = left[-c:]
        if list(l) == list(r):
            return r
    t = type(left) or type(right)
    return t()

def join_overlapping(left, right):
    o = overlapping(left, right)
    t = type(o)
    l = list(left[:])
    l += right[len(o):]
    return t(l)


def padded_range(n, padding_char='0'):
    ''' Returns a list of padded integers in the interval 0 < n. 
    
    >>> padded_range(10)
    ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09']
    
    >>> padded_range(5)
    ['0', '1', '2', '3', '4']
    
    '''
    return [str(padding_char[0]) * (len(str(n)) - len(str(i))) + str(i) for i in range(n)]


def flatten(a):
    ''' Flatten a list. (from http://www.archivum.info/tutor@python.org/2005-01/00506/Re:-[Tutor]-flattening-a-list.html) '''
    def bounce(thing):
        """Bounce the 'thing' until it stops being a callable."""
        while callable(thing):
            thing = thing()
        return thing
    def flatten_k(a, k):
        """CPS/trampolined version of the flatten function.  The original
        function, before the CPS transform, looked like this:
    
        def flatten(a):
            if not isinstance(a,(tuple,list)): return [a]
            if len(a)==0: return []
            return flatten(a[0])+flatten(a[1:])
    
        The following code is not meant for human consumption.
        """
        if not isinstance(a, (tuple, list)):
            return lambda: k([a])
        if len(a) == 0:
            return lambda: k([])
        def k1(v1):
            def k2(v2):
                return lambda: k(v1 + v2)
            return lambda: flatten_k(a[1:], k2)
        return lambda: flatten_k(a[0], k1)
    return bounce(flatten_k(a, lambda x: x))

def k_common_subsequence(sequences):
    ''' Returns the set of longest common subsequences in a collection of 
    sequences.

    See LCSubstr_set for longest common subsequence algorithm.

    >>> a = (0,1,2)
    >>> b = (0,2,4)
    >>> c = (1,2,3,4,5,6)
    >>> k_common_subsequence((a,b,c))
    [(2,)]
    
    >>> strings = ['hello', 'fellow', 'mellowing', 'bellowing']
    >>> k_common_subsequence(strings)
    ['ello']
    >>> def padded_range(n, padding_char='0'): return [str(padding_char[0]) * (len(str(n)) - len(str(i))) + str(i) for i in range(n)]
    >>> k_common_subsequence(padded_range(10))
    ['0']
    >>> k_common_subsequence(padded_range(100)) 
    ['0']
    
    '''
    import itertools
#    S = set(flatten([list(LCSubstr_set(s, t)) for s, t in itertools.combinations(sequences, 2)]))
    S = set(itertools.chain.from_iterable([LCSubstr_set(s, t) for s, t in itertools.combinations(sequences, 2)])) # itertools.chain.from_iterable is a one-level flatten 
#    S = sorted(S, key=len, reverse=True)
    return [s for s in S if in_all_sequences(s, sequences)]

def LCSubstr_set(S, T):
    ''' Returns the set of longest common subsequences in 2 sequences.
    
    Lifted from: http://en.wikibooks.org/wiki/Algorithm_implementation/Strings/Longest_common_substring#Python

    Python strings are sequences so this also works for them.
    
    >>> LCSubstr_set('hello world', 'hello_world')
    set(['world', 'hello'])
    
    '''
    m = len(S); n = len(T)
    L = [[0] * (n + 1) for i in xrange(m + 1)]
    LCS = set()
    len_longest = 0
    for i in xrange(m):
        for j in xrange(n):
            if S[i] == T[j]:
                v = L[i][j] + 1
                L[i + 1][j + 1] = v
                if v > len_longest:
                    len_longest = v
                    LCS = set()
                if v == len_longest:
                    LCS.add(S[i - v + 1:i + 1])
    return LCS

def findall(L, value, start=0):
    ''' Lifted from: http://effbot.org/zone/python-list.htm '''
    # generator version
    i = start - 1
    try:
        i = L.index(value, i + 1)
        yield i
    except ValueError:
        pass

def in_sequence(sub, sequence):
    ''' 
    
    >>> a = (1,2,3)
    >>> b = (1,2,4)
    >>> c = (1,2,3,4,5,6)
    >>> in_sequence(a,b)
    False
    >>> in_sequence(a,c)
    True
    >>> in_sequence(b,c)
    False

    >>> in_sequence('ello', 'hello')
    True
    >>> in_sequence('elo', 'hello')
    False

    '''
    l = len(sub)
    for i in findall(sequence, sub[0]):
        if sequence[i:l + i] == sub:
            return True
    return False

def in_all_sequences(sub, S):
    for s in S:
        if not in_sequence(sub, s):
            return False
    return True


if __name__ == "__main__":
    import doctest
    doctest.testmod()
