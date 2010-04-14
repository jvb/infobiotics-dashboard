from infobiotics.shared.api import \
    HasTraits, Instance, Str, Undefined, File, Directory, Bool, \
    os, Controller, List, can_read, logging, can_access

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

        if not os.path.isabs(file): file = os.path.abspath(file) 

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
        old_cwd = os.getcwd()
        os.chdir(dir) # change current directory to directory of params file
#        self._cwd = dir # used by expect.spawn(cwd=self._cwd)
        
        # set parameters from dictionary
#        print parameters_dictionary
        for k, v in parameters_dictionary.iteritems():
            self.set_trait_value_from_parameter_value(k, v)

#        print self.params_file_string()
                
        # success!
        self._params_file = file # keep file in trait
#        self._cwd = os.getcwd() # keep cwd in trait
        os.chdir(old_cwd) # now change back to previous cwd
        return True


    def set_trait_value_from_parameter_value(self, name, value):
        from api import trait_value_from_parameter_value
        setattr(self, name, trait_value_from_parameter_value(self, name, value))
#        # or set trait by assignment (requires less type-checking in trait_value_from_parameter_value)
#        try:
##            exec('self.experiment.%s=%s' % (name, value))
#            exec('self.experiment.trait_set(%s=%s)' % (name, value))
#            # Either method works but exec is necessary because we are 
#            # using value of 'name' to assign value to it in each case.
#            # The second form is consistent with __repr__ and reset in 
#            # ParamsExperiment.
#        except TraitError, e:
#            logger.debug('%s.%s=%s; %s' % (self.experiment, name, value, e))

    
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

    def __repr__(self): #TODO change eval's to 'getattr(self, trait_name)'
        ''' Returns the "official" string representation of an object.
        
        From http://docs.python.org/reference/datamodel.html:
            'Called by the repr() built-in function and by string conversions 
            (reverse quotes) to compute the "official" string representation 
            of an object. If at all possible, this should look like a valid 
            Python expression that could be used to recreate an object with the
            same value[s] (given an appropriate environment).'
        
        In other words a string that can be eval'd to completely recreate the 
        experiment object (i.e. what the user would have to script). Instances 
        that match the pattern below will be correctly represented.  
        
        class ExampleInstanceWithRepr(HasTraits):
            name = Str('Jon')
            def __repr__(self):
                return 'Test("name=%s")' % self.name
 
        '''
        repr = ''
        repr += self.__class__.__name__
        repr += '('
        parameter_names = self.parameter_names()
        for i, parameter_name in enumerate(parameter_names):
            if len(parameter_names) > 0:
                if i != 0:
                    repr += ', '
            # switch on trait type (uses __repr__() of value for Instance traits)
            trait_type_class_name = eval('self.trait("%s").trait_type.__class__.__name__' % parameter_name)
            if trait_type_class_name == 'TraitMap': # a mapped trait
#                repr += "%s='%s'" % (parameter_name, eval('self.%s' % parameter_name)) # displayed value
                repr += "%s_='%s'" % (parameter_name, eval('self.%s_' % parameter_name)) # shadow name/value
            elif trait_type_class_name in ('Unicode','Str', 'Enum', 'File', 'Directory'):
                repr += "%s='%s'" % (parameter_name, eval('self.%s' % parameter_name))
            elif trait_type_class_name == 'Instance': # see ExampleInstanceWithRepr below
                repr += "%s=%s" % (parameter_name, eval('self.%s.__repr__()' % parameter_name))
            else: # Bool, Int, Float, Long, ...
                repr += "%s=%s" % (parameter_name, eval('self.%s' % parameter_name))
        repr += ')'
        return repr        

    repr = Str # The "offical" string representation (scripting interface) of this params experiment, updated when any trait changes.

    def _repr_default(self):
        return self.__repr__()

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
    print parameters
