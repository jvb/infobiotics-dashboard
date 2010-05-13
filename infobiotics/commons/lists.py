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
