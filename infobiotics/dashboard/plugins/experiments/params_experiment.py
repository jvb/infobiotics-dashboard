# This file is part of the Infobiotics Dashboard. See LICENSE for copyright.
# $Id: experiment.py 414 2010-01-26 16:07:05Z jvb $
# $HeadURL: https://psiren.cs.nott.ac.uk/repos/infobiotics/dashboard/trunk/infobiotics/dashboard/plugins/experiments/experiment.py $
# $Author: jvb $
# $Revision: 414 $
# $Date: 2010-01-26 16:07:05 +0000 (Tue, 26 Jan 2010) $

from __future__ import with_statement
from infobiotics.shared.traits_imports import *
import os

from enthought.traits.api import HasTraits, implements
from i_experiment import IExperiment
from experiment import Experiment
from i_params_experiment import IParamsExperiment

from enthought.preferences.api import Preferences

from enthought.pyface.constant import *
from xml import sax

from infobiotics.dashboard.plugins.experiments.params_experiment_handler import ParamsExperimentHandler

from infobiotics.dashboard.shared.unified_logging import unified_logging
logger = unified_logging.get_logger('params_experiment')

from xml.sax import ContentHandler

#from params_xml_reader import ParamsXMLReader
class ParamsXMLReader(ContentHandler):
    ''' Parses params file and inserts parameters into dictionary passed to 
    __init__.
    
    Returns early if an unexpected parameter_set_name is encountered. 
    
    '''
    def __init__(self, parameters_dictionary, parameter_set_name):
        self.parameters_dictionary = parameters_dictionary
        self.expected_parameter_set_name = parameter_set_name
#        self.has_expected_parameters_name = False
        self.has_expected_parameter_set_name = False
#        super(ParamsXMLReader, self).__init__() # doesn't work!
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
                    

class ParamsExperiment(Experiment):
    ''' Abstract base class of all Infobiotics Dashboard experiments.
    
    ParamsExperiments are performed by external programs with parameters from
    files with the extension '.params' (hence forth called 'params files'). 
    Params files are XML in nature with 'parameters', 'parameterSet' 
    and 'parameter' elements. Only one 'parameters' element is present and 
    its name attribute is supposed to correlate to the program that parsers the
    file. Generally only one 'parameterSet' element is present in each params 
    file and its name attribute is supposed to correlate to a type of 
    experiment that the program performs. For example in a PModelChecker 
    experiment <parameters name="pmodelchecker"> and 
    <parameterSet name="PRISM"> or <parameterSet name="MC2">. Each 'parameter'
    element has 'name' and 'value' attributes that are used by the experiment
    performing program to parameterise and perform an experiment.    

    ParamsExperiment implements usable load(), save() and reset() methods from 
    the IParamsExperiment interface. has_valid_parameters() and 
    parameter_names() are left to subclasses to implement: in ParamsExperiment 
    they each raise a NotImplementedError when called, as does perform() from 
    the Experiment superclass.    
    
    '''
    implements(IParamsExperiment) # which inherits from IExperiment
    
    def __init__(self, *args, **kwargs):
        super(ParamsExperiment, self).__init__(*args, **kwargs)
#        self.preferences = Preferences(filename='%s.ini' % self.parameters_name)
    
    # Subclasses of ParamsExperiment must specify program.
    program = File(exists=True, desc='path to the executable that accepts the experiments params file.')

    # Subclasses of ParamsExperiment must specify parameters_name. 
    parameters_name = Str
    
    # Subclasses of ParamsExperiment must specify parameter_set_name.
    parameter_set_name = Str(desc='the name attribute of the parameterSet tag in the parameters XML file')

    #FIXME prefer 'path' as trait name? -> affects ParamsExperimentEditor
    #TODO Experiment.file = ... # load or save file on change?
    file = File(desc='the name of the .params file containing this experiments parameters, updated on save() and load(), to be passed to program.')
    def _file_changed(self, file): #TODO
        pass
#        print '%s.file changed' % self.__class__.__name__
    
    #FIXME make this a ListStr trait and use _parameter_names_default instead of parameter_names
    def parameter_names(self):
        raise NotImplementError(
            'Subclasses of ParamsExperiment must reimplement parameters_names()',
        )

    def has_valid_parameters(self): 
        raise NotImplementedError
#        self.problem = '' #TODO





    _cwd_item = Item('_cwd', label='Current working directory', visible_when='object._has_unresolved_paths')
    _has_unresolved_paths = Bool(False)
    # relative paths of File parameters are resolved from the path of the loaded parameters file
    # which will be None if not loaded in which case the user must be prompted.
    _cwd = Directory(desc='')
    def __cwd_changed(self, _cwd):
        pass
