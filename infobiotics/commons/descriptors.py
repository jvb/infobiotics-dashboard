class classmethod(object):
    ''' Adapted from http://users.rcn.com/python/download/Descriptor.htm#ClassMethod '''
    def __init__(self, f):
        self.f = f
    def __get__(self, obj, klass=None):
        if klass is None:
            klass = type(obj)
        def newfunc(*args, **kwargs):
            return self.f(klass, *args, **kwargs)
        return newfunc

class mixedmethod(object):
    ''' Act like a class method when called on a class 
    or an instance method when called on an instance. '''
    def __init__(self, f):
        self.f = f
    def __get__(self, obj, klass=None):
        if obj is not None:
            klass = obj
        def newfunc(*args, **kwargs):
            return self.f(klass, *args, **kwargs)
        return newfunc
