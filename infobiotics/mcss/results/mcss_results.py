from __future__ import division
#import sys
import tables
from types import SliceType
import bisect
import math
import numpy as np

from enthought.traits.api import Enum, Trait
#from enthought.traits.api import Property, Long  
from enthought.traits.api import HasTraits, Int, Str, List, ReadOnly, Array
from infobiotics.commons.traits.api import RelativeFile
#from infobiotics.commons.traits.api import FloatGreaterThanZero, IntGreaterThanZero
from enthought.traits.ui.api import View, Item, VGroup, HGroup


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


#class McssResultsAttributesProperty(HasTraits):
#    ''' Exposes root._v_attrs as Property traits '''
#
#    parameters = List(Str, 
#        [
#            'model_input_file',
#            'model_format',
#            'data_file',
#            'runs',
#            'log_type',
#            'max_time',
#            'seed',
#            'duplicate_initial_amounts',
#            'log_interval',
#            'log_degraded',
#            'log_volumes',
#            'log_propensities',
#            'growth_type',
#            'keep_divisions',
#            'division_direction',
#            'periodic_x',
#            'periodic_y',
#            'periodic_z',
#        ],
#    )
#
#    # in McssParams
#
#    _model_input_file = RelativeFile
#    model_input_file = Property(RelativeFile)
#    def _get_model_input_file(self):
#        return self._model_input_file
#    def _set_model_input_file(self):
#        sys.stderr.write("The 'model_input_file' trait of an McssResults instance is 'read only'.\n")
#    #Item('model_input_file', style='readonly'),#, label='model_input_file'),
#    
#    _model_format = ModelFormat
#    model_format = Property(ModelFormat)
#    def _get_model_format(self):
#        return self._model_format
#    def _set_model_format(self):
#        sys.stderr.write("The 'model_format' trait of an McssResults instance is 'read only'.\n")
#    #Item('model_format', style='readonly'),#, label='model_format'),
#        
#    _data_file = RelativeFile
#    data_file = Property(RelativeFile)
#    def _get_data_file(self):
#        return self._data_file
#    def _set_data_file(self):
#        sys.stderr.write("The 'data_file' trait of an McssResults instance is 'read only'.\n")
#    #Item('data_file', style='readonly'),#, label='data_file'),
#        
#    _runs = IntGreaterThanZero
#    runs = Property(IntGreaterThanZero)
#    def _get_runs(self):
#        return self._runs
#    def _set_runs(self):
#        sys.stderr.write("The 'runs' trait of an McssResults instance is 'read only'.\n")
#    #Item('runs', style='readonly'),#, label='runs'),
#        
#    _simulation_algorith = SimulationAlgorithm
#    simulation_algorith = Property(SimulationAlgorithm)
#    def _get_simulation_algorith(self):
#        return self._simulation_algorith
#    def _set_simulation_algorith(self):
#        sys.stderr.write("The 'simulation_algorith' trait of an McssResults instance is 'read only'.\n")
#    #Item('simulation_algorith', style='readonly'),#, label='simulation_algorith'),
#        
#    _log_type = LogType
#    log_type = Property(LogType)
#    def _get_log_type(self):
#        return self._log_type
#    def _set_log_type(self):
#        sys.stderr.write("The 'log_type' trait of an McssResults instance is 'read only'.\n")
#    #Item('log_type', style='readonly'),#, label='log_type'),
#        
#    _log_interval = FloatGreaterThanZero
#    log_interval = Property(FloatGreaterThanZero)
#    def _get_log_interval(self):
#        return self._log_interval
#    def _set_log_interval(self):
#        sys.stderr.write("The 'log_interval' trait of an McssResults instance is 'read only'.\n")
#    #Item('log_interval', style='readonly'),#, label='log_interval'),
#        
#    _max_time = FloatGreaterThanZero
#    max_time = Property(FloatGreaterThanZero)
#    def _get_max_time(self):
#        return self._max_time
#    def _set_max_time(self):
#        sys.stderr.write("The 'max_time' trait of an McssResults instance is 'read only'.\n")
#    #Item('max_time', style='readonly'),#, label='max_time'),
#        
#    _seed = Long
#    seed = Property(Long)
#    def _get_seed(self):
#        return self._seed
#    def _set_seed(self):
#        sys.stderr.write("The 'seed' trait of an McssResults instance is 'read only'.\n")
#    #Item('seed', style='readonly'),#, label='seed'),
#    
#    _duplicate_initial_amounts = Boolean
#    duplicate_initial_amounts = Property(Bool)
#    def _get_duplicate_initial_amounts(self):
#        return self._duplicate_initial_amounts_ # returns shadow value
##    def _set_duplicate_initial_amounts(self):
##        sys.stderr.write("The 'duplicate_initial_amounts' trait of an McssResults instance is 'read only'.\n")
#    #Item('duplicate_initial_amounts', enabled_when='False'),#, label='duplicate_initial_amounts'),
#    
#    _log_degraded = Boolean
#    log_degraded = Property(Bool)
#    def _get_log_degraded(self):
#        return self._log_degraded_ # returns shadow value
#    def _set_log_degraded(self):
#        sys.stderr.write("The 'log_degraded' trait of an McssResults instance is 'read only'.\n")
#    #Item('log_degraded', enabled_when='False'),#, label='log_degraded'),
#        
#    _log_volumes = Boolean
#    log_volumes = Property(Bool)
#    def _get_log_volumes(self):
#        return self._log_volumes_ # returns shadow value
#    def _set_log_volumes(self):
#        sys.stderr.write("The 'log_volumes' trait of an McssResults instance is 'read only'.\n")
#    #Item('log_volumes', enabled_when='False'),#, label='log_volumes'),
#        
#    _log_propensities = Boolean
#    log_propensities = Property(Bool)
#    def _get_log_propensities(self):
#        return self._log_propensities_ # returns shadow value
#    def _set_log_propensities(self):
#        sys.stderr.write("The 'log_propensities' trait of an McssResults instance is 'read only'.\n")
#    #Item('log_propensities', enabled_when='False'),#, label='log_propensities'),
#
#    _periodic_x = Boolean
#    periodic_x = Property(Bool)
#    def _get_periodic_x(self):
#        return self._periodic_x_ # returns shadow value
#    def _set_periodic_x(self):
#        sys.stderr.write("The 'periodic_x' trait of an McssResults instance is 'read only'.\n")
#    #Item('periodic_x', enabled_when='False'),#, label='periodic_x'),
#        
#    _periodic_y = Boolean
#    periodic_y = Property(Bool)
#    def _get_periodic_y(self):
#        return self._periodic_y_ # returns shadow value
#    def _set_periodic_y(self):
#        sys.stderr.write("The 'periodic_y' trait of an McssResults instance is 'read only'.\n")
#    #Item('periodic_y', enabled_when='False'),#, label='periodic_y'),
#    
#    _periodic_z = Boolean
#    periodic_z = Property(Bool)
#    def _get_periodic_z(self):
#        return self._periodic_z_ # returns shadow value
#    def _set_periodic_z(self):
#        sys.stderr.write("The 'periodic_z' trait of an McssResults instance is 'read only'.\n")
#    #Item('periodic_z', enabled_when='False'),#, label='periodic_z'),
#        
#    _lattice_x_dimension = Int
#    lattice_x_dimension = Property(Int)
#    def _get_lattice_x_dimension(self):
#        return self._lattice_x_dimension
#    def _set_lattice_x_dimension(self):
#        sys.stderr.write("The 'lattice_x_dimension' trait of an McssResults instance is 'read only'.\n")
#    #Item('lattice_x_dimension', style='readonly'),#, label='lattice_x_dimension'),
#        
#    _lattice_y_dimension = Int
#    lattice_y_dimension = Property(Int)
#    def _get_lattice_y_dimension(self):
#        return self._lattice_y_dimension
#    def _set_lattice_y_dimension(self):
#        sys.stderr.write("The 'lattice_y_dimension' trait of an McssResults instance is 'read only'.\n")
#    #Item('lattice_y_dimension', style='readonly'),#, label='lattice_y_dimension'),
#        
#    _lattice_z_dimension = Int
#    lattice_z_dimension = Property(Int)
#    def _get_lattice_z_dimension(self):
#        return self._lattice_z_dimension
#    def _set_lattice_z_dimension(self):
#        sys.stderr.write("The 'lattice_z_dimension' trait of an McssResults instance is 'read only'.\n")
#    #Item('lattice_z_dimension', style='readonly'),#, label='lattice_z_dimension'),
#        
#    _growth_type = GrowthType
#    growth_type = Property(GrowthType)
#    def _get_growth_type(self):
#        return self._growth_type
#    def _set_growth_type(self):
#        sys.stderr.write("The 'growth_type' trait of an McssResults instance is 'read only'.\n")
#    #Item('growth_type', style='readonly'),#, label='growth_type'),
#        
#    _keep_divisions = Boolean
#    keep_divisions = Property(Bool)
#    def _get_keep_divisions(self):
#        return self._keep_divisions_ # returns shadow value
#    def _set_keep_divisions(self):
#        sys.stderr.write("The 'keep_divisions' trait of an McssResults instance is 'read only'.\n")
#    #Item('keep_divisions', enabled_when='False'),#, label='keep_divisions'),
#        
#    _division_direction = DivisionDirection
#    division_direction = Property(DivisionDirection)
#    def _get_division_direction(self):
#        return self._division_direction
#    def _set_division_direction(self):
#        sys.stderr.write("The 'division_direction' trait of an McssResults instance is 'read only'.\n")
#    #Item('division_direction', style='readonly'),#, label='division_direction'),
#
#    # not in McssParams
#        
#    _mcss_version = Str
#    mcss_version = Property(Str)
#    def _get_mcss_version(self):
#        return self._mcss_version
#    def _set_mcss_version(self):
#        sys.stderr.write("The 'mcss_version' trait of an McssResults instance is 'read only'.\n")
#    #Item('mcss_version', style='readonly'),#, label='mcss_version'),
#
#    _number_of_species = IntGreaterThanZero
#    number_of_species = Property(IntGreaterThanZero)
#    def _get_number_of_species(self):
#        return self._number_of_species
#    def _set_number_of_species(self):
#        sys.stderr.write("The 'number_of_species' trait of an McssResults instance is 'read only'.\n")
#    #Item('number_of_species', style='readonly'),#, label='number_of_species'),
#            
#    _number_of_rule_templates = Int
#    number_of_rule_templates = Property(Int)
#    def _get_number_of_rule_templates(self):
#        return self._number_of_rule_templates
#    def _set_number_of_rule_templates(self):
#        sys.stderr.write("The 'number_of_rule_templates' trait of an McssResults instance is 'read only'.\n")
#    #Item('number_of_rule_templates', style='readonly'),#, label='number_of_rule_templates'),
#        
#    _number_of_rules_in_templates = Int
#    number_of_rules_in_templates = Property(Int)
#    def _get_number_of_rules_in_templates(self):
#        return self._number_of_rules_in_templates
#    def _set_number_of_rules_in_templates(self):
#        sys.stderr.write("The 'number_of_rules_in_templates' trait of an McssResults instance is 'read only'.\n")
#    #Item('number_of_rules_in_templates', style='readonly'),#, label='number_of_rules_in_templates'),
#    
#    _total_number_of_rules = Int
#    total_number_of_rules = Property(Int)
#    def _get_total_number_of_rules(self):
#        return self._total_number_of_rules
#    def _set_total_number_of_rules(self):
#        sys.stderr.write("The 'total_number_of_rules' trait of an McssResults instance is 'read only'.\n")
#    #Item('total_number_of_rules', style='readonly'),#, label='total_number_of_rules'),
#        
##    _simulation_start_time = Trait
##    simulation_start_time = Property(Trait)
##    def _get_simulation_start_time(self):
##        return self._simulation_start_time
##    def _set_simulation_start_time(self):
##        sys.stderr.write("The 'simulation_start_time' trait of an McssResults instance is 'read only'.\n")
##    #Item('simulation_start_time', style='readonly'),#, label='simulation_start_time'),
##        
##    _simulation_end_time = Trait
##    simulation_end_time = Property(Trait)
##    def _get_simulation_end_time(self):
##        return self._simulation_end_time
##    def _set_simulation_end_time(self):
##        sys.stderr.write("The 'simulation_end_time' trait of an McssResults instance is 'read only'.\n")
##    #Item('simulation_end_time', style='readonly'),#, label='simulation_end_time'),
#
#    def traits_view(self):
#        return View(
#            VGroup(
#                Item('mcss_version', style='readonly', label='mcss version'),
#                VGroup(
#                    Item('model_input_file', style='readonly', label='model_input_file'), 
#                    Item('model_format', style='readonly', label='model_format'), 
#                    Item('data_file', style='readonly', label='data_file'), 
#                    Item('runs', style='readonly', label='runs'), 
#                    Item('log_type', style='readonly', label='log_type'), 
#                    Item('max_time', style='readonly', label='max_time'), 
#                    Item('seed', style='readonly', label='seed'), 
#                    Item('duplicate_initial_amounts', enabled_when='False', label='duplicate_initial_amounts'), 
#                    Item('log_interval', style='readonly', label='log_interval'),
#                    Item('log_degraded', enabled_when='False', label='log_degraded'), 
#                    Item('log_volumes', enabled_when='False', label='log_volumes'), 
#                    Item('log_propensities', enabled_when='False', label='log_propensities'), 
#                    Item('growth_type', style='readonly', label='growth_type'), 
#                    Item('keep_divisions', enabled_when='False', label='keep_divisions'), 
#                    Item('division_direction', style='readonly', label='division_direction'), 
#                    HGroup(
##                        Item(label='Periodic boundaries'),
#                        Item('periodic_x', enabled_when='False', label='periodic_x'),#, label='x'), 
#                        Item('periodic_y', enabled_when='False', label='periodic_y'),#, label='y'), 
#                        Item('periodic_z', enabled_when='False', label='periodic_z'),#, label='z'), 
##                    ),
#                    label='Parameters',
#                ),
#                VGroup(
#                    Item('number_of_species', style='readonly'),
#                    Item('number_of_rule_templates', style='readonly'),
#                    Item('number_of_rules_in_templates', style='readonly'),
#                    Item('total_number_of_rules', style='readonly'),
#                    HGroup(
#                        Item(label='Lattice dimensions'),
#                        Item('lattice_x_dimension', style='readonly', label='x'),#, label='lattice_x_dimension'), 
#                        Item('lattice_y_dimension', style='readonly', label='y'),#, label='lattice_y_dimension'), 
##                        Item('lattice_z_dimension', style='readonly', label='z'),#, label='lattice_z_dimension'), 
#                    ),
##                    Item('simulation_end_time', style='readonly'),
##                    Item('simulation_start_time', style='readonly'),
#                    label='Properties',
#                ),
#            ),
#            resizable=True,
#            scrollable=True,
#            title=self.data_file,
#        )
#    
#    def __init__(self, h5_file_name, **traits):
#        ''' Extracts metadata from H5 file and exposes it as readonly attributes.
#        
#        Creates lists of species and compartment objects
#        
#        Does *not* create run objects and compartment objects within each runs, 
#        so compartment creation or destruction cannot be accounted for currently.
#        
#        '''
#        super(McssResultsAttributes, self).__init__(**traits)
#
#        h5_file = tables.openFile(h5_file_name, 'r')
#        
#        a = h5_file.root._v_attrs
#        
#        try:
#            self._log_type = a.log_type
#
#            if self.log_type.lower() != 'levels':
#                raise ValueError('This version of McssResults does not handle mcss data files with log_type != levels')
#
#            self._runs = a.number_of_runs
#            self._max_time = a.max_time
#
#            # fix runs in cases where mcss didn't close properly
#            for i in range(1, self.runs + 1):
#                try:
#                    h5_file.root._f_getChild('run%s' % i)
#                except tables.exceptions.NoSuchNodeError, error:
#                    # Couldn't find run i, so overwrite runs with i - 1
#                    h5_file.close() # close and open again in append mode
#                    h5_file = tables.openFile(h5_file, 'r+')
#                    h5_file.root._v_attrs.number_of_runs = i - 1
#                    break
#    
#            # avoid using a truncated run (for averages)
#            last_run_node = h5_file.root._f_getChild('run%s' % self.runs)
#            if last_run_node._v_attrs.simulated_time < self.max_time:
#                if self.runs > 1:
#                    self._runs -= 1
#                else:
#                    self._max_time = last_run_node._v_attrs.simulated_time
#
#            self._model_input_file = a.model_input_file
#            self._model_format = a.model_format
#            self._data_file = a.data_file
#            self._simulation_algorithm = a.simulation_algorithm
#            self._log_interval = a.log_interval
#            self._seed = a.seed
#            self._duplicate_initial_amounts = a.duplicate_initial_amounts
#            self._log_degraded = a.log_degraded
#            self._log_volumes = a.log_volumes
#            self._log_propensities = a.log_propensities
#            self._periodic_x = a.periodic_x
#            self._periodic_y = a.periodic_y
#            self._periodic_z = a.periodic_z
#            self._lattice_x_dimension = a.lattice_x_dimension
#            self._lattice_y_dimension = a.lattice_y_dimension
#            self._lattice_z_dimension = a.lattice_z_dimension
#            self._growth_type = a.growth_type
#            self._keep_divisions = a.keep_divisions
#            self._division_direction = chr(a.division_direction) # convert ascii, might fail depending on encoding
#                        
#            self._mcss_version = a.mcss_version
#            self._number_of_species = a.number_of_species
#            self._number_of_rule_templates = a.number_of_rule_templates
#            self._number_of_rules_in_templates = a.number_of_rules_in_templates
#            self._total_number_of_rules = a.total_number_of_rules
##            self._simulation_start_time = a.simulation_start_time
##            self._simulation_end_time = a.simulation_end_time
#            
#        finally:
#            h5_file.close()


