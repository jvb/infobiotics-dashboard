from __future__ import division
from mcsscmaes_params import McssCmaesParams
from infobiotics.core.experiment import Experiment
from enthought.traits.api import Int, Float

class McssCmaesExperiment(McssCmaesParams, Experiment):
    
    def _handler_default(self):
        from infobiotics.mcsscmaes.api import McssCmaesExperimentHandler
        return McssCmaesExperimentHandler(model=self)
    
    executable_kwargs = ['show_progress=false']
#    executable_kwargs = ['show_progress=true']
#    
#    _output_pattern_list = [
#        '[0-9]+ [0-9]+', # 'time_in_run, run'
#    ] 
#
#    def _output_pattern_matched(self, pattern_index, match):
#        if pattern_index == 0: # '1 20.5'
#            time_in_run, run = match.split(' ')
#            self.run = int(run)
#            self.time_in_run = float(time_in_run)
#        else:
#            super(McssCmaesExperiment, self)._output_pattern_matched(pattern_index, match)
#            
#    run = Int(1)
#    time_in_run = Float


if __name__ == '__main__':
    experiment = McssCmaesExperiment()
    experiment.load('~/src/mcss-0.0.41/examples/mcss-cmaes/mcss-cmaes-01.cmaes.params')
    experiment.configure()
