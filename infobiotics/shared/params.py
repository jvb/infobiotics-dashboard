from infobiotics.shared.api import \
    HasTraits, Instance, Str, Undefined, File, Directory, Bool, \
    os, Controller, List, can_read, logging, can_access, \
    set_trait_value_from_parameter_value

logger = logging.get_logger('params')


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

#    def load(self, file=None): 
#        if file is None:
#            raise ValueError
#        pass

    _unresetable = List(Str)

    def load(self, file=''):
        '''  
        
        Tries to load file, if successful resets traits and *then* parses file. 
        
        Returns True if a params file was successfully loaded. 
        
        '''

        if self._dirty: 
            print 'loading %s when current parameters are dirty' % file
            #TODO prompt to save, with timeout
            pass

#        if not os.path.isabs(file): file = os.path.abspath(file) 

#        if not os.path.exists(file): raise IOError("'%s' does not exist." % file)
        assert can_access(file)
        
        if not can_read(file): raise IOError("'%s' cannot be read." % file)    
            
        # open and parse params file with ParamsXMLReader
        # reporting errors or responding to success 
        with open(file, 'rb') as fh:
            from xml import sax
            from api import ParamsXMLReader
            parser = sax.make_parser()
            parameters_dictionary = {}
            handler = ParamsXMLReader(parameters_dictionary, self._parameter_set_name)
            parser.setContentHandler(handler)
            error = None
            try:
                # read parameters from file into dictionary
                parser.parse(fh)
            except sax._exceptions.SAXParseException, e: 
                error = 'Not a well-formed XML file.' # can fail *after* some parameters have been changed!
            # check for other errors
            if not hasattr(handler, 'parameter_set_name'): # will fail without changing anything, good.
                error = 'Not a parameters file.'
#            elif not handler.has_expected_parameter_set_name: # will also fail without changing anything, also good.
#                error = 'Incorrect parameter set: %s when %s expected' % (handler.parameter_set_name, handler.expected_parameter_set_name)
            elif len(parameters_dictionary) == 0:
                error = 'No parameters in file'
            if error is not None:
                # report error
                logger.error(error)
#                auto_close_message(message=error) #TODO is this desirable when scripting?...might not happen, as with ProgressDialog
                return False

        # read parameters ok
        self._unresetable = self.reset()
        # reset traits so we don't carry over parameters that are missing from 
        # the file we are loading
        #TODO reset traits after file successfully parsed, *then* apply traits?

        # change directory so that setting of File traits with relative paths works
        if not os.path.isabs(file):
            file = os.path.abspath(file)
        dir = os.path.dirname(file)
        old_cwd = os.getcwd() # remember where we are now
        os.chdir(dir)
        
        # set parameters from dictionary
        for k, v in parameters_dictionary.iteritems():
            set_trait_value_from_parameter_value(self, k, v)

        # success!
        self._params_file = file # update _params_file
        self._cwd = os.getcwd() # update _cwd
        os.chdir(old_cwd) # go back to where we were (for scripts using relative paths)
        return True


    def save(self, file=''):
        #TODO prompt not to overwrite, with a timeout in case of non-interactive mode
        with open(file, 'w') as fh:
            print fh
            logger.debug(fh)
            try:
                fh.write(self.params_file_string()) # important bit, see method below
            except IOError, e:
                logger.error('save(), %s' % e) #TODO message box
                return False
        # success!
#        if os.path.isabs(file): #FIXME
#            os.chdir(os.path.dirname(file)) # change current directory to directory of params file
#        self._cwd = os.getcwd()
        self._params_file = file
        self._dirty = False
        return True

    def reset(self, traits=None):
        ''' Resets some or all of an object's trait attributes to their default
        values. Identical to HasTraits.reset_traits(). 
        
        Used when loading params files because they may not contain all   
        parameters and we don't want the previous values to remain.
        
        Returns a list of attributes that the method was unable to reset, which
        is empty if all the attributes were successfully reset. 
        
        '''
        return self.reset_traits(traits)

    def reset_parameters(self, parameter_names=None):
        if parameter_names == None:
            parameter_names = self.parameter_names()
        return self.reset(parameter_names)

    #TODO make this a ListStr trait and use _parameter_names_default instead of parameter_names?
    #TODO change to a Property(List)? 
    #TODO change to more descriptive name, something to do with the fact that not all parameters will be returned
    def parameter_names(self):  
        raise NotImplementedError(
            "Subclasses of Params must reimplement 'parameter_names'"
        )
        
    def params_file_string(self):
        '''Returns desired contents of a params file as a string. '''
        s = '''<?xml version="1.0" encoding="utf-8" ?>
<parameters name="%s" xmlns="http://www.cpib.ac.uk/~jpt"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.cpib.ac.uk/~jpt parameter.xsd">

    <!-- parameter definitions -->
    <parameterSet name="%s">
''' % (self._parameters_name, self._parameter_set_name)
        from api import parameter_value_from_trait_value
        for name in self.parameter_names():
            value = parameter_value_from_trait_value(self, name)
            parameter = '        <parameter name="%s" value="%s"/>\n' % (name, value)
            s += parameter
        s += '''    </parameterSet>
</parameters>
'''     
        return s

    def __str__(self):
#        return self.params_file_string()
        return super(HasTraits, self).__str__()

    repr = Str # The "offical" string representation (scripting interface) of this params experiment, updated when any trait changes.

    def _repr_default(self):
        return self.__repr__()

    def __repr__(self):
        from infobiotics.shared.api import traits_repr
        return traits_repr(self, self.parameter_names())

    def _anytrait_changed(self, name, old, new): # move to handler
        ''' Updates 'repr' trait with value of '__repr__()', for display.
        
        This method is called when *any* trait's value changes.
        
        What about '_changed()', or @on_trait_change('*')?
        
        '''
        self.repr = self.__repr__()


    handler = Instance(Controller)
    
    def _handler_default(self):
        raise NotImplementedError
    
    def configure(self, **args):
        self.handler.configure_traits(kind='livemodal', **args)
        
    def edit(self, **args):
        self.handler.edit_traits(kind='live', **args)


if __name__ == '__main__':
    from infobiotics.mcss.api import McssParams
    parameters = McssParams()
#    parameters.configure_traits()
#    parameters.configure()
    os.chdir('../../tests/mcss/models')
    print parameters.load('module1.params')
    print parameters.load('reactions1.params')
    print parameters
