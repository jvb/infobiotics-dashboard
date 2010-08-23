'''
Some common, and not so common, sequence operations.
'''

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


def copy(l):
    '''
    Returns a copy of the list l. 
    '''
    return l[:]


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
        if not isinstance(a,(tuple,list)):
            return lambda: k([a])
        if len(a)==0:
            return lambda: k([])
        def k1(v1):
            def k2(v2):
                return lambda: k(v1 + v2)
            return lambda: flatten_k(a[1:], k2)
        return lambda: flatten_k(a[0], k1)
    return bounce(flatten_k(a, lambda x: x))

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


def LCSubstr_set(S, T):
    ''' Returns the set of longest common subsequences in 2 sequences.
    
    Lifted from: http://en.wikibooks.org/wiki/Algorithm_implementation/Strings/Longest_common_substring#Python

    Python strings are sequences so this also works for them.
    
    >>> LCSubstr_set('hello world', 'hello_world')
    set(['world', 'hello'])
    
    '''
    m = len(S); n = len(T)
    L = [[0] * (n+1) for i in xrange(m+1)]
    LCS = set()
    len_longest = 0
    for i in xrange(m):
        for j in xrange(n):
            if S[i] == T[j]:
                v = L[i][j] + 1
                L[i+1][j+1] = v
                if v > len_longest:
                    len_longest = v
                    LCS = set()
                if v == len_longest:
                    LCS.add(S[i-v+1:i+1])
    return LCS


def k_common_subsequence(sequences):
    ''' Returns the set of longest common subsequences in a collection of 
    sequences.

    See LCSubstr_set for longest common subsequence algorithm.

    a = (0,1,2)
    b = (0,2,4)
    c = (1,2,3,4,5,6)
    >>> k_common_subsequence((a,b,c))
    set([(1, 2)])
    
    >>> strings = [
    >>>     'hello',
    >>>     'fellow',
    >>>     'mellowing',
    >>>     'bellowing',
    >>> ]
    >>> k_common_subsequence(strings)
    set(['ellowing'])

    >>> def padded_range(n, padding_char='0'):
    >>>     return [str(padding_char[0]) * (len(str(n)) - len(str(i))) + str(i) for i in range(n)]
    >>> k_common_subsequence(padded_range(10))
    set(['0'])
    >>> k_common_subsequence(padded_range(100)) 
    set(['02', '03', '00', '01', '06', '07', '04', '05', '08', '09'])
    
    '''
    import itertools
    len_longest = 0
    list_longest = []
#        # wrong!
#    for p in itertools.combinations(sequences, 2):
#        s = LCSubstr_set(p[0], p[1])
#        for i in s:
#            if len(i) == len_longest:
#                list_longest.append(i)
#            elif len(i) > len_longest:
#                list_longest = [i]
#            if len(i) >= len_longest:
#                len_longest = len(i)
        
    # get set of all longest subsequences
#    s = set(flatten([list(LCSubstr_set(s, t)) for s, t in itertools.combinations(sequences, 2)]))
    s = set(itertools.chain.from_iterable([LCSubstr_set(s, t) for s, t in itertools.combinations(sequences, 2)]))
    
    # sort set, longest subsequences first
    s = sorted(s, key=len, reverse=True)
    
    # test, in sorted order, that subsequence is in all sequences, adding subsequence to new list
    return [sub for sub in s if present_in_all(sub, sequences)] 


def present_in_all(subsequence, sequences):
    
    return True #TODO
#    if instanceof(subsequence, str):

        


strings = [
    'hello',
    'fellow',
    'mellowing',
    'bellowing',
    'el',
]
print k_common_subsequence(strings)

def k_common_subsequence_present_in_all(sequences):
    s = list(k_common_subsequence(sequences))
    if len(s) == 0:
        # fail fast
        return s
    # if i is not a subsequence of every sequences in sequence then pop it and continue 
    o = []
    broken = False
    for i in s:
        for j in sequences:
            t = LCSubstr_set(i, j)
            if len(t) == 0:
                broken = True
                break
            for k in t:
                if len(k) < len(i):
                    broken = True
                    break
        if broken:
            broken = False
            continue
        else:
            o.append(i)
    return o

#sequences = [
#    'ello',
#    'hello',
#    'el',
#]
#print k_common_subsequence(sequences)
#print k_common_subsequence_present_in_all(sequences)

def padded_range(n, padding_char='0'):
    ''' Returns a list of padded integers in the interval 0 < n. 
    
    >>> padded_range(10)
    ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09']
    
    >>> padded_range(5)
    ['0', '1', '2', '3', '4']
    
    '''
    return [str(padding_char[0]) * (len(str(n)) - len(str(i))) + str(i) for i in range(n)]

