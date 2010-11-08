import tables
from enthought.traits.api import Property, HasTraits, Enum, Trait, Int, Str, Long, List
from infobiotics.commons.traits.api import FloatGreaterThanZero, IntGreaterThanZero, RelativeFile
from enthought.traits.ui.api import View, Item, HGroup

# defined outside class as shared with McssParams
ModelFormat = Enum(['xml', 'sbml', 'lpp'], desc='the model specification format')
SimulationAlgorithm = Enum(['dmq2', 'dmq', 'dm', 'ldm', 'dmgd', 'dmcp', 'dmqg', 'dmq2g', 'dmq2gd'], desc='the stochastic simulation algorithm to use')
LogType = Enum(['levels', 'reactions'], desc='the type of data logging to perform') #TODO why does it have to be one or the other, both would be very useful. Also where are rate constants stored in data_file?
DivisionDirection = Enum(['x', 'y', 'z'], desc='the direction of cell division (x,y,z)')
GrowthType = Enum(['none', 'linear', 'exponential', 'function'], desc='the volume growth type')
Boolean = Trait(
    0,
    {
        0:False,
        1:True,
        '0':False,
        '1':True,
        'false':False,
        'true':True,
        False:False,
        True:True,
    }
)
#TODO move these to infobiotics.mcss.traits and import in __init__.py


#class Run(HasTraits):
#    
#    main_loop_end_time = Property(Str)
#    def _get_main_loop_end_time(self):
#        return self._main_loop_end_time
#    _main_loop_end_time = Str
#    #Item('main_loop_end_time', style='readonly'),
#    
#    main_loop_start_time = Property(Str)
#    def _get_main_loop_start_time(self):
#        return self._main_loop_start_time
#    _main_loop_start_time = Str
#    #Item('main_loop_start_time', style='readonly'),
#    
#    number_of_compartments = Property(IntGreaterThanZero)
#    def _get_number_of_compartments(self):
#        return self._number_of_compartments
#    _number_of_compartments = IntGreaterThanZero
#    #Item('number_of_compartments', style='readonly'),
#    
#    number_of_timepoints = Property(IntGreaterThanZero)
#    def _get_number_of_timepoints(self):
#        return self._number_of_timepoints
#    _number_of_timepoints = IntGreaterThanZero
#    #Item('number_of_timepoints', style='readonly'),
#    
#    preprocess_end_time = Property(Str)
#    def _get_preprocess_end_time(self):
#        return self._preprocess_end_time
#    _preprocess_end_time = Str
#    #Item('preprocess_end_time', style='readonly'),
#
#    preprocess_start_time = Property(Str)
#    def _get_preprocess_start_time(self):
#        return self._preprocess_start_time
#    _preprocess_start_time = Str
#    #Item('preprocess_start_time', style='readonly'),
#    
#    run_end_time = Property(Str)
#    def _get_run_end_time(self):
#        return self._run_end_time
#    _run_end_time = Str
#    
#    run_start_time = Property(Str)
#    def _get_run_start_time(self):
#        return self._run_start_time
#    _run_start_time = Str
#    
#    simulated_time = Property(Str)
#    def _get_simulated_time(self):
#        return self._simulated_time
#    _simulated_time = Str
#    
#    total_reactions_simulated = Property(Int)
#    def _get_total_reactions_simulated(self):
#        return self._total_reactions_simulated
#    _total_reactions_simulated = Int


class Species(HasTraits):
    index = Int
    name = Str


class Compartment(HasTraits):
#    run = Run

    index = Int
#    id = Str # not used
    name = Str
    x_position = Int
    y_position = Int
#    z_position = Int
#    template_index = Int # not used
#    creation_time = Float # not used
#    destruction_time = Float # not used

    def coordinates(self):
        return (self.x_position, self.y_position)

    def compartment_name_and_xy_coords(self):
        return "%s (%s,%s)" % (self.name, self.x_position, self.y_position)


