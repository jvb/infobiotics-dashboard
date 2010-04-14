# Python 3 imports ---

from __future__ import division, with_statement


# Python 2 imports ---

from threading import Thread

import sys

import os


# 3rd party imports ---

import platform
if platform.system() == 'Windows':
    import wexpect as expect #TODO test with and include wexpect in sys.path
else:
    import pexpect as expect


# my non-ETS module imports

import unified_logging as logging  
logger = logging.get_logger('shared.api')

# Enthought imports ---

os.environ['ETS_TOOLKIT']='qt4' # must be before Enthought import statements

from enthought.traits.api import \
    HasTraits, Interface, implements, File, Directory, Bool, Str, List, \
    Callable, Property, property_depends_on, Range, Button, on_trait_change, \
    Instance, ListStr, Event, Int, Float, Undefined, Enum, Long, Trait, \
    DelegatesTo
    
from enthought.traits.ui.api import \
    Handler, Controller, ModelView, View, Item, Action, DefaultOverride, \
    Group, VGroup, Item, FileEditor, HGroup, UIInfo

from enthought.pyface.api import FileDialog, OK


# custom traits ---

#TODO move this to enthought branch?
from float_greater_than_zero import FloatGreaterThanZero
from long_greater_than_zero import LongGreaterThanZero
from float_with_minimum import FloatWithMinimum
from int_greater_than_zero import IntGreaterThanZero


# reusable trait definitions ---

percentage = Range(0.0, 100.0, 0.0)
 

# actions ---

shared_actions = ['Undo','Revert','OK', 'Cancel']

load_action = Action(name='Load', action='load', 
    tooltip='Load parameters from a file'
) 

save_action = Action(name='Save', action='save', 
    tooltip='Save the current parameters to a file'
)

params_actions = [load_action, save_action]

perform_action = Action(name='Perform', action='perform', 
    tooltip='Perform the experiment with the current parameters',
    enabled_when='object.has_valid_parameters()',
)

experiment_actions = [load_action, save_action, perform_action] 


# subclasses of View ---

class ParamsView(View): # can be used to edit parameters without performing the experiment (why would you want to do that?)
    
    buttons = shared_actions + params_actions
    resizable = True
    id = 'ParamsView'
    

class ExperimentView(ParamsView):

    buttons = shared_actions + experiment_actions
    id = 'ExperimentView'


# mixins ---


class CancelExperimentMixin(object):
    ''' Mixin '''
    cancel = Button
    
    @on_trait_change('cancel')
    def cancelled(self):
        pass


# useful functions

def key_from_value(dict, value):
    ''' Returns the key in a dictionary for a value or None if the value is not 
    found. 
    
    Raises a ValueError if the value is not unique.
    
    def test_key_from_value():
        # test key_from_value unique values
        dict = {'zero':0,'one':1,'two':0}
        print key_from_value(dict, 1) 
        print key_from_value(dict, 0) # same as key_from_value(map, 2)
        
    '''
    # count value
    value_count = dict.values().count(value)
    if value_count == 0:
        # value not found returning None
        return None
    if value_count > 1:
        # value is not unique raising ValueError
        raise ValueError('Multiple keys with value %s:' % value, \
                         ', '.join([k for k in dict.keys() if dict[k] == value]))
    # search for key
    for k, v in dict.iteritems():
        if v == value:
            # found value returning key
            return k


def whereis(program): #TODO rename to 'which'?
    '''
    from: http://jimmyg.org/blog/2009/working-with-python-subprocess.html
    '''
    for path in os.environ.get('PATH', '').split(':'):
        if os.path.exists(os.path.join(path, program)) and not os.path.isdir(os.path.join(path, program)):
            return os.path.join(path, program)
    return None


def can_access(path, mode=os.F_OK):
    '''
    
    os.F_OK tests the existence of a path
    
    http://docs.python.org/library/os.html#files-and-directories
    
    '''
    return os.access(path, mode)

def can_execute(path):
    return can_access(path, os.X_OK)

def can_read(path):
    return can_access(path, os.R_OK)

def read(file, mode='r'):
    if not can_read(file):
        raise IOError("Cannot read '%s'." % file)
    else:
        return open(file, mode)

def read_binary(file):
    return read(file, mode='rb')        

def can_write(path):
    ''' When testing whether a file can be written to the statement:
        "open(path, 'w')" alone will overwrite the file specified by path!
        Use "if not can_write(self.temporal_formulas):" instead.
    '''
    if can_access(path):
        return can_access(path, os.W_OK)
    else:
        # if we got then the file might not exist but we can still test if the 
        # directory is should be in is writable.
        return can_write(os.path.dirname(os.path.abspath(path)))
        
def write(file, mode='w'):
    if not can_write(file):
        raise IOError("Cannot write '%s'." % file)
    else:
        return open(file, mode)

def append(file):
    return write(file, mode='a')

def update(file):
    return write(file, mode='r+')


# Params specific definitions and imports ---

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
    assert name in self.parameter_names()
    trait = self.trait(name)
    type = trait.trait_type.__class__.__name__
#    from infobiotics.dashboard.shared.dicts import key_from_value # in this file
    if type == 'DelegatesTo':
        _delegate = trait._delegate
        setattr(eval('self.%s' % (_delegate)), name, value)
        #FIXME should go in 'set_trait_value_from_parameter_value'
        return value
    elif type == 'Bool': # convert from lowercase truth values
        return True if value == 'true' else False
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
             from infobiotics.shared.api import traits_repr
             return traits_repr(self, [name, age])
    
    '''
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
        elif type in ('Unicode','Str', 'Enum', 'File', 'Directory'):
            repr += "%s='%s'" % (name, getattr(self, '%s' % name))
        else: # Bool, Int, Float, Long, ...
            repr += "%s=%s" % (name, getattr(self, '%s' % name))
    repr += ')'
    return repr      



from params import Params
from params_handler import ParamsHandler
from experiment import Experiment
from experiment_progress_handler import ExperimentProgressHandler
from experiment_handler import ExperimentHandler


# methods to flatten nested lists, taken from http://www.archivum.info/tutor@python.org/2005-01/00506/Re:-[Tutor]-flattening-a-list.html

def flatten(a):
    """Flatten a list."""
    return bounce(flatten_k(a, lambda x: x))

def bounce(thing):
    """Bounce the 'thing' until it stops being a callable."""
    while callable(thing):
        thing = thing()
    return thing

def flatten_k(a, k):
    """CPS/trampolined version of the flatten function.  The original
    function, before the CPS transform, looked like this:

    def flatten(a):
        if not isinstance(a,(tuple,list)): return [a]
        if len(a)==0: return []
        return flatten(a[0])+flatten(a[1:])

    The following code is not meant for human consumption.
    """
    if not isinstance(a,(tuple,list)):
        return lambda: k([a])
    if len(a)==0:
        return lambda: k([])
    def k1(v1):
        def k2(v2):
            return lambda: k(v1 + v2)
        return lambda: flatten_k(a[1:], k2)
    return lambda: flatten_k(a[0], k1)
    
    