class McssResultsAttributesReadOnly(HasTraits):
    ''' Exposes root._v_attrs as ReadOnly traits '''

    parameters = List(Str, 
        [
            'model_input_file',
            'model_format',
            'data_file',
            'runs',
            'log_type',
            'max_time',
            'seed',
            'duplicate_initial_amounts',
            'log_interval',
            'log_degraded',
            'log_volumes',
            'log_propensities',
            'growth_type',
            'keep_divisions',
            'division_direction',
            'periodic_x',
            'periodic_y',
            'periodic_z',
        ],
    )

    # in McssParams
    
    log_type = ReadOnly
    runs = ReadOnly
    max_time = ReadOnly
    model_input_file = ReadOnly
    model_format = ReadOnly
    data_file = ReadOnly
    simulation_algorithm = ReadOnly
    log_interval = ReadOnly
    seed = ReadOnly
    duplicate_initial_amounts = ReadOnly
    log_degraded = ReadOnly
    log_volumes = ReadOnly
    log_propensities = ReadOnly
    periodic_x = ReadOnly
    periodic_y = ReadOnly
    periodic_z = ReadOnly
    growth_type = ReadOnly
    keep_divisions = ReadOnly
    division_direction = ReadOnly
                
    # not in McssParams
                
    mcss_version = ReadOnly
    number_of_species = ReadOnly
    number_of_rule_templates = ReadOnly
    number_of_rules_in_templates = ReadOnly
    total_number_of_rules = ReadOnly
    lattice_x_dimension = ReadOnly
    lattice_y_dimension = ReadOnly
    lattice_z_dimension = ReadOnly
