import re

def is_valid(name):
    ''' See http://homepage.mac.com/s_lott/books/python/html/p04/p04c04_re.html '''
    if not re.match('[_A-Za-z][_A-Za-z1-9]*', name):
        raise ValueError("name should be a valid Python identifier, i.e. a string that starts with a letter or _, and containing any number of letters, digits or _'s. Got '%s' " % name)

def find_names(obj):
    ''' http://pythonic.pocoo.org/2009/5/30/finding-objects-names 
    
    foo = object()
    def demo():
        bar = foo
        print find_names(bar)
    demo()

    '''
    import gc, sys
    frame = sys._getframe()
    for frame in iter(lambda: frame.f_back, None):
        frame.f_locals
    result = []
    for referrer in gc.get_referrers(obj):
        if isinstance(referrer, dict):
            for k, v in referrer.iteritems():
                if v is obj:
                    result.append(k)
    return result


