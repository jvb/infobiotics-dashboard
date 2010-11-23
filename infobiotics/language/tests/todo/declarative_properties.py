from enthought.traits.api import Int, Property
####class Test(HasTraits):
####    _i = Int
####    def _set_i(self, value):
####        self._i = value
####    def _get_i(self):
####        return self._i * 10
####    def __init__(self, **traits):
####        i = traits.pop('i', None)
####        if i is None:
####            i = getattr(self.__class__, 'i', self._i)
####        super(Test, self).__init__(**traits)
####        self.add_trait('i', Property(self._get_i, self._set_i, trait=Int))
####        self.i = i# if i is not None else 0
###class Test(HasTraits):
####    _i = Int
###    def _set_i(self, value):
###        self._i = value
###    def _get_i(self):
###        return self._i * 10
###    def __init__(self, **traits):
###        i = traits.pop('i', None)
###        if i is None:
###            i = getattr(self.__class__, 'i', 0)#self._i)
####        super(Test, self).__init__(**traits) # why doesn't this matter?
###        self.add_trait('i', Property(self._get_i, self._set_i, trait=Int))
###        self.i = i# if i is not None else 0
##class Test(HasTraits):
##    def _get_i(self):
##        return self._i * 10
##    def _set_i(self, value):
##        self._i = value
##    def __init__(self, **traits):
##        i = traits.pop('i', None)
##        self.add_trait('i', Property(self._get_i, self._set_i, trait=Int))
##        self.i = i if i is not None else getattr(self.__class__, 'i', 0)
#class Test(HasTraits):
#    def _get_i(self):
#        return self._i * 10
#    def _set_i(self, value):
#        self._i = value
#    def __init__(self, **traits):
#        self.add_trait('i', Property(self._get_i, self._set_i, trait=Int))
#        self.i = traits.pop('i', getattr(self, 'i', getattr(self.__class__, 'i', 0)))
class Test(HasTraits):
#    _i = Int
    i = Property(Int)
    def _get_i(self):
        return self._i * 10
    def _set_i(self, value):
        self._i = value
    def __init__(self, **traits):
        self.add_trait('i', Property(self._get_i, self._set_i, trait=Int))
        self.i = traits.pop('i', getattr(self, 'i', getattr(self.__class__, 'i', 0)))

# i not defined in class
assert Test().i == 0

# i defined in class
class TestSubclass(Test):
    i = 1
assert TestSubclass().i == 10

# i not defined and set in init 
assert Test(i=2).i == 20

# i defined and set in init
assert TestSubclass(i=2).i == 20

# i defined incorrectly
class TestSubclass2(Test):
    i = 'a'
try:
    test = False
    TestSubclass2()
    test = True
except:
    assert test == False

# i set correctly
t = Test()
t.i = 10
assert t.i == 100

#t.i = 1.1
t.i = 1.1
print t.i
