# http://www.artima.com/weblogs/viewpost.jsp?thread=240808

from infobiotics.commons.sequences import flatten

def flattened(f):
    ''' Decorator that flattens the returned sequence. '''
    def decorated(*args, **kwargs):
        return flatten(f(*args, **kwargs))
    decorated.__name__ = f.__name__ # otherwise returned .__name__ = 'new_f'
    decorated.__doc__ = f.__doc__ # ditto for docstring
    return decorated

module = flattened # alias
