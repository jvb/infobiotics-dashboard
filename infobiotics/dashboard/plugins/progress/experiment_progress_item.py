from enthought.traits.api import Instance, Button
from enthought.traits.ui.api import View, Item, HGroup
from progress_item import ProgressItem
from enthought.pyface.confirmation_dialog import confirm
from experiment import Experiment

class ExperimentProgressItem(ProgressItem):
    
    experiment = Instance(Experiment, Experiment())

    view_parameters = Button
    view_output = Button
    view_results = Button
    
    hide_condition = 'object.hide_function is not None and object.hidden == False and (object.finished or object.cancelled)'
    
    def additional_buttons(self):
        return HGroup(
            Item('view_parameters',
                label='View parameters',
                show_label=False,
            ),
            Item('view_output',
                label='View output',
                show_label=False,
#                visible_when='object.experiment.has_output',
                enabled_when='object.experiment.has_output',
            ),
            Item('view_results',
                label='View results',
                show_label=False,
                enabled_when='object.experiment.has_results'
            ),
        )
        
    def _view_parameters_fired(self):
        self.experiment.edit_traits(kind='nonmodal')        
    
    def _view_output_fired(self): pass #TODO
    
    def _view_results_fired(self): pass #TODO
    
    
    def _start_function_default(self):
        def start(self):
#            from enthought.pyface.timer.timer import Timer
#            self.timer = Timer(100, lambda: self.update_progress(self.value+1))
            return True
        return start

    def _pause_function_default(self):
        def pause(self):
            self.timer.Stop()
            return True            
        return pause
    
    def _continue_function_default(self):
        def continue_(self):
            self.timer.Start()
            return True            
        return continue_
    
    def _cancel_function_default(self):
        def cancel(self):
            self.timer.Stop()
            return True
        return cancel
    
    def _retry_function_default(self):
        def retry(self):
            if confirm(self.progress_bar, 'Retrying the experiment may overwrite existing results.\nAre you sure want to retry?'):
                self.start = True
                return True
            else:
                return False
        return retry

    def _finished_function_default(self):
        def finished(self):
            self.timer.Stop()
#            self._text = '%s%s' %(self.text, self.finished_text)
            return True
        return finished
