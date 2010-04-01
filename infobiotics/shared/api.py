# Imports ---

from __future__ import division, with_statement

import platform
if platform.system() == 'Windows':
    import wexpect as expect #TODO test with and include wexpect in sys.path
else:
    import pexpect as expect

from threading import Thread

import sys

import os

os.environ['ETS_TOOLKIT']='qt4'

from enthought.traits.api import \
    HasTraits, Interface, implements, File, Directory, Bool, Str, List, \
    Callable, Property, property_depends_on, Range, Button, on_trait_change, \
    Instance, ListStr, Event, Int, Float, Undefined, Enum, Long, Trait, \
    DelegatesTo
    
from enthought.traits.ui.api import \
    Handler, Controller, ModelView, View, Item, Action, DefaultOverride, \
    Group, VGroup, Item, FileEditor, HGroup

from float_greater_than_zero import FloatGreaterThanZero
from long_greater_than_zero import LongGreaterThanZero
from float_with_minimum import FloatWithMinimum
from int_greater_than_zero import IntGreaterThanZero

percentage = Range(0.0, 100.0, 0.0)
 

# Actions ---

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
#    enabled_when='object.has_valid_parameters()', #XXX calls has_valid_parameters which each UI change
)

experiment_actions = [load_action, save_action, perform_action] 


# View classes ---

class ParamsView(View): # can be used to edit parameters without performing the experiment (why would you want to do that?)
    
    buttons = shared_actions + params_actions
    resizable = True
    id = 'ParamsView'
    

class ExperimentView(ParamsView):

    buttons = shared_actions + experiment_actions
    id = 'ExperimentView'


# Mixins ---


class CancelExperimentMixin(object):
    ''' Mixin '''
    cancel = Button
    
    @on_trait_change('cancel')
    def cancelled(self):
        pass
    

from params import Params
from params_handler import ParamsHandler
from experiment import Experiment
from experiment_progress_handler import ExperimentProgressHandler
from experiment_handler import ExperimentHandler

