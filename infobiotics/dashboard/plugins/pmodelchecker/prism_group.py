import os; os.environ['ETS_TOOLKIT']='qt4'

from enthought.traits.ui.api import Group, Item, VGroup, HGroup, TextEditor
from infobiotics.dashboard.plugins.pmodelchecker.temporal_formulas import *

prism_group = VGroup(

    Item('model_specification'),
    
    HGroup(
        Item('PRISM_model', label='PRISM model'),
        Item('generate_prism_model', label='Generate', show_label=False),
#        Item('_show_prism_model', label='Show'),
        Item('edit_prism_model', label='Edit', show_label=False),
    ),
    HGroup(
       Item('_prism_model_str', show_label=False, style='custom', editor=TextEditor(), enabled_when='object._show_prism_model'),
       label='PRISM_model',
    ),
    
    temporal_formulas_group,
    
    VGroup(
        HGroup(
            Item('task', emphasized=True),
        ),
        
        VGroup(
            Item('model_parameters', enabled_when='object.task == "Approximate" or object.task == "Verify"'),
        #    Item('parameters_file', label='PRISM parameters file'),
        ),
    
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
        
        label='PRISM'
    ),
)

if __name__ == '__main__':
    execfile('prism_experiment.py')