#    simulation_start_time = ReadOnly
#    simulation_end_time = ReadOnly

    def traits_view(self): 
        return View(
            VGroup(
                Item('mcss_version', style='readonly', label='mcss version'),
                VGroup(                
                    Item('log_type', style='readonly', label='log_type'),
                    Item('runs', style='readonly', label='runs'),
                    Item('max_time', style='readonly', label='max_time'),
                    Item('model_input_file', style='readonly', label='model_input_file'),
                    Item('model_format', style='readonly', label='model_format'),
                    Item('data_file', style='readonly', label='data_file'),
                    Item('simulation_algorithm', style='readonly', label='simulation_algorithm'),
                    Item('log_interval', style='readonly', label='log_interval'),
                    Item('seed', style='readonly', label='seed'),
                    Item('duplicate_initial_amounts', style='readonly', label='duplicate_initial_amounts'),
                    Item('log_degraded', style='readonly', label='log_degraded'),
                    Item('log_volumes', style='readonly', label='log_volumes'),
                    Item('log_propensities', style='readonly', label='log_propensities'),
                    Item('periodic_x', style='readonly', label='periodic_x'),
                    Item('periodic_y', style='readonly', label='periodic_y'),
                    Item('periodic_z', style='readonly', label='periodic_z'),
                    Item('lattice_x_dimension', style='readonly', label='lattice_x_dimension'),
                    Item('lattice_y_dimension', style='readonly', label='lattice_y_dimension'),
                    Item('lattice_z_dimension', style='readonly', label='lattice_z_dimension'),
                    Item('growth_type', style='readonly', label='growth_type'),
                    Item('keep_divisions', style='readonly', label='keep_divisions'),
                    Item('division_direction', style='readonly', label='division_direction'),
                    label='Parameters',
                ),
                VGroup(                    
                    Item('number_of_species', style='readonly'),
                    Item('number_of_rule_templates', style='readonly'),
                    Item('number_of_rules_in_templates', style='readonly'),
                    Item('total_number_of_rules', style='readonly'),
                    HGroup(
                        Item(label='Lattice dimensions'),
                        Item('lattice_x_dimension', style='readonly', label='x'),#, label='lattice_x_dimension'), 
                        Item('lattice_y_dimension', style='readonly', label='y'),#, label='lattice_y_dimension'), 
#                        Item('lattice_z_dimension', style='readonly', label='z'),#, label='lattice_z_dimension'), 
                    ),
#                    Item('simulation_end_time', style='readonly'),
#                    Item('simulation_start_time', style='readonly'),
                    label='Properties',
                ),
            ),
            resizable=True,
            scrollable=True,
            title=self.data_file,
        )
        
    number_of_timepoints = ReadOnly
    
    def __init__(self, h5_file_name, **traits):
        ''' Extracts metadata from H5 file and exposes it as readonly attributes.
        
        Creates lists of species and compartment objects
        
        Does *not* create run objects and compartment objects within each runs, 
        so compartment creation or destruction cannot be accounted for currently.
        
        '''
        super(McssResultsAttributesReadOnly, self).__init__(**traits)

        h5_file = tables.openFile(h5_file_name, 'r')
        
        a = h5_file.root._v_attrs
        
        try:
            self.log_type = a.log_type

            if self.log_type.lower() != 'levels':
                raise ValueError('This version of McssResults does not handle mcss data files with log_type != levels')

            runs = a.number_of_runs
            max_time = a.max_time

            # fix runs in cases where mcss didn't close properly
            for i in range(1, int(runs) + 1):
                try:
                    h5_file.root._f_getChild('run%s' % i)
                except tables.exceptions.NoSuchNodeError, error:
                    # Couldn't find run i, so overwrite runs with i - 1
                    h5_file.close() # close and open again in append mode
                    h5_file = tables.openFile(h5_file, 'r+')
                    h5_file.root._v_attrs.number_of_runs = i - 1
                    break
    
            # avoid using a truncated run (for averages)
            a2 = h5_file.root._f_getChild('run%s' % int(runs))._v_attrs
            if a2.simulated_time < max_time:
                if runs > 1:
                    runs -= 1
                else:
                    max_time = a2.simulated_time
                    self.number_of_timepoints = a2.number_of_timepoints
            else:
                self.number_of_timepoints = h5_file.root.run1._v_attrs.number_of_timepoints

            self.runs = int(runs)
            self.max_time = max_time

            self.model_input_file = a.model_input_file
            self.model_format = a.model_format
            self.data_file = a.data_file
            self.simulation_algorithm = a.simulation_algorithm
            self.log_interval = a.log_interval
            self.seed = a.seed
            self.duplicate_initial_amounts = a.duplicate_initial_amounts
            self.log_degraded = a.log_degraded
            self.log_volumes = a.log_volumes
            self.log_propensities = a.log_propensities
            self.periodic_x = a.periodic_x
            self.periodic_y = a.periodic_y
            self.periodic_z = a.periodic_z
            self.lattice_x_dimension = a.lattice_x_dimension
            self.lattice_y_dimension = a.lattice_y_dimension
            self.lattice_z_dimension = a.lattice_z_dimension
            self.growth_type = a.growth_type
            self.keep_divisions = a.keep_divisions
            self.division_direction = chr(a.division_direction) # convert ascii, might fail depending on encoding
                        
            self.mcss_version = a.mcss_version
            self.number_of_species = a.number_of_species
            self.number_of_rule_templates = a.number_of_rule_templates
            self.number_of_rules_in_templates = a.number_of_rules_in_templates
            self.total_number_of_rules = a.total_number_of_rules
