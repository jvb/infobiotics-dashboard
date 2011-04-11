from infobiotics.commons.counter import Counter

class multiset(Counter):
    def __str__(self):
        '''Returns 'a + b + b' for {'a':1,'b':2}.'''
        return ' + '.join([k for k, v in sorted(self.items()) for _ in range(v)])

    def __len__(self):
        '''
        
        >>> m = multiset({'a':1, 'b':2})
        >>> len(m)
        2
        
        '''
        return super(multiset, self).__len__()

    def cardinality(self):
        ''' The total number of elements in a multiset, including repeated memberships, is the cardinality of the multiset. 
        
        >>> m = multiset({'a':1, 'b':2})
        >>> m.cardinality()
        3
        
        '''
        return len(list(self.elements()))

    def multiplicity(self, key):
        '''
        
        >>> m = multiset({'a':1, 'b':2})
        >>> m.multiplicity('a')
        1
        >>> m.multiplicity('b')
        2
        >>> m.multiplicity('c')
        0
        
        '''
        return self[key]


#class frozenmultiset(multiset):
#    try:
#        frozenset
#    except NameError:
#        from sets import ImmutableSet as frozenset
#    __slots__ = ('_hash',)
#    def __hash__(self):
#        rval = getattr(self, '_hash', None)
#        if rval is None:
#            rval = self._hash = hash(frozenset(self.iteritems()))
#        return rval

if __name__ == '__main__':
    import doctest
    print doctest.testmod()


    m = multiset({'a':1, 'b':2})
    print m.__str__()
    print m.__repr__()

    n = multiset(m + m)
    print 'cardinality =', n.cardinality(), 'len =', len(n)
