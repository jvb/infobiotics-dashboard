from infobiotics.core.api import ParamsRelativeFile
from infobiotics.core.params import Params
from enthought.traits.api import Enum, Bool, Range, Long, Property, Float
from infobiotics.commons.traits.api import FloatGreaterThanZero, LongGreaterThanZero
from infobiotics.mcss.mcss_preferences import McssParamsPreferencesHelper

class McssParams(Params):

    def _handler_default(self):
        from infobiotics.mcss.api import McssParamsHandler
        return McssParamsHandler(model=self)

    def _preferences_helper_default(self):
        helper = McssParamsPreferencesHelper()
        return helper

    executable_name = 'mcss'
    
    _parameters_name = 'mcss'
    _parameter_set_name = 'SimulationParameters'
        
    model_file = ParamsRelativeFile(desc='the model file to simulate',
        exists=True,
        filter=[
            'All model files (*.lpp *.sbml)',
            'Lattice population P system files (*.lpp)',
            'P system XML files (*.xml)',
            'Systems Biology Markup Language files (*.sbml)',
            'All files (*)'
        ],
        entries=10,
    )
    model_format = Enum(['sbml', 'xml', 'lpp'], desc='the model specification format')
    duplicate_initial_amounts = Bool(False, desc='whether to duplicate initial amounts for all templates in the SBML model')
#    just_psystem = Bool(False, desc='whether to just initialise the P system and not perform the simulation')
    max_time = FloatGreaterThanZero(desc='the maximum time to run simulation')
    log_interval = FloatGreaterThanZero(1.0, desc='the time interval between which to log data') 
    runs = LongGreaterThanZero(1, desc='the number of simulation runs to perform')
    data_file = ParamsRelativeFile('simulation.h5', writable=True, desc='the file to save simulation data to')
    seed = Long(0, desc='the random number seed (0=randomly generated)')
    compress = Bool(True, desc='whether to compress HDF5 output')
    compression_level = Range(low=0, high=9, value=9, desc='the HDF5 compression level (0-9; 9=best)')
    simulation_algorithm = Enum(['dmq2', 'dmq', 'dm', 'ldm', 'dmgd', 'dmcp', 'dmqg', 'dmq2g', 'dmq2gd'], desc='the stochastic simulation algorithm to use')

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
    division_direction = Enum(['x', 'y', 'z'], desc='the direction of cell division (x,y,z)')
    keep_divisions = Bool(False, desc='whether to keep dividing cells (no need for degradation rates to emulate dilution by cell division)')
    growth_type = Enum(['none', 'linear', 'exponential', 'function'], desc='the volume growth type')
    
    show_progress = Bool(False, desc='whether to output the current time to screen at each log interval') # not in parameter_names below
    progress_interval = Float(0.0, desc='time interval within each run to output progress information') #TODO
    
    def parameter_names(self):
        return [
            'model_file', 'model_format', 'duplicate_initial_amounts',
#            'just_psystem', 
            'max_time', 'log_interval', 'runs', 'data_file',
            'seed', 'compress', 'compression_level', #'show_progress', 
            'simulation_algorithm', 'log_type', 'log_memory',
            'log_propensities', 'log_volumes', 'log_steady_state',
            'log_degraded', 'dump', 'periodic_x', 'periodic_y', 'periodic_z',
            'division_direction', 'keep_divisions', 'growth_type' 
        ]


if __name__ == '__main__':
    parameters = McssParams()
#    parameters.load('../../tests/workbench_examples/modules/module1.params')
    parameters.load('/home/jvb/src/mcss-0.0.41/examples/models/module1.params')
#    parameters.edit()
    parameters.configure()
            
