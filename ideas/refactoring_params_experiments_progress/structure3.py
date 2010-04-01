'''
Skeletal definitions of interfaces, abstract classes, classes and mixins used 
by Infobiotics programs.

Class names have the general form:
[IM][Specific]General[Context][Function][Handler]
I = Interface
M = Mixin
Specific ~ Mcss
General ~ Experiment
Context ~ Dashboard
Function ~ Progress
Handler = Handler
e.g. IMcssExperimentDashboardProgressHandler

'''




# Imports ---


from __future__ import division
import platform
if platform.system() == 'Windows':
    import wexpect as expect #TODO test with and include wexpect in sys.path
else:
    import pexpect as expect

from threading import Thread

import sys

import os

from enthought.traits.api import \
    HasTraits, Interface, implements, File, Directory, Bool, Str, List, \
    Callable, Property, property_depends_on, Range, Button, on_trait_change, \
    Instance, ListStr, Event, Int, Float
    
from enthought.traits.ui.api import \
    Controller, ModelView, View, Item, Action, RangeEditor




# Traits ---

#class Percentage(Range):
#    
#    def __init__(self, value=None, **metadata):
#        super(Percentage, self).__init__(low=1.0, high=100.0, exclude_low=False, exclude_high=False, **metadata)




# Actions --- #TODO move into Params/Experiment

load_action = Action(name='Load', action='load', 
    tooltip='Load parameters from a file'
) 

save_action = Action(name='Save', action='save', 
    tooltip='Save the current parameters to a file'
)

params_actions = [load_action, save_action]

perform_action = Action(name='Perform', action='perform', 
    tooltip='Perform the experiment with the current parameters',
    enabled_when='object.has_valid_parameters()', #XXX calls has_valid_parameters which each UI change
)

experiment_actions = [load_action, save_action, perform_action] 

shared_actions = ['Undo','Revert','OK', 'Cancel']




# Views ---


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



# Params ---

from enthought.traits.api import Undefined

class Params(HasTraits): 
    
    _parameters_name = Str(Undefined, desc='the name attribute of the parameter tag in the params XML file')
    _parameter_set_name = Str(Undefined, desc='the name attribute of the parameterSet tag in the params XML file')
    _params_file = File(exists=True)
    _cwd = Directory(os.getcwd(), exists=True)
    _dirty = Bool
    
    def __params_file_changed(self, _params_file):
        self._cwd = os.path.dirname(_params_file)
    
    def parameter_names(self): # change to more descriptive name, something to do with the fact that not all parameters will be returned 
        raise NotImplementedError
    
    def load(self, file=None): 
        if file is None:
            raise ValueError
        pass
    
    def save(self, file=None): 
        if file is None:
            raise ValueError
        pass

#    def __init__(self, file=None, *args, **traits):
#        super(Params, self).__init__(*args, **traits)
#        self.load(file)

    title = Property(Str)
    
    @property_depends_on('_params_file')
    def _get_title(self):
        if len(self._params_file) > 0:
            path = self._params_file
        else:
            path = self._params_program
        dirname, basename = os.path.split(path)
        if dirname == '':
            return basename
        else:
            return '%s (%s)' % (basename, dirname)


#class McssParams(Params):
#    model_file = Str('model.lpp', desc='the model file to simulate')
#    model_format = Enum(['xml','sbml','lpp'], desc='the model specification format')
#    duplicate_initial_amounts = Bool(desc='whether to duplicate initial amounts for all templates in the SBML model')
#    just_psystem = Bool(desc='whether to just initialise the P system and not perform the simulation')
#    max_time = FloatGreaterThanZero(desc='the maximum time to run simulation')
#    log_interval = FloatGreaterThanZero(desc='the time interval between which to log data') 
#    runs = LongGreaterThanZero(1, desc='the number of simulation runs to perform')
#    data_file = File('simulation.h5', desc='the file to save simulation data to')
#    seed = Long(0, desc='the random number seed (0=randomly generated)')
#    compress = Bool(True, desc='whether to compress HDF5 output')
#    compression_level = Range(low=0, high=9, value=9, desc='the HDF5 compression level (0-9; 9=best)')
#    simulation_algorithm = Enum(['dmq','dm','ldm','dmgd','dmcp'], desc='the stochastic simulation algorithm to use')
#
#    log_type = Enum(['levels','reactions'], desc='the type of data logging to perform')
#    log_memory = Bool(desc='whether to log output to memory')
#    log_propensities = Bool(desc='whether to log reaction propensities')
#    log_volumes = Bool(desc='whether to log compartment volumes')
#    log_steady_state = Bool(True, desc='whether to log up to max_time if steady state reached')
#    log_degraded = Bool(desc='whether to log levels of degraded species')
#    dump = Bool(desc='whether to dump model to binary format')
#   
#    periodic_x = Bool(desc='whether the x dimension of the lattice has a periodic boundary condition')
#    periodic_y = Bool(desc='whether the y dimension of the lattice has a periodic boundary condition')
#    periodic_z = Bool(desc='whether the z dimension of the lattice has a periodic boundary condition')
#    division_direction = Enum(['x','y','z'], desc='the direction of cell division (x,y,z)')
#    keep_divisions = Bool(desc='whether to keep dividing cells')
#    growth_type = Enum(['none','linear','exponential','function'], desc='the volume growth type')
#    
#    show_progress = Bool(desc='whether to output the current time to screen at each log interval')
#
#
#class McssExperiment(Experiment):
#    parameters = McssParams
#    parameters = Either(McssParams, File)
#    def _parameters_changed(self, parameters):
#        if not isinstance(parameters, McssParams):
#            params = McssParams()
#            params.load(parameters)
#            self.parameters = params      
#    
#    max_time = DelegatesTo('parameters')
#    runs = DelegatesTo('parameters')


