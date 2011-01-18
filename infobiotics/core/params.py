from __future__ import with_statement # from __future__ imports must come first
import infobiotics # set up TraitsUI backend before traits imports
from infobiotics.core.params_preferences import ParamsPreferencesHelper, ParamsPreferencesPage, EXECUTABLE_TRAIT, DIRECTORY_TRAIT
from enthought.traits.api import (
    HasTraits, Str, Undefined, Bool, List, TraitError, Instance, Property,
#    on_trait_change
)
from enthought.traits.ui.api import Controller
from infobiotics.core.traits.params_relative_file import ParamsRelativeFile
from infobiotics.commons.api import key_from_value, can_access, read, write, logging, can_execute
from infobiotics.commons.traits.api import RelativeFile, RelativeDirectory
import os, sys
from xml import sax
from infobiotics.thirdparty.which import which, WhichError

logger = logging.getLogger(level=logging.ERROR)

import infobiotics.preferences # calls set_default_preferences, do not remove

class Params(HasTraits): 

    _parameters_name = Str(Undefined, desc='the name attribute of the parameter tag in the params XML file')
    _parameter_set_name = Str(Undefined, desc='the name attribute of the parameterSet tag in the params XML file')

    _params_file = ParamsRelativeFile(absolute=True, exists=True, readable=True, writable=True)
    
    executable_name = Str

    _preferences_path = Property(depends_on='executable_name')

    def _get__preferences_path(self):
        return self.executable_name

    preferences_helper = Instance(ParamsPreferencesHelper)
    def _preferences_helper_default(self):
        raise NotImplementedError('Params subclasses must provide a _get_preferences_helper methods that returns an instance of (a subclass of) ParamsPreferencesHelper.')

    preferences = List(Str, ['executable', 'directory'], desc='a list of trait names to bind to preferences')
    
    executable = EXECUTABLE_TRAIT

    def _executable_default(self):
        try:
            executable = self.preferences_helper.executable # load saved or default
#            print 'got here'
            return executable
        except TraitError, e:
            print e
            try:
                alternative = which(self.executable_name) # search path for alternative
#                print 'got here 2'
                return alternative
            except WhichError, e:
                print e
                return Undefined # fail ignomiously

    directory = DIRECTORY_TRAIT # infinite recursion if ParamsRelativeDirectory because directory='directory'
    
    def __init__(self, file=None, **traits):
        self.bind_preferences()
        super(Params, self).__init__(**traits)
        self.on_trait_change(self.update_repr, self.parameter_names())
        if file is not None:
            self.load(file)

    def bind_preferences(self):
        ''' Changes to preferences object will update bound trait value and 
        vice versa. Uses get_default_preferences and therefore 
        set_default_preferences must have been called with the correct preferences object.
        '''
        from enthought.preferences.api import bind_preference #, get_default_preferences
#	    preferences = get_default_preferences()
        from infobiotics.preferences import preferences
#        print preferences
        # must assign bound_preferences otherwise bindings will be lost when this method returns 
#        self.bound_preferences = [bind_preference(self, preference, '.'.join([self._preferences_path, preference]), infobiotics.preferences.preferences) for preference in self.preferences]
        self.bound_preferences = []
        for preference in self.preferences:
            preferences_path = '.'.join([self._preferences_path, preference])
            if preference in ('directory'):#, 'executable'):
                path = infobiotics.preferences.preferences.get(preferences_path, '')
                if not os.path.exists(path): #TODO what about None?
#                    sys.stderr.write(path)
#                    sys.stderr.write('\n')
                    infobiotics.preferences.preferences.set(preferences_path, '')
                    infobiotics.preferences.preferences.flush()
            # this fails if preference trait is DelegatesTo
            bound_preference = bind_preference(self, preference, preferences_path, infobiotics.preferences.preferences)
            self.bound_preferences.append(bound_preference)
        
    def save_preferences(self):
        ''' Called from self.handler.close() '''
        from enthought.preferences.api import get_default_preferences
        get_default_preferences().save()

        
    _unresetable = List(Str)
        
    def load(self, file=''):
        ''' Reads parameters file, 
        resets traits,
        sets traits to new parameters,
        
        Returns True if a params file was successfully loaded. 
        
        '''
        if getattr(self, '__dirty', False):
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
            logger.warn("Some parameters were not reset: %s", ', '.join(self._unresetable))

        # change directory so that setting of File traits with relative paths works
        if not os.path.isabs(file):
            file = os.path.abspath(file)

        # change directory here so that relative paths don't trigger TraitError
        self.directory = os.path.dirname(file)

        # set parameters from dictionary, passing if values are not suitable
        for name, value in parameters_dictionary.iteritems():
            try:
                set_trait_value_from_parameter_value(self, name, value)
            except TraitError:
                pass
            
        # success!
