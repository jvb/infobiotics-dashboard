from enthought.traits.ui.api import Group, Item, VGroup, HGroup
from infobiotics.pmodelchecker.api import temporal_formulas_group

mc2_params_group = VGroup(
    Item('model_specification'),
    HGroup(
        Item('simulations_file_hdf5', label='mcss simulation file'),
        Item('simulations_generatedHDF5', label='Simulated?'),
        enabled_when='not object.simulations_generatedMC2',
    ),
    HGroup(
        Item('mcss_params_file', label='mcss parameters file'),
        Item('handler.edit_mc2_mcss_experiment', label='&Edit', show_label=False, enabled_when='handler._mc2_mcss_experiment is not None'),
        enabled_when='not object.simulations_generatedHDF5 and not object.simulations_generatedMC2',
    ),
    HGroup(
           Item('simulations_file_MC2', label='MC2 input file'),
           Item('simulations_generatedMC2', label='Generated?'),
    ),
    Item('number_samples', 
        label='Number of samples', 
    ),
    temporal_formulas_group,   
    Item('results_file'),
)


if __name__ == '__main__':
    execfile('mc2_params.py')
    