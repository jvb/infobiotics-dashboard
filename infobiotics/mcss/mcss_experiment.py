from __future__ import division
from mcss_params import McssParams
from infobiotics.common.api import Experiment
from enthought.traits.api import Int, Float

class McssExperiment(McssParams, Experiment):
    
    def _handler_default(self):
        from infobiotics.mcss.api import McssExperimentHandler
        return McssExperimentHandler(model=self)
    
    executable_kwargs = ['show_progress=true']#, 'max_time=333', 'runs=66'] # testing
    _output_pattern_list = [
        '[0-9]+ [0-9]+', # 'time_in_run, run'
    ] 

    # output pattern traits
    run = Int(1)
    time_in_run = Float

#    @profile
    def _output_pattern_matched(self, pattern_index, match):
        if pattern_index == 0: # '1 20.5'
            time_in_run, run = match.split(' ')
            self.run = int(run)
            self.time_in_run = float(time_in_run) 
        else:
            super(McssExperiment, self).pattern_matched(pattern_index, match)


if __name__ == '__main__':
    McssExperiment().configure()
