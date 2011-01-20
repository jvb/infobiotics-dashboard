from __future__ import division
from infobiotics.core.experiment_progress_handler import ExperimentProgressHandler
from enthought.traits.api import on_trait_change

class McssExperimentProgressHandler(ExperimentProgressHandler):

#    @on_trait_change('progress')
#    def update_message(self):
#        if self.progress < self.max:
#            self.message = 'Simulating %s' % self.model.model_file
#        else:
#            self.message = "Loading results '%s'" % self.model.data_file
#
#    max = 100 # defaults to zero
#    
#    show_time = True
#    
    @on_trait_change('model.time_in_run, model.runs, model.max_time')
    def update_progress(self):
        self.progress = int((((self.model.time_in_run) + ((self.model.run - 1) * self.model.max_time)) / (self.model.max_time * self.model.runs)) * 100)
        print self.progress

if __name__ == '__main__':
    execfile('mcss_experiment.py')
    
