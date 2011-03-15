from enthought.traits.ui.api import Group, Item, VGroup, HGroup, RangeEditor
from infobiotics.pmodelchecker.temporal_formulas import temporal_formulas_group

mc2_params_group = VGroup(
    Item('model_specification'),
    HGroup(
        Item('simulations_file_hdf5', label='mcss simulation file'),
        Item('simulations_generatedHDF5', label='Simulated?'),
        enabled_when='not object.simulations_generatedMC2',
    ),
    HGroup(
        # even though there is duplication we have to set enabled_when for these 
        # individually because the HGroup's enabled_when overrides the 
        # individual conditions
        Item('mcss_params_file',
             label='mcss parameters file',
             enabled_when='not object.simulations_generatedHDF5 and not object.simulations_generatedMC2'),
        Item('handler.edit_mc2_mcss_experiment', label='&Edit', show_label=False, enabled_when='object.mcss_params_file != "" and not object.simulations_generatedHDF5 and not object.simulations_generatedMC2'),
    ),
    HGroup(
           Item('simulations_file_MC2', label='MC2 input file'),
           Item('simulations_generatedMC2', label='Generated?'),
    ),
    Item('number_samples',
        label='Number of samples',
        visible_when='not handler.number_of_runs_read',
    ),
    Item('handler.number_samples_when_simulation_file_supplied',
        label='Number of samples',
        visible_when='handler.number_of_runs_read',
        editor=RangeEditor(
            auto_set=True,
            high_name='handler.max_number_samples',
            low=1,
        ),
    ),
    temporal_formulas_group,
    Item('results_file'),
)


if __name__ == '__main__':
    execfile('mc2_params.py')
    