class McssResults(HasTraits):
    '''  '''

    # exposing root._v_attrs as readonly traits

    # in McssParams

    model_input_file = Property(RelativeFile)
    def _get_model_input_file(self):
        return self._model_input_file
    _model_input_file = RelativeFile
    
    model_format = Property(ModelFormat)
    def _get_model_format(self):
        return self._model_format
    _model_format = ModelFormat

    data_file = Property(RelativeFile)
    def _get_data_file(self):
        return self._data_file
    _data_file = RelativeFile
    
    number_of_runs = Property(IntGreaterThanZero)
    def _get_number_of_runs(self):
        return self._number_of_runs
    _number_of_runs = IntGreaterThanZero
    
    simulation_algorithm = Property(SimulationAlgorithm)
    def _get_simulation_algorithm(self):
        return self._simulation_algorithm
    _simulation_algorithm = SimulationAlgorithm
    
    log_type = Property(LogType)
    def _get_log_type(self):
        return self._log_type
    _log_type = LogType
    
    log_interval = Property(FloatGreaterThanZero)
    def _get_log_interval(self):
        return self._log_interval
    _log_interval = FloatGreaterThanZero
    
    max_time = Property(FloatGreaterThanZero)
    def _get_max_time(self):
        return self._max_time
    _max_time = FloatGreaterThanZero
            
    seed = Property(Long)
    def _get_seed(self):
        return self._seed
    _seed = Long
    
    duplicate_initial_amounts = Property(Boolean)
    def _get_duplicate_initial_amounts(self):
        return self._duplicate_initial_amounts_ # returns shadow value
    _duplicate_initial_amounts = Boolean
    
    log_degraded = Property(Boolean)
    def _get_log_degraded(self):
        return self._log_degraded_ # returns shadow value
    _log_degraded = Boolean
    
    log_volumes = Property(Boolean)
    def _get_log_volumes(self):
        return self._log_volumes_ # returns shadow value
    _log_volumes = Boolean
    
    log_propensities = Property(Boolean)
    def _get_log_propensities(self):
        return self._log_propensities_ # returns shadow value
    _log_propensities = Boolean
    
    periodic_x = Property(Boolean)
    def _get_periodic_x(self):
        return self._periodic_x_ # returns shadow value
    _periodic_x = Boolean
    
    periodic_y = Property(Boolean)
    def _get_periodic_y(self):
        return self._periodic_y_ # returns shadow value
    _periodic_y = Boolean
    
    periodic_z = Property(Boolean)
    def _get_periodic_z(self):
        return self._periodic_z_ # returns shadow value
    _periodic_z = Boolean
    
    lattice_x_dimension = Property(Int)
    def _get_lattice_x_dimension(self):
        return self._lattice_x_dimension
    _lattice_x_dimension = Int
    
    lattice_y_dimension = Property(Int)
    def _get_lattice_y_dimension(self):
        return self._lattice_y_dimension
    _lattice_y_dimension = Int
    
    lattice_z_dimension = Property(Int)
    def _get_lattice_z_dimension(self):
        return self._lattice_z_dimension
    _lattice_z_dimension = Int
    
    growth_type = Property(GrowthType)
    def _get_growth_type(self):
        return self._growth_type
    _growth_type = GrowthType

    keep_divisions = Property(Boolean)
    def _get_keep_divisions(self):
        return self._keep_divisions_ # returns shadow value
    _keep_divisions = Boolean
    
    division_direction = Property(DivisionDirection)
    def _get_division_direction(self):
        return self._division_direction
    _division_direction = DivisionDirection


    view = View(
        Item('model_input_file', style='readonly'),
        Item('model_format', style='readonly'),
        Item('data_file', style='readonly'),
        Item('number_of_runs', style='readonly'),
        Item('log_type', style='readonly'),
        Item('max_time', style='readonly'),
        Item('seed', style='readonly'),
        Item('duplicate_initial_amounts', style='readonly'),
        Item('log_degraded', style='readonly'),
        Item('log_volumes', style='readonly'),
        Item('log_propensities', style='readonly'),
        HGroup(
            Item(label='Periodic boundaries'),
            Item('periodic_x', style='readonly', label='x'),
            Item('periodic_y', style='readonly', label='y'),
            Item('periodic_z', style='readonly', label='z'),
        ),
        HGroup(
            Item(label='Lattice dimensions'),
            Item('lattice_x_dimension', style='readonly', label='x'),
            Item('lattice_y_dimension', style='readonly', label='y'),
            Item('lattice_z_dimension', style='readonly', label='z'),
        ),
        Item('growth_type', style='readonly'),
        Item('keep_divisions', style='readonly'),
        Item('division_direction', style='readonly'),
        Item('number_of_rule_templates', style='readonly'),
        Item('number_of_rules_in_templates', style='readonly'),
        Item('number_of_species', style='readonly'),
        Item('simulation_end_time', style='readonly'),
        Item('simulation_start_time', style='readonly'),
        Item('total_number_of_rules', style='readonly'),
        Item('mcss_version', style='readonly'),
    )


    
    # not in McssParams
        
    mcss_version = Property(Str)
    def _get_mcss_version(self):
        return self._mcss_version
    _mcss_version = Str

    number_of_rule_templates = Property(Int)
    def _get_number_of_rule_templates(self):
        return self._number_of_rule_templates
    _number_of_rule_templates = Int
    
    number_of_rules_in_templates = Property(Int)
    def _get_number_of_rules_in_templates(self):
        return self._number_of_rules_in_templates
    _number_of_rules_in_templates = Int
    
    number_of_species = Property(IntGreaterThanZero)
    def _get_number_of_species(self):
        return self._number_of_species
    _number_of_species = IntGreaterThanZero
    
    simulation_start_time = Property(Str)
    def _get_simulation_start_time(self):
        return self._simulation_start_time
    _simulation_start_time = Str
    
    simulation_end_time = Property(Str)
    def _get_simulation_end_time(self):
        return self._simulation_end_time
    _simulation_end_time = Str
    
    total_number_of_rules = Property(Int)
    def _get_total_number_of_rules(self):
        return self._total_number_of_rules
    _total_number_of_rules = Int


    def __init__(self, h5_file_name, **traits):
        ''' Extracts metadata from H5 file and exposes it as readonly attributes.
        
        Creates lists of species and compartment objects
        
        Does *not* create run objects and compartment objects within each runs, 
        so compartment creation or destruction cannot be accounted for currently.
        
        '''
        super(HasTraits, self).__init__(**traits)
        
        h5_file = tables.openFile(h5_file_name, 'r')
        
        a = h5_file.root._v_attrs
        
        try:
            self._log_type = a.log_type

            if self.log_type.lower() != 'levels':
                raise ValueError('This version of McssResults does not handle mcss data files with log_type != levels')

            self._number_of_runs = a.number_of_runs
            self._max_time = a.max_time

            # fix number_of_runs in cases where mcss didn't close properly
            for i in range(1, self.number_of_runs + 1):
                try:
                    h5_file.root._f_getChild('run%s' % i)
                except tables.exceptions.NoSuchNodeError, error:
                    # Couldn't find run i, so overwrite number_of_runs with i - 1
                    h5_file.close() # close and open again in append mode
                    h5_file = tables.openFile(h5_file, 'r+')
                    h5_file.root._v_attrs.number_of_runs = i - 1
                    break
    
            # avoid using a truncated run (for averages)
            if self.number_of_runs > 1:
                last_run_node = h5.root._f_getChild('run%s' % self.number_of_runs)
                if last_run_node._v_attrs.simulated_time < self.max_time:
                    self.number_of_runs -= 1
                    print 'got here'

            self._model_input_file = a.model_input_file
            self._model_format = a.model_format
            self._data_file = a.data_file
            self._simulation_algorithm = a.simulation_algorithm
            self._log_interval = a.log_interval
            self._seed = a.seed
            self._duplicate_initial_amounts = a.duplicate_initial_amounts
            self._log_degraded = a.log_degraded
            self._log_volumes = a.log_volumes
            self._log_propensities = a.log_propensities
            self._periodic_x = a.periodic_x
            self._periodic_y = a.periodic_y
            self._periodic_z = a.periodic_z
            self._lattice_x_dimension = a.lattice_x_dimension
            self._lattice_y_dimension = a.lattice_y_dimension
            self._lattice_z_dimension = a.lattice_z_dimension
            self._growth_type = a.growth_type
            self._keep_divisions = a.keep_divisions
            self._division_direction = chr(a.division_direction) # convert ascii, might fail depending on encoding
                        
            self._mcss_version = a.mcss_version
            self._number_of_rule_templates = a.number_of_rule_templates
            self._number_of_rules_in_templates = a.number_of_rules_in_templates
            self._number_of_species = a.number_of_species
            self._simulation_start_time = a.simulation_start_time
            self._simulation_end_time = a.simulation_end_time
            self._total_number_of_rules = a.total_number_of_rules

            cols = h5_file.root.species_information.cols
            species_indices = cols.species_index[:]
            species_names = cols.species_name[:]
            self.species = [
                Species(
                    index=species_indices[i],
                    name=species_names[i],
                ) for i in range(self.number_of_species)
            ]
            
            cols = h5_file.root.run1.compartment_information.cols
            compartment_indices = cols.compartment_index[:]
