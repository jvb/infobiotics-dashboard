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