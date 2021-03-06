from traits.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'qt4'
from traitsui.api import (
    VGroup, Item, HGroup, InstanceEditor, View, VSplit, Group, Spring
)
from infobiotics.pmodelchecker.model_parameters import model_parameters_group
from infobiotics.pmodelchecker.temporal_formulas import temporal_formulas_group

prism_params_group = VGroup(
    Item('model_specification', label='P system model'),
    VGroup(
        VGroup(
            HGroup(
                Item('PRISM_model', label='PRISM model'),
                Item('handler.view_prism_model', label='View', show_label=False, enabled_when='len(handler._prism_model_str) > 0')#handler._prism_model_str != ""'),
            ),
        ),
        HGroup(
            Spring(),
            Item('handler.task', emphasized=True),
            Spring(),
        ),
        Group(
            VGroup(
                Item('handler.model_parameters_object',
                    style='custom',
                    show_label=False,
                    editor=InstanceEditor(
                        label='Edit model parameters',
                        kind='live',
                        view=View(
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
            Item('handler.confidence'), #TODO TextEditor?
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
        enabled_when='object.model_specification != ""',
    ),
)


if __name__ == '__main__':
    execfile('prism_params.py')
    
