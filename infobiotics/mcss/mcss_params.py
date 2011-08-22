from infobiotics.core.api import ParamsRelativeFile, ModelFile
from infobiotics.core.params import Params
from enthought.traits.api import Enum, Bool, Range, Long, Float, Int
from infobiotics.commons.traits.api import FloatGreaterThanZero, LongGreaterThanZero
from enthought.traits.api import TraitError
import os.path

from infobiotics.commons.api import logging
logger = logging.getLogger(__name__)

class McssParams(Params):

    def __handler_default(self):
        from infobiotics.mcss.mcss_params_handler import McssParamsHandler
        return McssParamsHandler(model=self)

    def _preferences_helper_default(self):
        from infobiotics.mcss.mcss_preferences import McssParamsPreferencesHelper
        return McssParamsPreferencesHelper()

    executable_name = 'mcss'
    
    _parameters_name = 'mcss'
    _parameter_set_name = 'SimulationParameters'

    def _model_file_changed(self):
        directory, model_file = os.path.split(self.model_file_)
        try:
            if directory != '':
                self.directory = directory #TODO os.path.normpath(directory)
        except TraitError, e:
            logger.warn(e)
        try:
            # problem: model_specification is appearing relative to the previous
            # directory
            # solution (avoiding infinite loop):
            # first set it without notifying change handlers
            self.trait_setq(model_file=model_file)
            # second notify change handlers by setting it
            self.model_file = model_file
        except TraitError, e:
            logger.warn(e)
    
    model_file = ModelFile
    
    # overridden in McssParamsHandler
    model_format = Enum(['sbml', 'xml', 'lpp'], desc='the model specification format')
    
    duplicate_initial_amounts = Bool(True, desc='whether to duplicate initial amounts for all templates in the SBML model')
#    just_psystem = Bool(False, desc='whether to just initialise the P system and not perform the simulation')
    max_time = FloatGreaterThanZero(desc='the maximum simulated time')
    max_run_time = Range(low=0, desc='the maximum execution time for all runs')
    log_interval = FloatGreaterThanZero(1.0, desc='the time interval between which to log data') 
    runs = LongGreaterThanZero(1, desc='the number of simulation runs to perform')
    data_file = ParamsRelativeFile('simulation.h5', writable=True, filter=['HDF5 files (*.h5)'], desc='the file to save simulation data to')
    seed = Long(0, desc='the random number seed (0=randomly generated)')
    compress = Bool(True, desc='whether to compress HDF5 output')
    compression_level = Range(low=0, high=9, value=9, desc='the HDF5 compression level (0-9; 9=best)')
    
    # overridden in McssParamsHandler
    simulation_algorithm = Enum(['ode1','dmq2', 'dmq', 'dm', 'ldm', 'dmgd', 'dmcp', 'dmqg', 'dmq2g', 'dmq2gd'])

    # overridden in McssParamsHandler
    ode_solver = Enum(['rk2','rk4','rkf45','rkck','rk8pd','rk2imp','rk4imp','bsimp','gear1','gear2'])

    log_type = Enum(['levels', 'reactions'], desc='the type of data logging to perform')
    log_memory = Bool(desc='whether to log output to memory')
    log_propensities = Bool(desc='whether to log reaction propensities')
    log_volumes = Bool(desc='whether to log compartment volumes')
    log_steady_state = Bool(True, desc='whether to log up to max_time if steady state reached')
    log_degraded = Bool(desc='whether to log levels of degraded species')
    dump = Bool(desc='whether to dump model to binary format')
   
    periodic_x = Bool(desc='whether the x dimension of the lattice has a periodic boundary condition')
    periodic_y = Bool(desc='whether the y dimension of the lattice has a periodic boundary condition')
    periodic_z = Bool(desc='whether the z dimension of the lattice has a periodic boundary condition')
    #TODO x_boundary = yboundary = z_boundary = Enum(['solid','periodic','void','helical?']
    
    division_direction = Enum(['x', 'y', 'z'], desc='the direction of cell division (x,y,z)')
    keep_divisions = Bool(False, desc='whether to keep dividing cells (no need for degradation rates to emulate dilution by cell division)')
    growth_type = Enum(['none', 'linear', 'exponential', 'function'], desc='the volume growth type')
    
    # overridden in McssParamsHandler
    neighbourhood = Enum([4,8])
    
    show_progress = Bool(False, desc='whether to output the current time to screen at each log interval')
    progress_interval = Float(0.0, desc='time interval within each run to output progress information')
    
    def parameter_names(self):
        return [
            'model_file', 
            'model_format', 
                'duplicate_initial_amounts', # SBML
#                'just_psystem', # P system XML?

            'max_time', 
            'log_interval', 
            'runs', 
            
            'data_file', 
            'seed', 
            
            'compress', 
            'compression_level', 

            'simulation_algorithm', 
            'ode_solver',
            
            'log_memory',
            'log_type', 
            'log_propensities', 
            'log_volumes', 
            'log_steady_state',
            'log_degraded', 
#            'dump', 
            
            'neighbourhood',
            
            'periodic_x', 
            'periodic_y', 
            'periodic_z',
            
            'division_direction', 
            
            'keep_divisions', 
            'growth_type', 
            
            'show_progress', 
            'progress_interval', 
        ]

    _runs = 1

    def _simulation_algorithm_changed(self, old, new):
        if old != 'ode1' and new == 'ode1':
            self._runs = self.runs
            self.runs = 1
        elif old=='ode1' and new != 'ode1':
            self.runs = self._runs


if __name__ == '__main__':
    parameters = McssParams()#executable='/usr/bin/mcs')
#    print 'executable', parameters.executable
    parameters.configure()
            
