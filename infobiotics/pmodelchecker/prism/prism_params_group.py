from enthought.traits.ui.api import (
    VGroup, Item, HGroup, InstanceEditor, View, VSplit, Group,
)
from infobiotics.pmodelchecker.api import (
    model_parameters_group, temporal_formulas_group,
)

prism_params_group = VGroup(
    Item('model_specification', label='P system model'),
    VGroup(
        HGroup(
#            Item('handler.retranslate_prism_model', label='Retranslate', show_label=False, visible_when='handler._prism_model_str_changed'),
            Item('PRISM_model', label='PRISM model'),
            Item('handler.edit_prism_model', label='Edit', show_label=False, enabled_when='object.PRISM_model != ""'),
        ),
    ),
    Item('task'),#, emphasized=True),
    Group(
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
            label='Model parameters',
        ),
        temporal_formulas_group,
        enabled_when='object.task != "Translate"',
        layout='tabbed',
    ),
    HGroup(
        Item('handler.confidence'),
        Item('handler._custom_confidence', show_label=False, enabled_when='handler.confidence=="custom"'),
        Item('precision'),
        Item('number_samples', label='Number of samples'),
        enabled_when='object.task == "Approximate"',
    ),
    VGroup(
        Item('results_file', enabled_when='object.task in ("Approximate", "Verify")'),
        Item('states_file', enabled_when='object.task=="Build"'),
        Item('transitions_file', enabled_when='object.task=="Build"'),
    ),
)


if __name__ == '__main__':
    execfile('prism_params.py')
    