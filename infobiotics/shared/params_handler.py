'''
Deprecated: moved to params.py to avoid circular import.
'''

from infobiotics.shared.api import \
    Handler, Instance, Property, property_depends_on, Str, \
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
    title = Property(Str)

    @property_depends_on('parameters._params_file')
    def _get_title(self):
        path = self.parameters._params_file
        if len(path) > 0:
            dirname, basename = os.path.split(path)
            if dirname == '':
                return basename
            else:
                return '%s (%s)' % (basename, dirname)
        else:
            return self.parameters._parameters_name

    def _title_changed(self, title):
        print title
        info.ui.title = self.title


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


        
#    # Class attributes --- 
#    
#    traits_view = ParamsView(
#        Item('_cwd', label='Working directory', tooltip='Relative paths will be relative to this directory.'),
#    )