class ParamsHandler(Controller):
    
    def load(self, info): 
        file=None
        info.object.load(file)
    
    def save(self, info):
        file=None
        info.object.save(file)

    traits_view = ParamsView(
        Item('_cwd', label='Working directory', tooltip='Relative paths will be relative to this directory.'),
    )

    def object_title_changed(self, info):
        info.ui.title = info.object.title

 

# Experiment ---


class Experiment(Params):
    
    _params_program = File(exists=True)
    _params_program_kwargs = ListStr
    _output_pattern_list = ListStr
    _error_pattern_list = ListStr([
        '^[eE]rror:.*', # mcss 'error: unknown parameter how_progress'
        '^[eE]rror[^:].+\nline [0-9]+: \([0-9]+ \[Error\]\) .*', # Fran & LibSBML 'error reading sbml input file\nline 1: (00002 [Error]) File unreadable.' 
        '^[eE]rror[^:].*', # Fran 'error ...'
        '^.+: command not found', # bash
        '^I/O warning : failed to load external entity ".+"', # libxml++
    ])
    _error_string = Str
    starting = Event
    started = Event
    timed_out = Event
    finished = Event
    
#    @on_trait_change('started')
#    def forward_program_output_to_stdout(self):
##    def _started_fired(self):
#        ''' An example of responding to an Event. '''
#        self.child.logfile_read = sys.stdout

#    def has_valid_parameters(self): 
#        raise NotImplementedError
##        self.error = '' #TODO see Invalid...demo

    def perform(self, thread=False): 
        ''' Spawns an expect process and handles it in a separate thread. '''
#        if not self.has_valid_parameters():
#            return False

        def _spawn():
            ''' Start the program and try to match output.
            
            Spawns the program (starting it in self.cwd), 
            compiles list of patterns for expect_list, 
            adds EOF to list,
            calls 'started' hook,
            loops calling the '_output_pattern_matched' hook with the index of the pattern
            and the match until EOF whereupon it calls the 'finished' hook.
             
            '''
            starting = True
    
            # spawn process
            self.child = expect.spawn(self._params_program, [self._params_file] + self._params_program_kwargs[:], cwd=self._cwd) # _cwd defined in Params
            # note that the expect module doesn't like list traits so we copy them using [:] 
    
            # useful for debugging
#            self.child.logfile_read = sys.stdout #TODO comment out in release
    
            self.started = True
    
            # compile pattern list for expect_list
            compiled_pattern_list = self.child.compile_pattern_list(self._output_pattern_list + self._error_pattern_list)
            
            # append EOF to compiled pattern list
            compiled_pattern_list.append(expect.EOF)
            eof_index = compiled_pattern_list.index(expect.EOF)
            
            # append TIMEOUT to compiled pattern list
            compiled_pattern_list.append(expect.TIMEOUT)
            timeout_index = compiled_pattern_list.index(expect.TIMEOUT)
            
            # expect loop
            while True:
                pattern_index = self.child.expect_list(compiled_pattern_list)
                if pattern_index == eof_index:
                    # process has finished, perhaps prematurely
                    break
                elif pattern_index == timeout_index:
                    self.timed_out = True
                else:
                    self._output_pattern_matched(pattern_index, self.child.match.group())
    
            self.finished = True

        if thread:
            Thread(target=_spawn).start()
        else:
            _spawn()

    def _output_pattern_matched(self, pattern_index, match):
        ''' Update traits in response to matching error patterns.
        
        Subclasses should call this method after processing their own patterns,
        e.g.:
            if pattern_index == 0:
                # do something
            elif pattern_index == 1:
                # do something else
            else:
                # pattern_index not defined by this class, pass to superclass
                ParamsExpect._output_pattern_matched(self, pattern_index, match)
                # or
#                super(McssExpect, self)._output_pattern_matched(pattern_index, match)
                
        '''
        self._error_string = match.split('rror')[1].strip(':') if 'rror' in match else match

    def __error_string_changed(self, _error_string):
        print _error_string
        

