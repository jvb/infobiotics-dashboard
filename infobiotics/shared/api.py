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


def can_read(path):
    return can_access(path, os.R_OK)


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


#TODO def trait_value_from_param_value(params, name, value):
def trait_value_from_parameter_value(params, name, value):
    ''' Return parameter trait value from a parameter value string. '''
    try:
        assert name in params.parameter_names()
    except AssertionError, e:
        print name, e
    trait = params.trait(name)
    type = trait.trait_type.__class__.__name__
#    from infobiotics.dashboard.shared.dicts import key_from_value # in this file
    if type == 'DelegatesTo':
        _delegate = trait._delegate
        setattr(eval('params.%s' % (_delegate)), name, value)
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
def parameter_value_from_trait_value(params, name):
    ''' Return parameter value string from a ParamsExperiment parameter trait. ''' 
    assert name in params.parameter_names()
    trait = params.trait(name)
    value = params.trait_get(name)[name] # trait_get returns dict
    type = trait.trait_type.__class__.__name__
    if type == 'Bool': # convert to lowercase truth values
        value = 'true' if value is True else 'false'
    elif type == 'TraitMap': # use shadow_value
        shadow_name = '%s_' % name
        shadow_value = params.trait_get(shadow_name)[shadow_name]
        # look for a trait with the name in shadow_value and if found return its value
        possible_shadow_trait_dictionary = params.trait_get(shadow_value)
        if len(possible_shadow_trait_dictionary) > 0:
            shadow_value = possible_shadow_trait_dictionary[shadow_value]
        else:
            value = shadow_value
#    elif type == 'File': value = os.path.basename(value) #FIXME
#    print name, value
    return str(value)
    

from params import Params
from params_handler import ParamsHandler
from experiment import Experiment
from experiment_progress_handler import ExperimentProgressHandler
from experiment_handler import ExperimentHandler



    
    