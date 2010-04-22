from infobiotics.shared.api import (
    HasTraits, Instance, Str, Undefined, List, File, Directory, Bool, 
    Property, Controller, can_access, read, write, os, 
    ParamsXMLReader, set_trait_value_from_parameter_value, 
    parameter_value_from_trait_value, traits_repr, 
    logging, 
    chdir,
)

from xml import sax

logger = logging.getLogger(level=logging.DEBUG)

class Params(HasTraits): 

    _parameters_name = Str(Undefined, desc='the name attribute of the parameter tag in the params XML file')
    _parameter_set_name = Str(Undefined, desc='the name attribute of the parameterSet tag in the params XML file')
    
    _dirty = Bool(False)
    _unresetable = List(Str)

    _params_file = File(exists=True)

    def __params_file_changed(self, _params_file):
        self._dirty = False
        self._cwd = os.path.dirname(_params_file)
        
#    # external validation of '_cwd'
#    _cwd_invalid = Property(Bool, depends_on='_cwd') # relates to Item('_cwd', invalid='_cwd_invalid', ...) in working_directory_group of infobiotics.shared.api
#    def _get__cwd_invalid(self):
#        return True if not can_access(self._cwd) else False

    _cwd = Directory(exists=True, auto_set=True)
    
    def __cwd_default(self):
        #TODO try and load _cwd from preferences?
        _cwd = os.getcwd()
#        logger = logging.getLogger(level=logging.DEBUG)
        logger.debug('__cwd_default(%s) returning %s', self, _cwd)
        return _cwd
#
#    def __cwd_changed(self, old, new):
#        # try and change directory ---
#        old_new_tuple_or_false = chdir(new)
#        # update all file and directory parameters with relative paths ---
#        if old_new_tuple_or_false:
#            old, new = old_new_tuple_or_false
#            self._update_relative_paths(old, new) 
#
#    def _update_relative_paths(self, old, new):
#        for name in self.parameter_names():
#            type = self.trait(name).trait_type.__class__.__name__
#            if type in ('File', 'Directory'):
#                path = getattr(self, name)
#                if isrel(path):
#                    path = os.path.join(old, path)
#                setattr(self, name, os.path.relpath(path, new))


    def __init__(self, file=None, **traits):
        super(Params, self).__init__(**traits)
        self.on_trait_change(self.update_repr, self.parameter_names())
        if file is not None:
            self.load(file)

    def load(self, file=''):
        '''  
        
        Reads parameters file, 
        resets traits,
        sets traits to new parameters,
        
        Returns True if a params file was successfully loaded. 
        
        '''

        if self._dirty:
            logger.warn('loading %s when current parameters are dirty', file)
            #TODO prompt to save, with timeout/override for non-interactive_mode
            pass

        # open and parse params file with ParamsXMLReader
        # reporting errors or responding to success 
        with read(file, 'rb') as fh:
            parser = sax.make_parser()
            parameters_dictionary = {}
            handler = ParamsXMLReader(parameters_dictionary, self._parameter_set_name)
            parser.setContentHandler(handler)
            error = None
            try:
                # read parameters from file into dictionary
                parser.parse(fh)
            except sax._exceptions.SAXParseException: 
                error = "'%s' is not a well-formed XML file." % file
            # check for other errors
            if not hasattr(handler, 'parameter_set_name'):
                error = "'%s' is not a parameters file." % file
#            elif not handler.has_expected_parameter_set_name: # will also fail without changing anything, also good.
#                error = "Incorrect parameter set: '%s' when '%s' expected." % (handler.parameter_set_name, handler.expected_parameter_set_name)
            elif len(parameters_dictionary) == 0:
                error = "No parameters in file '%s'." % file
            if error is not None:
                logger.error(error)
#                auto_close_message(message=error) #TODO is this desirable when scripting?...might not happen, as with ProgressDialog
                return False

        # read parameters ok
        
        
        # reset traits so we don't carry over parameters that are missing from 
        # the file we are loading
        self._unresetable = self.reset(self.parameter_names())
        if len(self._unresetable) > 0:
            logger.warn("Some parameters were not reset: %s", self._unresetable)

        # change directory so that setting of File traits with relative paths works
        if not os.path.isabs(file):
            file = os.path.abspath(file)
        old = os.getcwd() # remember where we are now
        new = os.path.dirname(file)
        chdir(new)

        # set parameters from dictionary
        for k, v in parameters_dictionary.iteritems():
            set_trait_value_from_parameter_value(self, k, v)
            # must specify directory/directory_name in model_file = File() else: enthought.traits.trait_errors.TraitError: The 'model_file' trait of a McssParams instance must be an existing file name in '/home/jvb/phd/eclipse/infobiotics/dashboard/infobiotics/shared', but a value of 'module1.sbml' <type 'str'> was specified.

        # success!
        
        # remember params file
        self._params_file = file # update _params_file (and _cwd via __params_file_changed)
        
#        self._update_relative_paths(old, new) #TODO FileDialog.extras -> 'Move input files to new directory?' checkbox
        
        # go back to where we were (for scripts using relative paths)
        chdir(old)
        
        logger.debug("Loaded '%s'." % file)
        return True


    def save(self, file='', force=False):
        # handle whether or not to overwrite an existing file ---
        if can_access(file):
            if not force:
                if self._interactive is True:
                    #TODO prompt not to overwrite with a message box
                    pass
                else:
                    #TODO prompt not to overwrite, with a timeout in case of non-interactive mode
                    pass
#                    print "Are you sure you want to overwrite '%s' (Y/n)?" % file
##                    start_time = time()
##                    while(whatever):
##                        do_something
##                        if time() - smart_time > 5:
##                            return
#                    answer = sys.stdin.readline()
#                    if answer.lower().startswith('y'):
#                        pass

        # actually write the file ---
        try:
            with write(file) as fh:
                fh.write(self.params_file_string()) # important bit
        except IOError, e:
            # handle IOError ---
            logger.exception(e)
            if self._interactive:
                from infobiotics.shared.api import message
                message(e, title='Error')
            else:
                print e
            return False
            
        # success! ---
#        if os.path.isabs(file): #FIXME
#            chdir(os.path.dirname(file)) # change current directory to directory of params file
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
        return '%s(_params_file=%s)' % (self.__class__.__name__, os.path.basename(self._params_file))
        
    def __repr__(self):
        return traits_repr(self, self.parameter_names())

    repr = Str # The "offical" string representation (scripting interface) of this params experiment, updated when any trait changes.

    def _repr_default(self):
        return self.__repr__()

    # on_trait_change set in __init__
    def update_repr(self):
        self.repr = self.__repr__()

    
    # interactive methods ---
        
    _interactive = False

    handler = Instance(Controller)
    
    def _handler_default(self):
        '''
        e.g.
            from infobiotics.mcss.api import McssParamsHandler
            return McssParamsHandler(model=self)
        '''
        raise NotImplementedError
    
    def configure(self, **args):
        self._interactive = True
        self.handler.configure_traits(**args)
        
    def edit(self, **args):
        self._interactive = True
        self.handler.edit_traits(kind='live', **args)


if __name__ == '__main__':
    execfile('../mcss/mcss_params.py')
    