class ExperimentHandler(ParamsHandler):
    
    _progress_handler = Callable # a class inheriting from IExperimentProgressHandler
    
    def perform(self, info):
        ''' Perform the experiment. '''
        self.model.perform(thread=True)
        self._show_progress()

    def _show_progress(self):
        progress_handler = self._progress_handler(model=self.model)
        progress_handler.edit_traits(kind='live')

    traits_view = ExperimentView(
        Item('_cwd', label='Working directory', tooltip='Relative paths will be relative to this directory.'),
    )


from enthought.traits.ui.api import DefaultOverride

class ExperimentProgressHandler(ModelView): # --> Mixin?
    
    progress = Property(Range(0.0, 100.0, 0.0)) # subclasses must repeat this line!?
    status = Property(Str)

    def _get_progress(self):
        raise NotImplementedError
    
    def _get_status(self):
        raise NotImplentedError
    
    traits_view = View(
        Item('progress', editor=DefaultOverride(low_label='0%', high_label='100%', format='%2.1f')),
        'status',
    )

    def model_finished_fired(self):
        print 'finished'

    def model_title_changed(self, info):
        info.ui.title = info.model.title
        
    def _progress_changed(self, progress):
        print progress
        
# mcss ---


class McssExperiment(Experiment):
    
    _params_program = 'mcss'
    _params_program_kwargs = ['show_progress=true', 'max_time=333', 'runs=66']
    _output_pattern_list = [
        '[0-9]+ [0-9]+', # 'time_in_run, run'
    ] 

    # parameters
    max_time = Float(333.0)
    runs = Int(66)
    
    # output patterns
    run = Int(1)
    time_in_run = Float

    def _output_pattern_matched(self, pattern_index, match):
        if pattern_index == 0: # '1 20.5'
            time_in_run, run = match.split(' ')
            self.run = int(run)
            self.time_in_run = float(time_in_run)
        else:
            super(McssExperimentProgressHandler, self)._output_pattern_matched(pattern_index, match)


class McssExperimentProgressHandler(ExperimentProgressHandler):
    
    progress = Property(Range(0.0, 100.0, 0))
    
    @property_depends_on('model.time_in_run, model.runs, model.max_time')#model.run
    def _get_progress(self):
        percentage = float((((self.model.time_in_run) + ((self.model.run - 1) * self.model.max_time)) / (self.model.max_time * self.model.runs)) * 100) 
#        print '%s/%s %s/%s'%(self.model.time_in_run, self.model.max_time, self.model.run, self.model.runs), percentage
        return percentage

    def _get_status(self):
        return 'todo'


class McssExperimentHandler(ExperimentHandler):

    _progress_handler = McssExperimentProgressHandler

    traits_view = ExperimentView(
        Item('_cwd', label='Working directory', tooltip='Relative paths will be relative to this directory.'),
    )
    
class McssExperimentDashboardProgressHandler(McssExperimentProgressHandler, CancelExperimentMixin):
    pass
    

class McssExperimentDashboardHandler(McssExperimentHandler):

    _progress_handler = McssExperimentDashboardProgressHandler

    def _show_progress(self):
        pass
        print '%s._show_progress: delegating to McssExperimentHandler' % self
        super(McssExperimentDashboardHandler, self)._show_progress()




# pmodelchecker ---
    
    
class PModelCheckerExperiment(Experiment): 

    _params_program = 'pmodelchecker'
    _parameters_name = 'pmodelchecker'


class PModelCheckerExperimentHandler(ExperimentHandler):
    pass



# MC2 --


class MC2Experiment(PModelCheckerExperiment):

    _parameter_set_name = 'mc2'
    model_checker = 'MC2'

    
class MC2ExperimentProgressHandler(ExperimentProgressHandler):

    @property_depends_on('pass')
    def _get_progress(self):
        pass

    def _get_status(self):
        pass


class MC2ExperimentHandler(PModelCheckerExperimentHandler):

    _progress_handler = MC2ExperimentProgressHandler 

    traits_view = ExperimentView(
        Item('_cwd', label='Working directory', tooltip='Relative paths will be relative to this directory.'),
    )


class MC2ExperimentDashboardProgressHandler(MC2ExperimentProgressHandler, CancelExperimentMixin):
    pass


