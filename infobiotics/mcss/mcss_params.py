from infobiotics.shared.api import \
    Params, File, Enum, Bool, Range, Long, \
    FloatGreaterThanZero, LongGreaterThanZero

class McssParams(Params):
    
#    def __cwd_changed(self):
#        print 'got here'
#        model_file = self.model_file
##        self.model_file = ''
#        self.model_file = model_file
    
    _parameters_name = 'mcss'
    _parameter_set_name = 'SimulationParameters'
    
    model_file = File('model.lpp', 
        exists=True, 
        desc='the model file to simulate', 
        directory_name='_cwd', 
        auto_set=True,
        filter=[
            'All model files (*.lpp *.sbml)', 
            'Lattice population P system files (*.lpp)', 
            'P system XML files (*.xml)', 
            'Systems Biology Markup Language files (*.sbml)', 
            'All files (*)'
        ],
        entries=10,
    )
    model_format = Enum(['xml','sbml','lpp'], desc='the model specification format')
    duplicate_initial_amounts = Bool(desc='whether to duplicate initial amounts for all templates in the SBML model')
    just_psystem = Bool(desc='whether to just initialise the P system and not perform the simulation')
    max_time = FloatGreaterThanZero(desc='the maximum time to run simulation')
    log_interval = FloatGreaterThanZero(desc='the time interval between which to log data') 
    runs = LongGreaterThanZero(1, desc='the number of simulation runs to perform')
    data_file = File('simulation.h5', writable=True, auto_set=True, directory_name='_cwd', desc='the file to save simulation data to')
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
        from infobiotics.mcss.api import McssParamsHandler
        return McssParamsHandler(model=self)


if __name__ == '__main__':
    from infobiotics.shared.api import chdir
#    chdir('../../tests/mcss/models')
#    parameters = McssParams('module1.params')
    parameters = McssParams('../../tests/mcss/models/module1.params')
#    parameters.load('reactions1.params')
#    print parameters # test __repr__
    parameters.configure()
            