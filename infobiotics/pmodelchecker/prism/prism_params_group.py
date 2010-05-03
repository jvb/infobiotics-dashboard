from enthought.traits.ui.api import (
    VGroup, Item, HGroup, InstanceEditor, View, VSplit, Group, Spring
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
            Item('handler.edit_prism_model', label='View', show_label=False, enabled_when='object.PRISM_model != ""'),
        ),
    ),
    HGroup(
        Spring(),
        Item('task', emphasized=True),
        Spring(),
    ),
    Group(
        VGroup(
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
        Group(
            temporal_formulas_group,
            label='Temporal Formulas',
            enabled_when='object.task != "Build"',
        ),
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
        Item('states_file', enabled_when='object.task in ("Build", "Verify")'),
        Item('transitions_file', enabled_when='object.task in ("Build", "Verify")'),
    ),
)


if __name__ == '__main__':
    execfile('prism_params.py')
    