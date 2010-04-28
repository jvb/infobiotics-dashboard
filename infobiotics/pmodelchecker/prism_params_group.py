from infobiotics.shared.api import (
    VGroup, Item, HGroup, TextEditor, InstanceEditor, View
)
from infobiotics.pmodelchecker.model_parameters import editable_modal_parameters_group
from infobiotics.pmodelchecker.temporal_formulas import temporal_formulas_group

prism_params_group = VGroup(
    VGroup(
        Item('_cwd', label='Working directory'),     
    ),
    VGroup(
        Item('model_specification', label='P system model'),
        HGroup(
            Item('PRISM_model', label='PRISM model'),
            Item('handler.generate_prism_model', label='Generate from P system', show_label=False, enabled_when='object.model_specification != ""'),
#            Item('_show_prism_model', label='Show'),
#            Item('edit_prism_model', label='Edit', show_label=False),
        ),
        Item('handler._prism_model_str', show_label=False, style='custom', editor=TextEditor(), visible_when='len(handler._prism_model_str) > 0'),#enabled_when='handler._show_prism_model'),
        label='PRISM model',
    ),
#    model_parameters_group,
    Item('model_parameters', style='custom'),
#    Item('handler._model_parameters', #TODO 
#        style='simple', 
#        show_label=False, 
#        editor=InstanceEditor(
#            label='Edit model parameters',
#            kind='live',
#            view = View(
#                editable_modal_parameters_group,
#                buttons=['OK','Cancel'],
##                resizable=True, # uncommenting this will stop button doing anything!
#            ),
#        ),
#        visible_when='len(object._model_parameters) > 0',
#    ),
    temporal_formulas_group,
    VGroup(
        HGroup(
            Item('task', emphasized=True),
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
        ),
        VGroup(
            Item('results_file', enabled_when='object.task == "Approximate" or object.task == "Verify"'),
            Item('states_file', enabled_when='object.task=="Build"'),
            Item('transitions_file', enabled_when='object.task=="Build"'),
        ),
        label='PRISM parameters'
    ),
    show_border=True,
)


if __name__ == '__main__':
    execfile('prism_params.py')
    