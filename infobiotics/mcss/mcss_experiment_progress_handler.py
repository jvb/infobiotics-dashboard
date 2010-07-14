from __future__ import division
from infobiotics.common.api import ExperimentProgressHandler
from enthought.traits.api import on_trait_change

class McssExperimentProgressHandler(ExperimentProgressHandler):

    def _message_default(self):
        return 'Simulating %s' % self.model.model_file

#    max = 100 # defaults to zero
    
    @on_trait_change('model.time_in_run, model.runs, model.max_time')
    def update_progress(self):
        self.progress = int((((self.model.time_in_run) + ((self.model.run - 1) * self.model.max_time)) / (self.model.max_time * self.model.runs)) * 100)
        

if __name__ == '__main__':
    execfile('mcss_experiment.py')
    