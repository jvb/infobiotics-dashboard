from infobiotics.shared.api import Params, Str, Enum, Bool, File, Range, \
    Long, FloatGreaterThanZero, LongGreaterThanZero, Instance

class McssParams(Params):
    
    _parameters_name = 'mcss'
    _parameter_set_name = 'SimulationParameters'
    
#    model_file = File('model.lpp', exists=True, desc='the model file to simulate')
#    model_file = File('model.lpp', desc='the model file to simulate')
    model_file = Str('model.lpp', desc='the model file to simulate')
    model_format = Enum(['xml','sbml','lpp'], desc='the model specification format')
    duplicate_initial_amounts = Bool(desc='whether to duplicate initial amounts for all templates in the SBML model')
    just_psystem = Bool(desc='whether to just initialise the P system and not perform the simulation')
    max_time = FloatGreaterThanZero(desc='the maximum time to run simulation')
    log_interval = FloatGreaterThanZero(desc='the time interval between which to log data') 
    runs = LongGreaterThanZero(1, desc='the number of simulation runs to perform')
    data_file = File('simulation.h5', desc='the file to save simulation data to')
    seed = Long(0, desc='the random number seed (0=randomly generated)')
    compress = Bool(True, desc='whether to compress HDF5 output')
    compression_level = Range(low=0, high=9, value=9, desc='the HDF5 compression level (0-9; 9=best)')
    simulation_algorithm = Enum(['dmq','dm','ldm','dmgd','dmcp'], desc='the stochastic simulation algorithm to use')

    log_type = Enum(['levels','reactions'], desc='the type of data logging to perform')
    log_memory = Bool(desc='whether to log output to memory')
    log_propensities = Bool(desc='whether to log reaction propensities')
    log_volumes = Bool(desc='whether to log compartment volumes')
    log_steady_state = Bool(True, desc='whether to log up to max_time if steady state reached')
    log_degraded = Bool(desc='whether to log levels of degraded species')
    dump = Bool(desc='whether to dump model to binary format')
   
    periodic_x = Bool(desc='whether the x dimension of the lattice has a periodic boundary condition')
    periodic_y = Bool(desc='whether the y dimension of the lattice has a periodic boundary condition')
    periodic_z = Bool(desc='whether the z dimension of the lattice has a periodic boundary condition')
    division_direction = Enum(['x','y','z'], desc='the direction of cell division (x,y,z)')
    keep_divisions = Bool(desc='whether to keep dividing cells')
    growth_type = Enum(['none','linear','exponential','function'], desc='the volume growth type')
    
    # not in parameter_names
    show_progress = Bool(desc='whether to output the current time to screen at each log interval')

    def parameter_names(self):
        return [
            'model_file', 'model_format', 'duplicate_initial_amounts', 
            'just_psystem', 'max_time', 'log_interval', 'runs', 'data_file', 
            'seed', 'compress', 'compression_level', 'show_progress', 
            'simulation_algorithm', 'log_type', 'log_memory', 
            'log_propensities', 'log_volumes', 'log_steady_state', 
            'log_degraded', 'dump', 'periodic_x', 'periodic_y', 'periodic_z',
            'division_direction', 'keep_divisions', 'growth_type' 
        ]
        
    def _handler_default(self):
        from mcss_params_handler import McssParamsHandler
        return McssParamsHandler()
        
#    def configure(self, **args):
#        from mcss_params_handler import McssParamsHandler
#        handler = McssParamsHandler(parameters=self)
#        return handler.configure_traits(kind='modal', **args)

    def edit(self, **traits):
        from mcss_params_handler import McssParamsHandler
        handler = McssParamsController(parameters=self)
        return handler.edit_traits(kind='live', *args, **kwargs)
        