#        print _cwd
#        os.chdir(self._cwd)
        #TODO use for keeping cwd across multiple experiments, change to it when editor becomes active, use instead of os.getcwd()
#        print self.preferences, self
#        self.preferences.set('%s._cwd' % self.parameters_name, _cwd)
#        self.preferences.flush()
#        print self.preferences.get('%s._cwd' % self.parameters_name)
#    #FIXME add a current_working_directroy Directory trait to all experiments and expose in Views!


                
    def load(self, file=None):
        ''' Returns True if a params file was successfully loaded. 
        
        Tries to load file, if successful resets traits and *then* parses file. 
        
        '''
        if file is None:
            # get a filename
            fd = FileDialog(wildcard=self.wildcard, title='Load %s experiment parameters' % self.parameter_set_name)
            if fd.open() == OK:
                file = fd.path
        if file is None:
            return False

        if os.path.isabs(file):
            os.chdir(os.path.dirname(file)) # change current directory to directory of params file
        
        # check if file can be read (i.e. path is valid)
        # prompt to locate if not
        # fail gracefully if location unsuccessful
        from infobiotics.dashboard.shared.files import can_read
        if not can_read(file):
            logger.error('can\'t read %s' % file)
            file_in_cwd = os.path.join(os.getcwd(), os.path.basename(file))
            if not can_read(file_in_cwd):
                # get a filename
                fd = FileDialog(wildcard=file, title='Locate %s' % file)
                if fd.open() == OK:
                    file = fd.path
                if file is None or not can_read(file):
                    return False
            else:
                file = file_in_cwd
                logger.debug('can read %s' % file)

        print self.reset()
        # reset traits so we don't carry over parameters that are missing from 
        # the file we are loading
        #TODO reset traits after file successfully parsed, *then* apply traits?

        # open and parse params file with ParamsXMLReader
        # reporting errors or responding to success 
        with open(file, 'rb') as fh:
            parser = sax.make_parser()
            parameters_dictionary = {}
            handler = ParamsXMLReader(parameters_dictionary, self.parameter_set_name)
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
                auto_close_message(message=error) #TODO is this desirable when scripting?...might not happen, as with ProgressDialog
                return False

            # read parameters ok
            
            # set parameters from dictionary
            print parameters_dictionary
            for k, v in parameters_dictionary.iteritems():
                self.set_trait_value_from_parameter_value(k, v)
                
            # success!
            self._cwd = os.getcwd() # keep cwd in trait
            self.file = file # keep file in trait
            return True
        
        print 'got here unexpectedly'
        return False


    def save(self, file=''):
        if file == '':
            # get a filename
            fd = FileDialog(
                action='save as', 
                wildcard=self.wildcard,
                title='Save parameters',
            )
            if fd.open() == OK:
                file = fd.path
            if file == '':
                return False
        with open(file, 'w') as fh:
            try:
                fh.write(self.parameter_file_string()) # important bit, see method below
            except IOError, e:
                logger.error('save(), %s' % e) #TODO message box
                return False
        # success!

        if os.path.isabs(file): #FIXME
            os.chdir(os.path.dirname(file)) # change current directory to directory of params file
        self._cwd = os.getcwd()
        self.file = file

#        self._dirty = False #TODO

        return True

    def parameter_file_string(self): #TODO change name to params_file_string
        '''Returns desired contents of a params file as a string. '''
        s = '''<?xml version="1.0" encoding="utf-8" ?>

<parameters name="%s" xmlns="http://www.cpib.ac.uk/~jpt"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.cpib.ac.uk/~jpt parameter.xsd">

    <!-- parameter definitions -->
    <parameterSet name="%s">
''' % (self.parameters_name, self.parameter_set_name)

        for name in self.parameter_names():
            value = parameter_value_from_trait_value(self, name)
            parameter = '        <parameter name="%s" value="%s"/>\n' % (name, value)
            s += parameter
        s = '''    </parameterSet>

</parameters>
'''     
        return s

    def perform(self): 
        if not self.has_valid_parameters():
            return False


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
            elif trait_type_class_name in ('String', 'Enum', 'File', 'Directory'):
                repr += "%s='%s'" % (parameter_name, eval('self.%s' % parameter_name))
            elif trait_type_class_name == 'Instance': # see ExampleInstanceWithRepr below
                repr += "%s=%s" % (parameter_name, eval('self.%s.__repr__()' % parameter_name))
            else: # Bool, Int, Float, Long, ...
                repr += "%s=%s" % (parameter_name, eval('self.%s' % parameter_name))
        repr += ')'
        return repr

    def __str__(self):
