'''multiset class that augments Counter with cardinality and multiplicity. 

Also overrides __str__ for alternative representation and __len__ to add
illustrative doctest.

Requires counter.Counter from accompanying module if Python < 2.7

'''

try:
    from collections import Counter
    # Python >= 2.7
except ImportError:
    # Python < 2.7
#    from counter import Counter  # Python >= 2.5 
    from counter import Counter2 # Python >= 2.6

class multiset(Counter):
    def __str__(self):
        '''Returns the members of the multiset expanded, sorted and concatenated
        with ' + '.
        
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
        return Counter.__len__(self)

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


if __name__ == '__main__':
    import doctest
    print doctest.testmod()