#        logger.debug("Loaded '%s'." % file)
        self._params_file = file
        self._dirty = False #TODO use dirty for prompting to save on perform
        return True

    from enthought.traits.api import Event
    _dirty = Event
    def __dirty_changed(self, dirty):
        print dirty
        self.__dirty = dirty
    
    def _anytrait_changed(self, name, old, new):
#        print name, old, new
        if name in self.parameter_names():
            print name, old, new
            self._dirty = True

    def save(self, file='', force=False, copy=False, update_object=True):
        # handle whether or not to overwrite an existing file ---
        if can_access(file) and not force:
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

        # handle problem of invalidating relative paths when saving to a new directory
        old_params_file_dir = os.path.dirname(self._params_file)
        new_params_file_dir = os.path.dirname(file) 
        if old_params_file_dir != new_params_file_dir:
            for name in self.parameter_names():
                trait = self.base_trait(name)
                if not trait.trait_type.__class__.__name__ == 'File':
                    continue
                handler = trait.handler
                if handler.exists:
                    value = getattr(self, name)
                    if not os.path.isabs(value): 
                        if handler.directory != old_params_file_dir:
                            continue #FIXME what if old_params_file_dir == '' because the params/experiment hasn't been saved yet?
                        if copy: # copy input files whose parameter values are paths relative to _params_file to new _params_file directory
                            src = os.path.normpath(os.path.join(old_params_file_dir, value))
                            dst = os.path.normpath(os.path.join(new_params_file_dir, value))
                            print src
                            print dst
                            if not force:
                                pass
                                #TODO prompt to overwrite existing file
                                result = True #FIXME
                                if not result:
                                    continue
                            import shutil
                            shutil.copy2(src, dst) 
                            print 'copied', src, 'to', dst
                        else: # change relative paths to point to old locations
                            self.directory = new_params_file_dir
                            setattr(self, name, os.path.relpath(os.path.normpath(os.path.join(old_params_file_dir, value)), new_params_file_dir))

        # actually write the file ---
        try:
            with write(file) as fh:
                fh.write(self.params_file_string()) # important bit
        except IOError, e:
            # handle IOError ---
            logger.exception(e)
            if self._interactive:
                from enthought.traits.ui.message import auto_close_message, error, message
                message(str(e), title='Error')
            else:
                print e
            return False
            
        # success!
#        logger.debug("Saved '%s'." % file)
        self.directory = os.path.dirname(file)
        if update_object:
            self._params_file = file
            self._dirty = False #TODO use dirty for prompting to save on perform    
        return True


    def reset(self, traits=None):
        ''' Resets some or all of an object's trait attributes to their default
        values. Identical to HasTraits.reset_traits(). 
        
        Used when loading params files because they may not contain all   
        parameters and we don't want the previous values to remain.
        
        Returns a list of attributes that the method was unable to reset, 
        (all saved in _unresetable) 
        which is empty if all the attributes were successfully reset. 
        
        '''
        return self.reset_traits(traits)

    def reset_parameters(self, parameter_names=None):
        if parameter_names == None:
            parameter_names = self.parameter_names()
        return self.reset(parameter_names)

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

#    def __str__(self):
##        return self.params_file_string()
#        return '%s(_params_file=%s)' % (self.__class__.__name__, os.path.basename(self._params_file))
#        
#    def __repr__(self):
#        return traits_repr(self, self.parameter_names())

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
        ui = self.handler.edit_traits(**args)



    
from xml.sax import ContentHandler

class ParamsXMLReader(ContentHandler):
    ''' Parses params file and inserts parameters into dictionary passed to 
    __init__.
    
    Returns early if an unexpected parameter_set_name is encountered. 
    
    '''

    def __init__(self, parameters_dictionary, parameter_set_name):
        self.parameters_dictionary = parameters_dictionary

#        self.expected_parameters_name = parameters_name
#        self.has_expected_parameters_name = False

        self.expected_parameter_set_name = parameter_set_name
        self.has_expected_parameter_set_name = False
        
#        super(ParamsXMLReader, self).__init__() # doesn't work! Use below instead.
        ContentHandler.__init__(self)

    def startElement(self, name, attrs):
#        if name.lower() == 'parameters':
#            if attrs['name'] == self.expected_parameters_name:
#                self.has_expected_parameters_name = True
#            else:
#                return

        if name.lower() == 'parameterset':
            self.parameter_set_name = attrs['name'] # we will test for this using hasattr  
            if self.parameter_set_name.lower() == self.expected_parameter_set_name.lower():
                self.has_expected_parameter_set_name = True
            else:
                return
            
        if name.lower() == 'parameter':
            # <parameter name="..." value="..."/>
            name = attrs['name'] # overwriting name here!
            value = attrs['value'] # all unicode, need to convert to types
            self.parameters_dictionary[name] = value


