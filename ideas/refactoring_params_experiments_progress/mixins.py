import enthought.traits.has_traits
enthought.traits.has_traits.CHECK_INTERFACES = 2
from enthought.traits.api import Interface, HasTraits, implements

class IParams(Interface):
    def load(self, file=None):
        ''''''
    
#class Params(HasTraits): # prints 'Params.load'
#    implements(IParams)
#
#    def load(self, file=None):
#        print 'Params.load'    
    
class Load(object): # Mixin
    def load(self, file=None):
        print 'Load.load'    
    
#class Params(HasTraits, Load): # prints 'Params.load'
#    implements(IParams)
#
#    def load(self, file=None):
#        print 'Params.load'    
#    
#class Params(Load, HasTraits): # prints 'Params.load'
#    implements(IParams)
#
#    def load(self, file=None):
#        print 'Params.load'    

class Params(Load, HasTraits): # prints 'Load.load'
    implements(IParams)

#class Params(HasTraits, Load): # fails
#    implements(IParams)

class IExperiment(IParams):
    def perform(self):
        ''''''
    
#class Experiment(Params): # prints Experiment.load, Experiment.perform
#    implements(IExperiment)
#    
#    def load(self):
#        print 'Experiment.load'
#
#    def perform(self):
#        print 'Experiment.perform'

class Perform(object):
    
    def load(self):
        print 'Perform.load'
        
    def perform(self):
        print 'Perform.perform'
        
class Experiment(Params, Perform): # prints Load.load, Perform.perform
    pass

class Experiment(Perform, Params): # prints Perform.load, Perform.perform
    pass


if __name__ == '__main__':
#    Params().load()
    Experiment().load()
    Experiment().perform()
    