#            self.simulation_start_time = a.simulation_start_time
#            self.simulation_end_time = a.simulation_end_time
            
        finally:
            h5_file.close()    


class McssResults(McssResultsAttributesReadOnly):
    
    h5_file_name = RelativeFile
    
    species = List(Species)
    
    compartments = List(Compartment)

    def __init__(self, h5_file_name, **traits):
        ''' Extracts metadata from H5 file and exposes it as readonly attributes.
        
        Creates lists of species and compartment objects
        
        Does *not* create run objects and compartment objects within each runs, 
        so compartment creation or destruction cannot be accounted for currently.
        
        '''
        super(McssResults, self).__init__(h5_file_name, **traits)

        self.h5_file_name = h5_file_name
                
        h5_file = tables.openFile(h5_file_name, 'r')

        try:
            
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
            
        self._timepoints = np.linspace(0, self.max_time, self.number_of_timepoints)

    _timepoints = Array

    def timepoints(self, start, stop=-1, step=1):
        '''  Returns a list of (inclusive) timepoints given start and stop indices and a step/stride '''
        
        if isinstance(start, SliceType):
            return self._timepoints[start]
        
        if start < 0:
            start = 0
        elif start > len(self._timepoints) - 1:
            start = len(self._timepoints) - 1
        
        if stop < 0 or stop > len(self._timepoints):
            stop = len(self._timepoints)
        
        if step > stop:
            step = stop - start
        if step < 1:
            step = 1
        
        return self._timepoints[start:stop+1:step] 

    def timepoint_indices(self, beginning, end, every=-1):
        slice = self.timepoint_slice(beginning, end, every)
        return np.arange(slice.start, slice.stop, slice.step)
        
    def timepoint_slice(self, beginning, end, every=-1):
        ''' beginning, end and every are times,  start, stop and step are indices '''

        if beginning < 0:
            beginning = 0

        if self._timepoints[0] < beginning < self._timepoints[-1]:
            # make start the index of the timepoint closest to, and including, beginning
            start = bisect.bisect_left(self._timepoints, math.floor(beginning))
        else:
            # make start the index of the first timepoint
            start = 0

        if end < beginning:
            end = self._timepoints[0] - 1
        if self._timepoints[0] < end < self._timepoints[-1]:
            # make stop the index of the timepoint closest to, and including, end
            stop = bisect.bisect_right(self._timepoints, math.ceil(end))
        else:
            # make stop the index of the final timepoint + 1
            stop = len(self._timepoints)

        if every > end:
            every = end - beginning
        if every < self.log_interval:
            every = self.log_interval
        if every == self.log_interval:
            step = 1
        else:
            step = int(every // self.log_interval) #TODO better rounding?

        return slice(start, stop, step)
    
    def species(self, indices):
        pass
    
    def species_indices(self, *names):
        if len(names) == 1 and isinstance(names[0], (tuple, list)):
            names = names[0]
        return [species.index for name in names for species in self.species if species.name == name]
    
    def species_names(self, pattern='', case_sensitive=True, regex=False):
#        if pattern == '':
#            return [species.name for species in self.species]
#        import re
#        if regex:
#            if not case_sensitive:
#                return [species.name for species in self.species if re.search(pattern, species.name, re.IGNORECASE) != None]
#            else:
#                return [species.name for species in self.species if re.search(pattern, species.name) != None] 
#        else:
#            import fnmatch
#            if not case_sensitive:
#                return [species.name for species in self.species if re.search(fnmatch.translate(pattern), species.name, re.IGNORECASE) != None]
#            else:
#                return [species.name for species in self.species if re.search(fnmatch.translate(pattern), species.name) != None]
        return filter(self.species, 'name', pattern, case_sensitive, regex)
            
def filter(l, a, pattern='', case_sensitive=True, regex=False):
    ''' Return a subset of the a collection (l) whose item's string 
    attribute (a) matches 'pattern'. 
    
    Uses Unix shell-style wildcards when regex False.
    
    '''
    if pattern == '':
        return [getattr(i, a) for i in l]
    import re
    if regex:
        if not case_sensitive:
            return [getattr(i, a) for i in l if re.search(pattern, getattr(i, a), re.IGNORECASE) != None]
        else:
            return [getattr(i, a) for i in l if re.search(pattern, getattr(i, a)) != None] 
    else:
        import fnmatch
        if not case_sensitive:
            return [getattr(i, a) for i in l if re.search(fnmatch.translate(pattern), getattr(i, a), re.IGNORECASE) != None]
        else:
            return [getattr(i, a) for i in l if re.search(fnmatch.translate(pattern), getattr(i, a)) != None]
        
    
    
    

if __name__ == '__main__':
#    m = McssResults('/home/jvb/dashboard/examples/modules/module1-run2truncated.h5') # OK
#    m = McssResults('/home/jvb/dashboard/examples/modules/module1-run1truncated.h5') #TODO handle new max_time not completely divisible by log_interval
#    m = McssResults('/home/jvb/dashboard/examples/modules/module1.h5') # OK
    m = McssResults('/home/jvb/Desktop/pulseGenerator/_pulsePropagation.h5')

#    print m.species_indices(m.species_names())
#    print m.species_names('A', regex=True)
    assert m.species_names('*GFP', regex=False) == m.species_names('.*GFP$', regex=True) 
    assert m.species_names('*GFP*', regex=False) == m.species_names('.*GFP', regex=True)
    assert m.species_names('*GFP', regex=False, case_sensitive=True) == m.species_names('*gfp', regex=False, case_sensitive=False)
    print m.species_names('*GFP', regex=False, case_sensitive=True)
    print m.species_names('*gfp', regex=False, case_sensitive=False)
#    print m.model_format
#    print m.log_degraded # test Property(Boolean) returns shadow value 
#    m._model_format = 'bollox' # test validator
#    m._log_degraded = 0 # test Boolean mapped trait
#    m.model_format = 'xml' # test readonly

#    m.configure_traits()
    
#    print m.species
#    print m.compartments
    
#    for s in m.species:
#        print s.index, s.name
#        
#    for c in m.compartments:
#        print c.index, c.name, c.coordinates()
            
#    m.timepoint_indices(0, m.max_time, 1)
#    m.timepoint_indices(-100, m.max_time, 1)
#    m.timepoint_indices(0, m.max_time+100, 1)
#    m.timepoint_indices(0, m.max_time, 4)
#    m.timepoint_indices(0, m.max_time, 0.5)
#    m.timepoint_indices(100, 200, 1)
#    m.timepoint_indices(100, 200, 5)
#    m.timepoint_indices(100, 200, 6)
#    m.timepoint_indices(100, 200, 7)
#    print len(m.timepoint_indices(100, 200, 8)), m.timepoint_indices(100, 200, 8)
    
#    print m.timepoints(3000,1801,1)    
#    print m.timepoints(-100,3000,2)
        
#    indices = m.timepoint_indices(100, 150, 1) 
#    print indices
#    print m._timepoints[indices]
#    slice = m.timepoint_slice(100, 150, 1)
#    print m.timepoints(slice)
#    print m.timepoints(100, 150, 1)

    #TODO implement all of these as unit tests
    