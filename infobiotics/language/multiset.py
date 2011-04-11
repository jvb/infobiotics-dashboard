try:
    Counter #@UndefinedVariable
except NameError:
    from infobiotics.commons.counter import Counter


class multiset(Counter):
    def __str__(self):
        '''Returns the members of the multiset, expanded and concatenate with 
        '+'.
        
        >>> m = multiset('abb')
        >>> print m
        a + b + b
        '''
        return ' + '.join([k for k, v in sorted(self.items()) for _ in range(v)])

    def __len__(self):
        '''Returns the total number of members, excluding repeated elements.
        
        >>> m = multiset('abb')
        >>> len(m)
        2
        '''
        return super(multiset, self).__len__()

    def cardinality(self):
        '''Returns the total number of elements in a multiset, including 
        repeated memberships. 
        
        >>> m = multiset({'a':1, 'b':2})
        >>> m.cardinality()
        3
        '''
        return len(list(self.elements()))

    def multiplicity(self, member):
        '''Returns the number of elements of 'member'. 
        
        >>> m = multiset('abb')
        >>> m.multiplicity('a')
        1
        >>> m.multiplicity('b')
        2
        >>> m.multiplicity('c')
        0
        '''
        return self[member]


class frozenmultiset(multiset):
    '''Hashable but mutable.'''
    try:
        frozenset
    except NameError:
        from sets import ImmutableSet as frozenset
    __slots__ = ('_hash',)
    def __hash__(self):
        memo = getattr(self, '_hash', None)
        if memo is None:
            memo = self._hash = hash(frozenset(self.iteritems()))
        return memo


if __name__ == '__main__':
    import doctest
    doctest.testmod()
