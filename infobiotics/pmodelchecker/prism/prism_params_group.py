from infobiotics.shared.api import (
    VGroup, Item, HGroup, InstanceEditor, View, VSplit
)
from infobiotics.pmodelchecker.api import model_parameters_group
from infobiotics.pmodelchecker.api import temporal_formulas_group

prism_params_group = VGroup(
    VGroup(
        Item('_cwd', label='Working directory'),     
    ),
    Item('model_specification', label='P system model'),
    VGroup(
        HGroup(
            Item('handler.retranslate_prism_model', label='Retranslate', show_label=False, visible_when='handler._prism_model_str_changed'),
            Item('PRISM_model', label='PRISM model'),
            Item('handler.edit_prism_model', label='Edit', show_label=False, enabled_when='object.PRISM_model != ""'),
        ),
    ),
    
    VGroup(
        Item(label='Molecule constants:'),#'Model parameters: (double-click to edit)'),
        Item('handler._model_parameters', 
            style='custom',
            show_label=False, 
            editor=InstanceEditor(
                label='Edit model parameters',
                kind='live',
                view = View(
                    model_parameters_group,
                ),
            ),
        ),
    ),
    
    temporal_formulas_group,

    VGroup(
        HGroup(
            Item('task'),#, emphasized=True),
        ),
#        VGroup(
#            Item('model_parameters', enabled_when='object.task == "Approximate" or object.task == "Verify"'),
#        #    Item('parameters_file', label='PRISM parameters file'),
#        ),
        HGroup(
            Item('handler.confidence', enabled_when='object.task=="Approximate"'),
            Item('handler._custom_confidence', show_label=False, enabled_when='handler.confidence=="custom"'),
            Item('precision', enabled_when='object.task=="Approximate"'),
            Item('number_samples', label='Number of samples', enabled_when='object.task=="Approximate"'),
            enabled_when='task != "Translate"',
        ),
        VGroup(
            Item('results_file', enabled_when='object.task == "Approximate" or object.task == "Verify"'),
            Item('states_file', enabled_when='object.task=="Build"'),
            Item('transitions_file', enabled_when='object.task=="Build"'),
        ),
#        label='PRISM parameters'
    ),
    show_border=True,
)


if __name__ == '__main__':
    execfile('prism_params.py')
    