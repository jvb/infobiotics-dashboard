from traits.api import HasTraits, List, Button
from experiment_progress_item import ExperimentProgressItem
from traitsui.api import View, Item, ListEditor

class ExperimentQueue(HasTraits):
    experiment_progress_items = List(ExperimentProgressItem)
    hidden_experiment_progress_items = List(ExperimentProgressItem)
    show_hidden_experiments = Button
    
    def _show_hidden_experiments_fired(self):
        for experiment_progress_item in self.hidden_experiment_progress_items:
            self.experiment_progress_items.append(experiment_progress_item)
        del self.hidden_experiment_progress_items[:]

    def hide_function(self, experiment_progress_item):
        self.hidden_experiment_progress_items.append(self.experiment_progress_items.pop(self.experiment_progress_items.index(experiment_progress_item)))

    traits_view = View(
        Item('show_hidden_experiments',
            label='Show hidden experiments',
            show_label=False,
            visible_when='len(object.hidden_experiment_progress_items) > 0',
        ),
        
        Item('experiment_progress_items', 
            show_label=False,
            style='readonly',
            editor=ListEditor(style='custom'),
        ),
#
#        width=640, height=480,
#        resizable=True,
#
#        title='Experiments',
    )
