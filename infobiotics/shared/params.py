from infobiotics.shared.api import \
    HasTraits, Instance, Str, Undefined, File, Directory, Bool, Property, \
    os, property_depends_on

class Params(HasTraits): 
    
    _parameters_name = Str(Undefined, desc='the name attribute of the parameter tag in the params XML file')
    _parameter_set_name = Str(Undefined, desc='the name attribute of the parameterSet tag in the params XML file')
    _params_file = File(exists=True)
    _cwd = Directory(os.getcwd(), exists=True)
    _dirty = Bool

    title = Property(Str) #TODO change to _title?

    def __params_file_changed(self, _params_file):
        self._cwd = os.path.dirname(_params_file)
    
    @property_depends_on('_params_file')
    def _get_title(self):
        if len(self._params_file) > 0:
            path = self._params_file
            dirname, basename = os.path.split(path)
            if dirname == '':
                return basename
            else:
                return '%s (%s)' % (basename, dirname)
        else:
            return self._parameters_name
    
    
    def __init__(self, file=None, **traits):
        super(Params, self).__init__(**traits)
        if file is not None:
            self.load(file)

    #TODO change to a Property(List)? 
    #TODO change to more descriptive name, something to do with the fact that not all parameters will be returned
    def parameter_names(self):  
        raise NotImplementedError
    
    def load(self, file=None): 
        if file is None:
            raise ValueError
        pass
    
    def save(self, file=None): 
        if file is None:
            raise ValueError
        pass

    def configure(self, **args):
        raise NotImplementedError('''
        #Subclasses of ParamsHandler should implement something like:
    def configure(self, **args):
        from infobiotics.<program>.api import <program>[Params/Experiment]Handler
        handler = <program>Handler(model=self)
        return handler.configure_traits(kind='modal', **args)''')
    

    def edit(self, **args):
        raise NotImplementedError('''
        #Subclasses of ParamsHandler should implement something like:
    def edit(self, **args):
        from infobiotics.<program>.api import <program>[Params/Experiment]Handler
        handler = <program>Handler(model=self)
        return handler.edit_traits(
#            kind='live', 
            **args
        )''')