#        return self.parameter_file_string()
#        return "%s(file='%s')" % (self.__class__.__name__, self.file)
        return super(HasTraits, self).__str__()

    



    wildcard = Str(desc='an appropriate wildcard string for a WX or Qt open and save dialog looking for params files.')
    def _wildcard_default(self):
        wildcards = [
            ('Experiment parameters', ['*.params']), 
            ('All files', ['*']),
        ] 
        try:
            import os
            toolkit = os.environ['ETS_TOOLKIT']
        except KeyError:
            toolkit = 'wx'
        wildcard = ''
        if toolkit == 'qt4':
            for i, w in enumerate(wildcards):
                # qt4: 'py and test (*.py *.test)||\ntest (*.test)||\npy (*.py)'
                wildcard += '%s (%s)' % (w[0], ' '.join(w[1])) 
                if i < len(wildcards) - 1:
                    wildcard += '||'#\n'
        else: # assume os.environ['ETS_TOOLKIT'] == ('wx' and not 'null')
            for i, w in enumerate(wildcards):
                # wx: 'py and test (*.py *.test)|*.py;*.test|\ntest (*.test)|*.test|\npy (*.py)|*.py'#|
                w2 = ';'.join(w[1])
                wildcard += '%s (%s)|%s' % (w[0], w2, w2)
                if i < len(wildcards) - 1:
                    wildcard += '|'#\n'
        return wildcard

    
    _dirty = Bool(False)

    
    repr = Str # The "offical" string representation (scripting interface) of this params experiment, updated when any trait changes.
    def _anytrait_changed(self, name, old, new): # move to handler
        ''' Updates 'repr' trait with value of '__repr__()', for display.
        
        This method is called when *any* trait's value changes.
        
        What about '_changed()', or @on_trait_change('*')?
        
        '''
        self.repr = self.__repr__()

    handler = Class(desc='the Handler subclass for TraitsUI')
 
    def configure(self, *args, **kwargs):
        ''' configure_traits() with experiment-specific handler's view. '''
        return self.handler().configure_traits(context={'object':self}, *args, **kwargs)
        
    def edit(self, *args, **kwargs):
        ''' edit_traits() with experiment-specific handler's view. '''
        return self.handler().edit_traits(context={'object':self}, *args, **kwargs)
   

    def reset_parameters(self): 
        unresetable = self.reset_traits(self.parameter_names())
        return unresetable

#    def reset_traits(self): 
#        unresetable = super(ParamsExperiment, self).reset_traits()
#        return unresetable
##    identical to HasTraits.reset_traits() 
    
    def reset(self):
        return self.reset_traits()

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

from infobiotics.shared.dicts import key_from_value 
def trait_value_from_parameter_value(params_experiment, name, value):
    ''' Return parameter trait value from a parameter value string. '''
    try:
        assert name in params_experiment.parameter_names()
    except AssertionError, e:
        print name, e
    trait = params_experiment.trait(name)
    type = trait.trait_type.__class__.__name__
    if type == 'DelegatesTo':
        _delegate = trait._delegate
        setattr(eval('params_experiment.%s' % (_delegate)), name, value)
        #FIXME should go in 'set_trait_value_from_parameter_value'
        return value
    elif type == 'Bool': # convert from lowercase truth values
        return True if value == 'true' else False
    elif type in ('Int', 'IntGreaterThanZero'):
        return int(value) 
    elif type == 'Long':
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
def parameter_value_from_trait_value(params_experiment, name):
    ''' Return parameter value string from a ParamsExperiment parameter trait. ''' 
    assert name in params_experiment.parameter_names()
    trait = params_experiment.trait(name)
    value = params_experiment.trait_get(name)[name] # trait_get returns dict
    type = trait.trait_type.__class__.__name__
    if type == 'Bool': # convert to lowercase truth values
        value = 'true' if value is True else 'false'
    elif type == 'TraitMap': # use shadow_value
        shadow_name = '%s_' % name
        shadow_value = params_experiment.trait_get(shadow_name)[shadow_name]
        # look for a trait with the name in shadow_value and if found return its value
        possible_shadow_trait_dictionary = params_experiment.trait_get(shadow_value)
        if len(possible_shadow_trait_dictionary) > 0:
            shadow_value = possible_shadow_trait_dictionary[shadow_value]
        else:
            value = shadow_value
#    elif type == 'File': value = os.path.basename(value) #FIXME
#    print name, value
    return str(value)
    