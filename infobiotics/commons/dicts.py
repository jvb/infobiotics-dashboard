def key_from_value(dict, value):
    ''' Returns the key in a dictionary for a value or None if the value is not 
    found.
    
    Raises a ValueError if the value is not unique.
    
    def test_key_from_value():
        # test key_from_value unique values
        dict = {'zero':0,'one':1,'two':0}
        print key_from_value(dict, 1) 
        print key_from_value(dict, 0) # same as key_from_value(map, 2)
        
    '''
    # count value
    value_count = dict.values().count(value)
    if value_count == 0:
        # value not found returning None
        return None
    if value_count > 1:
        # value is not unique raising ValueError
        raise ValueError('Multiple keys with value %s:' % value, \
                         ', '.join([k for k in dict.keys() if dict[k] == value]))
    # search for key
    for k, v in dict.iteritems():
        if v == value:
            # found value returning key
            return k
