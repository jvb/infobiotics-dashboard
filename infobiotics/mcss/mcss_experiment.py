from __future__ import division
from mcss_params import McssParams
from infobiotics.core.experiment import Experiment
from enthought.traits.api import Int, Float
from infobiotics.commons.api import logging
logger = logging.getLogger(level=logging.ERROR)
import sys

class McssExperiment(McssParams, Experiment):
    
    def _handler_default(self):
        from infobiotics.mcss.api import McssExperimentHandler
        return McssExperimentHandler(model=self)
    
#    executable_kwargs = ['show_progress=false']
    executable_kwargs = ['show_progress=true']
#    
    _output_pattern_list = [
        '[0-9]+ [0-9]+', # 'time_in_run, run'
    ] 

#    stdout = sys.stdout #TODO enable redirection by scripts

    def _started_fired(self):
        if self._interaction_mode in ('terminal', 'script'):
#            import infobiotics.core.params
#            command = '%s %s %s' % (self.executable_name, self._params_file, ' '.join(['%s=%s' % (name, infobiotics.core.params.parameter_value_from_trait_value(self, name)) for name in self._dirty_parameters.keys()]))
            from progressbar import ProgressBar, Percentage, Bar, RotatingMarker, ETA
            self.progress_bar = ProgressBar(
                widgets=[
                    'mcss', #command,
                    ' ',
                    Percentage(),
                    ' ',
                    Bar(marker=RotatingMarker()),
                    ' ',
                    ETA()
                ],
                maxval=100,
            )
            self.progress_bar.start()
        
    run = Int(1)
    time_in_run = Float

    def _output_pattern_matched(self, pattern_index, match):
        if pattern_index == 0: # '20.5 1'
            time_in_run, run = match.split(' ')
            self.run = int(run)
            self.time_in_run = float(time_in_run)
            if self._interaction_mode in ('terminal', 'script'):
                percentage = int((((self.time_in_run) + ((self.run - 1) * self.max_time)) / (self.runs * self.max_time)) * 100)
                self.progress_bar.update(percentage)
        else:
            super(McssExperiment, self)._output_pattern_matched(pattern_index, match)
            
    def _finished_fired(self):
        if self._interaction_mode in ('terminal', 'script'):
            self.progress_bar.finish()
        Experiment._finished_fired(self)


def main():
    experiment = McssExperiment()
#    experiment.load('../../tests/workbench_examples/modules/module1.params')
    experiment.load('/home/jvb/src/mcss-0.0.41/examples/models/module1.params')
#    experiment.runs = 3
#    experiment.max_time = 3
#    print experiment._dirty_parameters
##    print experiment._interaction_mode
#    experiment._interaction_mode = 'terminal'
##    for name, value in experiment._clean_parameters.items(): 
##        print name, value 
##    exit()
    experiment.perform()#thread=True)
#    experiment.perform(thread=True)
##    #TODO del experiment.temp_params_file # done in Experiment._finished_fired
#    experiment.configure()

if __name__ == '__main__':
    main()
