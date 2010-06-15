# http://www.artima.com/weblogs/viewpost.jsp?thread=240808

#class entryExit(object):
#
#    def __init__(self, f):
#        self.f = f
#
#    def __call__(self):
#        print "Entering", self.f.__name__
#        self.f()
#        print "Exited", self.f.__name__

def entryExit(f):
    def new_f():
        print "Entering", f.__name__
        f()
        print "Exited", f.__name__
    new_f.__name__ = f.__name__ # otherwise returned .__name__ = 'new_f'
    return new_f

@entryExit
def func1():
    print "inside func1()"

@entryExit
def func2():
    print "inside func2()"

func1()
func2()


# http://www.artima.com/weblogs/viewpost.jsp?thread=240845

#def decoratorFunctionWithArguments(arg1, arg2, arg3):
#    def wrap(f):
#        print "Inside wrap()"
#        def wrapped_f(*args):
#            print "Inside wrapped_f()"
#            print "Decorator arguments:", arg1, arg2, arg3
#            f(*args)
#            print "After f(*args)"
#        return wrapped_f
#    return wrap
#
#@decoratorFunctionWithArguments("hello", "world", 42)
#def sayHello(a1, a2, a3, a4):
#    print 'sayHello arguments:', a1, a2, a3, a4


from infobiotics.commons.sequences import flatten

def module(m):
    ''' module decorator than flattens the returned rules '''
    def decorated_module(*args, **kwargs):
        return flatten(m(*args, **kwargs))
    decorated_module.__name__ = m.__name__ # otherwise returned .__name__ = 'new_f'
    decorated_module.__doc__ = m.__doc__ # ditto for docstring
    return decorated_module
    