#            compartment_ids = cols.compartment_id[:] # not used
            compartment_names = cols.compartment_name[:]
            compartment_x_positions = cols.compartment_x_position[:]
            compartment_y_positions = cols.compartment_y_position[:]
#            compartment_z_positions = cols.compartment_z_position[:] # not written by mcss despite lattice_z_dimension
#            compartment_template_indices = cols.compartment_template_index[:]
#            compartment_creation_time = cols.compartment_creation_time[:] # not used
#            compartment_destruction_time = cols.compartment_destruction_time[:] # not used
            self.compartments = [
                Compartment(
                    index=compartment_indices[i],
#                    id=compartment_ids[i], # not used
                    name=compartment_names[i],
                    x_position=compartment_x_positions[i],
                    y_position=compartment_y_positions[i],
#                    z_position=compartment_z_positions[i], # not written by mcss despite lattice_z_dimension
#                    template_index=compartment_template_indices[i], # not used
#                    creation_time=compartment_creation_time[i], # not used
#                    destruction_time=compartment_destruction_time[i], # not used
                ) for i in range(len(compartment_indices))
            ]
            
        finally:
            h5_file.close()
    
    
    species = List(Species)
    
    compartments = List(Compartment)
    

if __name__ == '__main__':
    m = McssResults('/home/jvb/dashboard/examples/modules/module1.h5')

#    print m.model_format
#    print m.log_degraded # test Property(Boolean) returns shadow value 
#    m._model_format = 'bollox' # test validator
#    m._log_degraded = 0 # test Boolean mapped trait
#    m.model_format = 'xml' # test readonly

#    m.configure_traits()
    
    print m.species
    print m.compartments    