def set_trait_value_from_parameter_value(self, name, value):
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

def trait_value_from_parameter_value(self, name, value): # change name to 'trait_value_from_param_value'?
    ''' Return parameter trait value from a parameter value string. '''
#    assert name in self.parameter_names()
    trait = self.trait(name)
    if trait is None:
        return
    type = trait.trait_type.__class__.__name__
#    if type == 'DelegatesTo':
#        _delegate = trait._delegate
#        setattr(eval('self.%s' % (_delegate)), name, value)
#        #FIXME should go in 'set_trait_value_from_parameter_value'
#        return value
    if type == 'Bool': # convert from lowercase truth values
#        return True if value == 'true' else False
        if value in ('true', 'True', '1'):
            return True
        elif value in ('false', 'False', '0'):
            return False
        else:
            print "'%s' not specified correctly. '%s' should be in ('true', 'True', '1', 'false', 'False', '0'). Assuming False." % (name, value)
            return False
    elif type in ('Int', 'IntGreaterThanZero'):
        return int(value) 
    elif type in ('Long', 'LongGreaterThanZero'):
        return long(value)
    elif type in ('Float', 'FloatGreaterThanZero'):
        return float(value) 
#    elif type == 'Complex':
#        return complex(value)
    elif type == 'Str':
        return str(value) 
    elif type == 'Unicode':
        return unicode(value) 
    elif type == 'TraitMap': # set non-shadow trait with key from shadow_value in map
        try:
            dict = trait.handler.map
            key = key_from_value(dict, value)
        except ValueError, e:
            pass
        if key is None:
            pass
        else:
            return key
    elif type == 'Range':
        if isinstance(trait.default, int):
            return int(value)
        elif isinstance(trait.default, float):
            return float(value)   
        elif isinstance(trait.default, long):
            return long(value)
    elif type in ('Enum', 'File', 'Directory'):
        return str(value)    
    else:
        logger.warn('unswitched type in trait_value_from_parameter_value: type=%s, name=%s, value=%s' % (type, name, value))
        return value

#TODO could replace name with trait.metadata.parameter_name and return (new_name, value)
def parameter_value_from_trait_value(self, name):
    ''' Return parameter value string from a ParamsExperiment parameter trait. ''' 
    assert name in self.parameter_names()
    trait = self.trait(name)
    value = self.trait_get(name)[name] # trait_get returns dict
    type = trait.trait_type.__class__.__name__
    if type == 'Bool': # convert to lowercase truth values
        value = 'true' if value is True else 'false'
    elif type == 'TraitMap': # use shadow_value
        shadow_name = '%s_' % name
        shadow_value = self.trait_get(shadow_name)[shadow_name]
        # look for a trait with the name in shadow_value and if found return its value
        possible_shadow_trait_dictionary = self.trait_get(shadow_value)
        if len(possible_shadow_trait_dictionary) > 0:
            shadow_value = possible_shadow_trait_dictionary[shadow_value]
        else:
            value = shadow_value
#    elif type == 'File': value = os.path.basename(value) #FIXME
#    print name, value
    return str(value)
    
def traits_repr(self, *names):
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
         age = Int(28)
         def __repr__(self):
             return traits_repr(self, [name, age])
    
    '''
    from infobiotics.commons.sequences import flatten
    names = flatten(names)
    repr = self.__class__.__name__ + '('
    for i, name in enumerate(names):
        if len(names) > 0:
            if i != 0:
                repr += ', '
        # switch on trait type 
        type = self.trait(name).trait_type.__class__.__name__
        if type == 'Instance':
            repr += "%s=%s" % (name, getattr(self, '%s' % name).__repr__())
        elif type == 'TraitMap': # Trait({'2+2':5})
            repr += "%s_='%s'" % (name, getattr(self, '%s_' % name)) # use shadow name/value
        elif type in (
            'Unicode', 'Str', 'Enum', 'File', 'Directory',
            'RelativeFile', 'RelativeDirectory',
            'ParamsRelativeFile', 'ParamsRelativeDirectory',
        ):
            repr += "%s='%s'" % (name, getattr(self, '%s' % name))
        else: # Bool, Int, Float, Long, ...
            repr += "%s=%s" % (name, getattr(self, '%s' % name))
    repr += ')'
    return repr      


if __name__ == '__main__':
    execfile('../mcss/mcss_params.py')
    
