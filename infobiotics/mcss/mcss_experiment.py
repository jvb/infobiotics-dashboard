from infobiotics.shared.api import Experiment, Float, Int, DelegatesTo
from mcss_params import McssParams

class McssExperiment(Experiment):
    
    _params_program = 'mcss'
    _params_program_kwargs = ['show_progress=true', 'max_time=333', 'runs=66']
    _output_pattern_list = [
        '[0-9]+ [0-9]+', # 'time_in_run, run'
    ] 

    parameters = McssParams()
    max_time = DelegatesTo('parameters')
    runs = DelegatesTo('parameters')
        
    # output patterns
    run = Int(1)
    time_in_run = Float

    def _output_pattern_matched(self, pattern_index, match):
        if pattern_index == 0: # '1 20.5'
            time_in_run, run = match.split(' ')
            self.run = int(run)
            self.time_in_run = float(time_in_run)
        else:
            super(McssExperimentProgressHandler, self).pattern_matched(pattern_index, match)
    
    def _handler_default(self):
        from mcss_experiment_handler import McssExperimentHandler
        return McssExperimentHandler()