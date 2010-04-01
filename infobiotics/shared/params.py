from infobiotics.shared.api import \
    HasTraits, Instance, Str, Undefined, File, Directory, Bool, Property, \
    os, property_depends_on, Controller

class Params(HasTraits): 
    
    _parameters_name = Str(Undefined, desc='the name attribute of the parameter tag in the params XML file')
    _parameter_set_name = Str(Undefined, desc='the name attribute of the parameterSet tag in the params XML file')
    _params_file = File(exists=True)
    _cwd = Directory(os.getcwd(), exists=True)
    _dirty = Bool

    def __params_file_changed(self, _params_file):
        self._cwd = os.path.dirname(_params_file)
    
    def __init__(self, file=None, **traits):
        super(Params, self).__init__(**traits)
        if file is not None:
            self.load(file)

    def load(self, file=None): 
        if file is None:
            raise ValueError
        pass
    
    def save(self, file=None): 
        if file is None:
            raise ValueError
        pass

    #TODO change to a Property(List)? 
    #TODO change to more descriptive name, something to do with the fact that not all parameters will be returned
    def parameter_names(self):  
        raise NotImplementedError

    handler = Instance(Controller)
    
    def _handler_default(self):
        raise NotImplementedError
    
    def configure(self, **args):
        self.handler.configure_traits(kind='livemodal', **args)

    def edit(self, **args):
        self.handler.edit_traits(kind='live', **args)
