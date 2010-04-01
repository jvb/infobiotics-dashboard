import enthought.traits.has_traits
enthought.traits.has_traits.CHECK_INTERFACES = 2
from enthought.traits.api import Interface, HasTraits, implements

# Interfaces ---

class ILoad(Interface):
    def load(self, file=None):
        ''''''

class ISave(Interface):
    def save(self, file=None):
        ''''''

class IPerform(Interface):
    def perform(self):
        ''''''

#class IParams(ILoad, ISave):
#    pass
#
#class IExperiment(IParams, IPerform):
#    pass

# Mixins ---
    
class MLoad(object):#LoadParametersMixin
    implements(ILoad)
    def load(self, file=None):
        print 'MLoad.load'
        
class MSave(object):#SaveParametersMixin
    implements(ISave)
    def save(self, file=None):
        print 'MSave.save'
        
class MPerform(object):#PerformExperimentMixin
    implements(IPerform)
    def perform(self):
        print 'MPerform.perform'
    def __init__(self):
        assert isinstance(self, Params), 'Missing required base class.'
            
class Params(MLoad, MSave, HasTraits):
#    implements(ISave)
#    pass
    def load(self, file=None):
        print 'Params.load'

class Experiment(Params, MPerform):
#    implements(IExperiment)
    pass


if __name__ == '__main__':
    Experiment().load()
    Experiment().save()
    Experiment().perform()
    