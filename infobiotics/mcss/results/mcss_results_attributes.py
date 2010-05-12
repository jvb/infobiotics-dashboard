from enthought.traits.api import Enum, HasTraits, Int, Str
from commons.traits.api import FloatGreaterThanZero, IntGreaterThanZero, RelativeFile

ModelFormat = Enum(['sbml','xml'])
SimulationAlgorithm = Enum(['dm','ldm','...'])
LogType = Enum(['levels','reactions'])
GrowthType = Enum(['...'])

class McssResultsAttributes(HasTraits):
    '''
    mcss version: 0.0.36
    model input file: reactions1.sbml
    model format: sbml
    data file: reactions1.h5
    number of runs: 1
    simulation algorithm: dm
    simulation algorithm name: Multicompartment Gillespie
    log type: levels
    log interval: 1.000000
    max time: 60.000000
    seed: 2480546808506876035
    duplicate initial amounts: 0
    log degraded: 1
    log volumes: 0
    log propensities: 0
    periodic x: 0
    periodic y: 0
    periodic z: 0
    number of species: 6
    number of rule templates: 1
    number of rules in templates: 7
    total number of rules: 0
    lattice x dimension: 1
    lattice y dimension: 1
    lattice z dimension: 0
    growth type: none
    keep divisions: 0
    division direction: y
    simulation start time: 15:02:16 03/05/10
    simulation end time: 15:02:16 03/05/10
    total simulation time: 0.000592 seconds
    number of compartments: 1
    simulated time: 1 minute 0 seconds (60 seconds)
    run start time: 15:02:16 03/05/10
    run end time: 15:02:16 03/05/10
    total run time: 0.000083 seconds
    total preprocessing time: 0.000007 seconds
    main loop total time: 0.000033 seconds
    total reactions simulated: 0
    reactions per second: 0
    '''
    mcss_version = Str
    model_input_file = RelativeFile # in McssParams
    model_format = ModelFormat # defined outside class as shared with McssParams
    data_file = RelativeFile # in McssParams
    number_of_runs = IntGreaterThanZero # in McssParams
    simulation_algorithm = SimulationAlgorithm # defined outside class as shared with McssParams
    log_type = LogType # defined outside class as shared with McssParams
    
    log_interval = FloatGreaterThanZero
    max_time = FloatGreaterThanZero
    
    seed = Long # in McssParams
    duplicate_initial_amounts = Enum([0, 1]) # Bool in McssParams
    log_degraded = Enum([0, 1])
    log_volumes = Enum([0, 1])
    log_propensities = Enum([0, 1])
    periodic_x = Enum([0, 1])
    periodic_y = Enum([0, 1])
    periodic_z = Enum([0, 1])
    number_of_species = IntGreaterThanZero
    number_of_rule_templates = Int
    number_of_rules_in_templates = Int
    total_number_of_rules = Int
    lattice_x_dimension = Int
    lattice_y_dimension = Int
    lattice_z_dimension = Int
    growth_type = GrowthType
    keep_divisions = Enum([0, 1])
    division_direction = Enum(['x','y','z'])
    simulation_start_time = Str
    simulation_end_time = Str
    total_simulation_time = Str
    number_of_compartments = IntGreaterThanZero
    simulated_time = Str
    run_start_time = Str
    run_end_time = Str
    total_run_time = Str
    total_preprocessing_time = Str
    main_loop_total_time = Str
    total_reactions_simulated = Int
    reactions_per_second = Int
    
    def load_from_h5(self, h5_file):
        pass 
    