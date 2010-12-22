''' Some common, and not so common, sequence operations. '''

def iterable(a): #TODO doctests
    ''' Tests if an object is iterable (but lies that str/unicode are not). 
    
    Attempts to makes a generator out of a sequence and then discards it
    which works for both __iter__ and __getitem__ iterable interfaces.

    Adapted from http://stackoverflow.com/questions/1952464/in-python-how-do-i-determine-if-a-variable-is-iterable/1952507#1952507
    '''
    if isinstance(a, basestring):
        return False
    try:
        (x for x in a)
        return True
    except TypeError:
        return False


def copy(l): #TODO doctests
    ''' Returns a copy of the list l.

    Using copy(l) just makes the intention more explicit (e.g. in pseudo - code).
    '''
    return l[:]


def unique(l): #TODO doctests
    ''' Returns the list with duplicates removed.

    From http: // stackoverflow.com / questions / 89178 / #91430

    Modifies the list in - place for speed and memory, use unique(copy(l)) if you
    don't want the list to be modified.
    '''
    s = set(); n = 0
    for x in l:
        if x not in s: s.add(x); l[n] = x; n += 1
    del l[n:]
    return l


def overlapping(left, right): #TODO doctests
    for c in reversed(range(len(right))):
        c += 1
        r = right[0:c]
        l = left[-c:]
        if list(l) == list(r):
            return r
    t = type(left) or type(right)
    return t()

def join_overlapping(left, right): #TODO doctests
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
#    # alternative implementation:    
#    w = len(str(n))
#    import string
#    return [string.zfill(i, w) for i in range(n)]


def flatten(a): #TODO doctests
    ''' Flatten a list. 
    
    (from http://www.archivum.info/tutor@python.org/2005-01/00506/Re:-[Tutor]-flattening-a-list.html) '''
    def bounce(thing):
        """Bounce the 'thing' until it stops being a callable."""
        while callable(thing):
            thing = thing()
        return thing
    def flatten_k(a, k):
        ''' CPS/trampolined version of the flatten function.  The original
        function, before the CPS transform, looked like this:
    
        def flatten(a):
            if not isinstance(a,(tuple,list)): return [a]
            if len(a)==0: return []
            return flatten(a[0])+flatten(a[1:])
    
        The following code is not meant for human consumption.
        '''
        if isinstance(a, dict) or not iterable(a): #not isinstance(a, (tuple, list)):
            return lambda: k([a])
        if len(a) == 0:
            return lambda: k([])
        def k1(v1):
            def k2(v2):
                return lambda: k(v1 + v2)
            return lambda: flatten_k(a[1:], k2)
        return lambda: flatten_k(a[0], k1)
    return bounce(flatten_k(a, lambda x: x))


def flattened(f): #TODO doctests
    ''' Decorator that flattens the returned sequence. 
    
    See http://www.artima.com/weblogs/viewpost.jsp?thread=240808 for more on decorators.
    
    '''
    def decorated(*args, **kwargs):
        return flatten(f(*args, **kwargs))
    decorated.__name__ = f.__name__ # otherwise returned .__name__ = 'new_f'
    decorated.__doc__ = f.__doc__ # ditto for docstring
    return decorated


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

def findall(L, value, start=0): #TODO doctests
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

def in_all_sequences(sub, S): #TODO doctests
    for s in S:
        if not in_sequence(sub, s):
            return False
    return True


def arrange(sequence): #TODO doctests
    ''' Returns the smallest rows x columns tuple for a given number of items.
    
    Adapted from Pawel's tiling code.
    
    '''
    number = len(sequence)
    import math
    rows = math.sqrt(number / math.sqrt(2))
    cols = rows * math.sqrt(2)
    if number <= math.ceil(rows) * math.floor(cols):
        rows = int(math.ceil(rows))
        cols = int(math.floor(cols))
    elif number <= math.floor(rows) * math.ceil(cols):
        rows = int(math.floor(rows))
        cols = int(math.ceil(cols))
    else:
        rows = int(math.ceil(rows))
        cols = int(math.ceil(cols))
    return (rows, cols)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
