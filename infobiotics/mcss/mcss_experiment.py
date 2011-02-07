from __future__ import division
from mcss_params import McssParams
from infobiotics.core.experiment import Experiment
from enthought.traits.api import Int, Float
from infobiotics.commons.traits.api import Percentage

class McssExperiment(McssParams, Experiment):
    
    def __handler_default(self):
        from infobiotics.mcss.api import McssExperimentHandler
        return McssExperimentHandler(model=self)
    
    executable_kwargs = [
        'show_progress=true', # print time and run to stdout 
        'progress_interval=1', # every 1 seconds
    ]

    _stdout_pattern_list = [
#        '0 1', # fixed in mcss
        '[0-9]+ [0-9]+', # 'time_in_run, run'
    ] 

    run = Int(1)
    time_in_run = Float

    _progress_percentage = Percentage
    
#    def __progress_percentage_changed(self, value):
#        print value
    
    def _stdout_pattern_matched(self, pattern_index, match):
        # parse stdout into percentage
        if pattern_index == 0:
#            pass
#        elif pattern_index == 1:
            time_in_run, run = match.split(' ')
            run = int(run)
            time_in_run = float(time_in_run)
            self._progress_percentage = int((((time_in_run) + ((run - 1) * self.max_time)) / (self.runs * self.max_time)) * 100)
            if self._interaction_mode in ('script', 'terminal'):
                if not self._progress_bar_started:
                    self._progress_bar_started = True
                    self._progress_bar.start()
                self._progress_bar.update(self._progress_percentage)
        else:
            Experiment._stdout_pattern_matched(self, pattern_index, match)
            

def test():
    experiment = McssExperiment()
#    print experiment.executable_

#    import sys
#    if sys.platform.startswith('win'):
#        experiment.load('C:\\src\\mcss-0.0.41\\examples\\models\\module1.params')
#    elif sys.platform == 'darwin':
#        experiment.load('/Users/jvb/src/mcss-0.0.41/examples/models/module1.params') 
#    else:
#        experiment.load('/home/jvb/src/mcss-0.0.41/examples/models/module1.params')
    
#    experiment.directory = '/home/jvb/src/mcss-0.0.41/examples'#/models'

    experiment.runs = 100
#    experiment.max_time = 3

    # test erroneous input for mcss
#    experiment.executable_kwargs = ['param=wrong']
#    experiment.model_file = 'module1.h5'

#    print experiment._dirty_parameters

##    print experiment._interaction_mode
#    experiment._interaction_mode = 'terminal'
##    for name, value in experiment._clean_parameters.items(): 
##        print name, value 
##    exit()


#    experiment.perform()
#    experiment.perform(thread=True)

    experiment.configure()


if __name__ == '__main__':
    test() 