class MC2ExperimentDashboardHandler(MC2ExperimentHandler):

    _progress_handler = MC2ExperimentDashboardProgressHandler

    def _show_progress(self):
        pass



# PRISM --


class PRISMExperiment(PModelCheckerExperiment):
    
    _parameter_set_name = 'prism'
    model_checker = 'PRISM'


class PRISMExperimentProgressHandler(ExperimentProgressHandler):

    @property_depends_on('pass')
    def _get_progress(self):
        pass

    def _get_status(self):
        pass


class PRISMExperimentHandler(PModelCheckerExperimentHandler):
    
    _progress_handler = PRISMExperimentProgressHandler

    traits_view = ExperimentView(
        Item('_cwd', label='Working directory', tooltip='Relative paths will be relative to this directory.'),
    )
    

class PRISMExperimentDashboardProgressHandler(PRISMExperimentProgressHandler, CancelExperimentMixin):
    pass
    
    
class PRISMExperimentDashboardHandler(PRISMExperimentHandler):

    _progress_handler = PRISMExperimentDashboardProgressHandler

    def _show_progress(self):
        pass




# poptimizer ---


class POptimizerExperiment(Experiment):

    _params_program = 'poptimizer'
    _parameters_name = 'poptimizer'
    _parameter_set_name = 'poptimizer'
    
    
class POptimizerExperimentProgressHandler(ExperimentProgressHandler):

    @property_depends_on('pass')
    def _get_progress(self):
        pass

    def _get_status(self):
        pass


class POptimizerExperimentHandler(ExperimentHandler):
    
    _progress_handler = POptimizerExperimentProgressHandler
    
    traits_view = ExperimentView(
        Item('_cwd', label='Working directory', tooltip='Relative paths will be relative to this directory.'),
        Item(label='testing override traits_view'),
    )


class POptimizerExperimentDashboardProgressHandler(POptimizerExperimentProgressHandler, CancelExperimentMixin):
    pass


class POptimizerExperimentDashboardHandler(POptimizerExperimentHandler):

    _progress_handler = POptimizerExperimentDashboardProgressHandler

    def _show_progress(self):
        print 'got here'




def mcss(*args, **traits):
    if len(args) < 1 or args[0] is None:
        raise ValueError
    if isinstance(args[0], str):
        file = args[0]
        mcss_experiment = McssExperiment(file)
#    mcss_experiment_handler = McssExperimentHandler(model=mcss_experiment)
#    mcss_experiment_handler.configure_traits()
    mcss_experiment.perform()




if __name__ == '__main__':

    mcss_experiment = McssExperiment(_params_file='/home/jvb/src/mcss-0.0.35-0.0.35/examples/models/reactions1.params')
    print mcss_experiment._parameters_name
#    mcss_experiment.configure_traits()
#    mcss_experiment_handler = McssExperimentHandler(model=mcss_experiment)
    mcss_experiment_handler = McssExperimentDashboardHandler(model=mcss_experiment)
#    mcss_experiment_handler = McssExperimentProgressHandler(model=mcss_experiment).configure_traits()
#    mcss_experiment_handler = McssExperimentDashboardProgressHandler(model=mcss_experiment)
#    mcss_experiment_handler._show_progress()
    mcss_experiment_handler.configure_traits()
#    mcss('abc')


#    pmodelchecker_experiment = PModelCheckerExperiment()
##    pmodelchecker_experiment.configure_traits()
#    pmodelchecker_experiment_handler = PModelCheckerExperimentHandler(model=pmodelchecker_experiment)
##    pmodelchecker_experiment_handler = PModelCheckerExperimentProgressHandler(model=pmodelchecker_experiment).configure_traits()
##    pmodelchecker_experiment_handler = PModelCheckerExperimentDashboardProgressHandler(model=pmodelchecker_experiment)
##    pmodelchecker_experiment_handler._show_progress()
#    pmodelchecker_experiment_handler.configure_traits()
##    pmodelchecker('abc')


#    poptimizer_experiment = POptimizerExperiment()

#    poptimizer_experiment.configure_traits()
#    poptimizer_experiment.configure_traits(view=ParamsView())
#    poptimizer_experiment.configure_traits(view=ExperimentView())

#    poptimizer_experiment_handler = POptimizerExperimentHandler(model=poptimizer_experiment)
#    poptimizer_experiment_handler._show_progress()
#    poptimizer_experiment_handler.configure_traits()

#    poptimizer_experiment_handler = POptimizerExperimentDashboardHandler(model=poptimizer_experiment)
#    poptimizer_experiment_handler._show_progress() # prints 'got here'
#    poptimizer_experiment_handler.configure_traits()
