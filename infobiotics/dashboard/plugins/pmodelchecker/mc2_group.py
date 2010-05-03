import os; os.environ['ETS_TOOLKIT']='qt4'
from enthought.traits.ui.api import VGroup, Group, Item, HGroup, InstanceEditor, View
from infobiotics.dashboard.plugins.pmodelchecker.temporal_formulas import temporal_formulas_group
from infobiotics.dashboard.plugins.experiments.params_experiment import ParamsExperiment
from infobiotics.dashboard.plugins.experiments.params_experiment_handler import ParamsExperimentHandler

mc2_group = Group(
    
    Item('model_specification'),
    
    VGroup(
        HGroup(
            Item('simulations_file_hdf5', label='mcss simulation file', enabled_when='object.simulations_generatedMC2 != True'),
            Item('simulations_generatedHDF5', label='Simulated?', enabled_when='object.simulations_generatedMC2 != True'),
        ),
        HGroup(
            Item('mcss_params_file', label='mcss parameters file', enabled_when='object.simulations_generatedHDF5 != True and object.simulations_generatedMC2 != True'),
            Item('_edit__mcss_experiment', show_label=False, enabled_when='object.simulations_generatedHDF5 != True and object.simulations_generatedMC2 != True'),
        ),
        HGroup(
               Item('simulations_file_MC2', label='MC2 input file'),
               Item('simulations_generatedMC2', label='Generated?'),
        ),
        Item('number_samples', 
            label='Number of samples', 
#            enabled_when='object.simulations_generatedMC2 != True'
        ),
        label='Simulation data',
    ),

    temporal_formulas_group,   
    
    Item('results_file'),
)


if __name__ == '__main__':
    execfile('mc2_experiment.py')
    