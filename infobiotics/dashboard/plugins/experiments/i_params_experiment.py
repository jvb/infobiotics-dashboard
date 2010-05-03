from enthought.traits.api import Instance, List, File, Str
from i_experiment import IExperiment

from enthought.traits.ui.api import Group
from enthought.traits.ui.menu import Action
from params_experiment_handler import ParamsExperimentHandler

class IParamsExperiment(IExperiment):
    ''' Experiment interface.
    
    Defines the interface for an experiment performed using a set of 
    parameters written to an XML file.
    
    '''

    # Subclasses of ParamsExperiment must specify program.
    program = File(exists=True, desc='path to the executable that accepts the experiments params file.')

    # Subclasses of ParamsExperiment must specify parameters_name. 
    parameters_name = Str
    
    # Subclasses of ParamsExperiment must specify parameter_set_name.
    parameter_set_name = Str(desc='the name attribute of the parameterSet tag in the parameters XML file')

    #TODO
    file = File(desc='the name of the .params file containing this experiments parameters, updated on save() and load(), to be passed to program.')

    def parameter_names(self):
        ''' Return the list of parameters to be saved. 
        
        Depending on the value of some parameters some other parameters might 
        not be relevant for the a particular experiment and therefore should
        not be saved. This method is basically a switch for each of these
        circumstances but it also ensures that some utility traits are not 
        saved as parameters. As such this method parameter_names() returns a 
        list of trait names corresponding to a one experiment's parameters.
        
        This method should be overridden to return a *list* of the necessary 
        parameter names, in the most reasonable order that they can be written.
        
        '''

    problem = Str(desc="indicates which trait is preventing the 'Perform' button from being enabled")

    def has_valid_parameters(self):
        ''' Return whether the values of certain parameters are valid.
        
        Whilst the trait definitions for each experiment do an OK job of 
        restricting the possible values of parameters in some cases it is 
        necessary to perform additional validation, for example whether the 
        users has permission to write to a file. This method 
        
        Testing whether a file can be written should be done using the access
        module in the standard library rather than "open(file, 'w')" which will
        automatically overwrite the contents of a file.
        
        This method should be overridden to return a *bool* 
        
        '''        

#    _dirty = Bool(True)
        
    def reset(self):
        ''' Resets experiment parameters to their trait defaults prior to 
        loading. 
        
        Aims to prevent parameter values from the previous experiment changing 
        the expected behaviour of the new experiment.  
        
        #TODO expose the resetting as a user preference?
        
        '''
    
    def load(self, file=None):
        ''' Load a set of experiment parameters from a params file.
        
        Takes the name of a file to load. #TODO accept a file object too.
        
        '''
        
    def save(self, file=None):
        ''' TODO
        
        '''

    #TODO tidy this up
    load_action = save_action = Action
    
    # Enabled when has_valid_parameters() returns True.
    perform_action = Action
    
    # Used by traits_view() to create load and save buttons
#    load_save_actions = List(Action)

    # Used by traits_view() to create load, save and perform buttons
    load_save_perform_actions = List(Action)
    
    # Used by traits_view() to react to action button clicks, and potentially more in subclasses.
    handler = Instance(ParamsExperimentHandler)
    
    # Used by traits_view() as an Include object without using Include (see http://code.enthought.com/projects/traits/docs/html/TUIUG/advanced_view.html#id16).
    group = Instance(Group)

    # Used by traits_view() as title of view. #TEST whether comment or desc appears with trait in Endo-generated documentation 
    name = Str(desc='the name of the experiment being performed')
    
    def traits_view(self):
        ''' Creates the default experiment view of an experiment.
        
        Uses group and name traits, and buttons that are handled by the handler 
        trait.
        
        '''

    # The "offical" string representation (scripting interface) of this params experiment, updated when any trait changes.
    repr = Str
            