from __future__ import division
from infobiotics.common.api import ExperimentProgressHandler
from commons.traits.api import Percentage
from enthought.traits.api import Property, property_depends_on
from enthought.traits.ui.api import ProgressEditor, View, Item

class McssExperimentProgressHandler(ExperimentProgressHandler):
    
    progress = Property(Percentage)
    
    @property_depends_on('model.time_in_run, model.runs, model.max_time')#, model.run')
    def _get_progress(self):
        return int((((self.model.time_in_run) + ((self.model.run - 1) * self.model.max_time)) / (self.model.max_time * self.model.runs)) * 100) 
        
    def object_finished_changed(self, info):
        self._on_close(info)

#    traits_view = View(
#        Item('progress', 
##            editor=ProgressEditor(
##                title='title',
##                min=0,
##                max=100,
##                message='message',
##                can_cancel=True,
##            #    can_ok=False,
##                show_time=True,
##                show_percent=True,
##            ),
#        ),
#    )


if __name__ == '__main__':
    execfile('mcss_experiment.py')
    