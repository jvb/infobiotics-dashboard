from __future__ import division
from infobiotics.common.api import ExperimentProgressHandler
from infobiotics.commons.traits.api import Percentage
from enthought.traits.api import Property, property_depends_on

class McssExperimentProgressHandler(ExperimentProgressHandler):
    
#    progress = Property(Percentage)
    
    @property_depends_on('model.time_in_run, model.runs, model.max_time')#, model.run')
    def _get_progress(self):
        percentage = int((((self.model.time_in_run) + ((self.model.run - 1) * self.model.max_time)) / (self.model.max_time * self.model.runs)) * 100) 
        return percentage
        
    def object_finished_changed(self, info):
        self._on_close(info)


if __name__ == '__main__':
    execfile('mcss_experiment.py')
    