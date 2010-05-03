from infobiotics.dashboard.plugins.experiments.params_experiment_handler import ParamsExperimentHandler
from enthought.traits.api import Tuple, Instance
from model_parameters import ModelParameter, editable_modal_parameters_group#model_parameters_group, 
from enthought.traits.ui.table_column import ObjectColumn
            
class PRISMExperimentHandler(ParamsExperimentHandler):
    title = 'PModelChecker (PRISM)'
    def traits_view(self):
        return View(
#            'file',
            prism_group,
            Item('handler.problem', style='readonly', emphasized=True, visible_when='handler.problem != ""'),
            buttons=['Cancel', 'Undo', 'Revert'] + self.load_save_perform_actions,
            resizable=True,
#            scrollable=True, #FIXME
            title=self.title,
        )


from enthought.traits.ui.api import VGroup, HGroup, TextEditor, InstanceEditor
from infobiotics.dashboard.plugins.pmodelchecker.temporal_formulas import *

prism_group = VGroup(
    Item('model_specification'),
    HGroup(
        Item('PRISM_model', label='PRISM model'),
        Item('generate_prism_model', label='Generate', show_label=False),
#        Item('_show_prism_model', label='Show'),
#        Item('edit_prism_model', label='Edit', show_label=False),
    ),
    VGroup(
       Item('_prism_model_str', show_label=False, style='custom', editor=TextEditor(), enabled_when='object._show_prism_model'),
       label='PRISM model',
    ),
#    model_parameters_group,
#    Item('_model_parameters', style='custom'),
    Item('_model_parameters', 
        style='simple', 
        show_label=False, 
        editor=InstanceEditor(
            label='Edit model parameters',
            kind='live',
            view = View(
                editable_modal_parameters_group,
                buttons=['OK','Cancel'],
#                resizable=True, # uncommenting this will stop button doing anything!
            ),
        ),
        visible_when='len(object._model_parameters) > 0',
    ),
    temporal_formulas_group,
    VGroup(
        HGroup(Item('task', emphasized=True),),
#        VGroup(
#            Item('model_parameters', enabled_when='object.task == "Approximate" or object.task == "Verify"'),
#        #    Item('parameters_file', label='PRISM parameters file'),
#        ),
        HGroup(
            Item('confidence', enabled_when='object.task=="Approximate"'),
            Item('_custom_confidence', show_label=False, enabled_when='object.confidence=="custom"'),
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
)
        
if __name__ == '__main__':
    execfile('prism_experiment.py')
