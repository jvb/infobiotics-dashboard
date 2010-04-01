'''
Deprecated: moved to params.py to avoid circular import.
'''

from infobiotics.shared.api import \
    Handler, Instance, \
    ParamsView, Item

from params import Params

class ParamsHandler(Handler):
    '''
    
    Extends Handler by adding 'parameters' to default UI context.
    
    '''
        
    # Traits ---
    
    parameters = Instance(Params) # enables ParamsHandler(parameters=McssParams(file='...'))

    def _parameters_default(self):
        raise NotImplemetedError('Subclasses should override this method or'\
                                 "declare 'parameters = McssParams()'")

    # Handler-specific ---
    
    def traits_context(self):
        '''
        
        Adapted from Controller: https://svn.enthought.com/enthought/browser/Traits/trunk/enthought/traits/ui/handler.py
        
        '''
        context = super(ExperimentHandler, self).traits_context()
        context.update({'parameters': self._parameters})
        return context
        
    
    # Action methods ---
    
    def load(self, info): 
        file=None
        pass
        info.parameters.load(file)
    
    def save(self, info):
        file=None
        pass
        info.parameters.save(file)


    # parameters traits methods ---

    def parameters_title_changed(self, info):
        info.ui.title = info.parameters.title

        
#    # Class attributes --- 
#    
#    traits_view = ParamsView(
#        Item('_cwd', label='Working directory', tooltip='Relative paths will be relative to this directory.'),
#    )
