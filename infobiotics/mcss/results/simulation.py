'''Provides a data structure for convenient access to model information held
in an h5 file produced by mcss.'''

from run import Run
from species import Species
from compartment import Compartment
import tables

class Simulation(object): #TODO rename McssSimulation

    def __init__(self, attributes):
#        self._propensities_list = []
#        self._reactions_list = []
#        self._rules_list = []
#        self._rulesets_list = []
        self._runs_list = []
        self._species_list = []

        self.data_file = attributes.data_file
#        self.division_direction = attributes.division_direction
#        self.duplicate_initial_amounts = attributes.duplicate_initial_amounts
#        self.growth_type = attributes.growth_type
#        self.keep_divisions = attributes.keep_divisions
#        self.lattice_x_dimension = attributes.lattice_x_dimension
#        self.lattice_y_dimension = attributes.lattice_y_dimension
#        self.lattice_z_dimension = attributes.lattice_z_dimension
#        self.log_degraded = attributes.log_degraded
        self.log_interval = attributes.log_interval
#        self.log_propensities = attributes.log_propensities
        self.log_type = attributes.log_type
        self.log_volumes = attributes.log_volumes
        self.max_time = attributes.max_time
#        self.mcss_version = attributes.mcss_version
#        self.model_format = attributes.model_format
        self.model_input_file = attributes.model_input_file
#        self.number_of_rule_templates = attributes.number_of_rule_templates
#        self.number_of_rules_in_templates = attributes.number_of_rules_in_templates
        self.number_of_runs = attributes.number_of_runs
        self.number_of_species = attributes.number_of_species
#        self.periodic_x = attributes.periodic_x
#        self.periodic_y = attributes.periodic_y
#        self.periodic_z = attributes.periodic_z
#        self.seed = attributes.seed
#        self.simulation_algorithm = attributes.simulation_algorithm
#        self.simulation_algorithm_name = attributes.simulation_algorithm_name
#        self.simulation_end_time = attributes.simulation_end_time
        self.simulation_start_time = attributes.simulation_start_time
#        self.total_number_of_rules = attributes.total_number_of_rules


def load_h5(h5_file):
    """Read mcss-produced hdf5 file, creating objects for datasets, exposing 
       attributes as properties and objects as public variables.
       AttributeErrors should be caught by the loading class."""

    h5 = tables.openFile(h5_file) # get file handle

    simulation = Simulation(h5.root._v_attrs) # create simulation objects

    # rule objects in Simulation._rules_list
    # ruleset objects Simulation._ruleset_list
    # propensities in Simulation._propensities_list
    # reactions in Simulation._reactions_list
    
    # volumes to be done in SimulationResultsDialog
    
    # positions not used yet

    if simulation.log_type.lower() != 'levels':
        return # give up

    # when reading from disk to memory taking the whole slice of each column is very fast
    species_indices = h5.root.species_information.cols.species_index[:]
    species_names = h5.root.species_information.cols.species_name[:]
    simulation._species_list = [
        Species(
            species_indices[i],
            species_names[i],
            simulation,
        ) for i in range(simulation.number_of_species)
    ]

    # create run objects and compartment objects within runs
    for i in range(1, int(simulation.number_of_runs) + 1):
        try:
            node = h5.root._f_getChild('run%s' % i)
            run = Run(node._v_attrs, i, simulation)
        except tables.exceptions.NoSuchNodeError, error:
            # Couldn't find run i, so overwrite number_of_runs with i - 1
            h5.close()
            h5 = tables.openFile(h5_file, 'r+')
            h5.root._v_attrs.number_of_runs = i - 1
            simulation.number_of_runs = h5.root._v_attrs.number_of_runs
            break

        # just create compartments once on the first run #TODO maybe change this when dealing with volumes 
        if i == 1:
            cols = node.compartment_information.cols # table columns accessor
            compartment_indices = cols.compartment_index[:]
            compartment_ids = cols.compartment_id[:]
            compartment_names = cols.compartment_name[:]
            compartment_x_positions = cols.compartment_x_position[:]
            compartment_y_positions = cols.compartment_y_position[:]
#            compartment_z_positions = cols.compartment_z_position[:] # not written
            compartment_template_indices = cols.compartment_template_index[:]
#            compartment_creation_time = cols.compartment_creation_time[:] # not used
#            compartment_destruction_time = cols.compartment_destruction_time[:] # not used

            compartments_list = [ # doesn't need to be global
                Compartment(
                    compartment_indices[i],
                    compartment_ids[i],
                    compartment_names[i],
                    compartment_x_positions[i],
                    compartment_y_positions[i],
#                    compartment_z_positions[i], # not written
                    compartment_template_indices[i],
#                    compartment_creation_time[i], # not used
#                    compartment_destruction_time[i], # not used
                    run,
                    run._simulation,
                ) for i in range(0, len(compartment_indices))
            ]
        run._compartments_list = compartments_list

        simulation._runs_list.append(run)

    h5.close()
    return simulation
