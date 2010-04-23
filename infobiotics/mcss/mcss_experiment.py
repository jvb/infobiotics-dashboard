from infobiotics.shared.api import Experiment, Float, Int
from infobiotics.mcss.api import McssParams

class McssExperiment(McssParams, Experiment):
    
    def _handler_default(self):
        from infobiotics.mcss.api import McssExperimentHandler
        return McssExperimentHandler(model=self)
    
    _params_program = 'mcss'
    _params_program_kwargs = ['show_progress=true']#, 'max_time=333', 'runs=66'] # testing
    _output_pattern_list = [
        '[0-9]+ [0-9]+', # 'time_in_run, run'
    ] 

    # output pattern traits
    run = Int(1)
    time_in_run = Float

    def _output_pattern_matched(self, pattern_index, match):
        if pattern_index == 0: # '1 20.5'
            time_in_run, run = match.split(' ')
            self.run = int(run)
            self.time_in_run = float(time_in_run)
        else:
            super(McssExperimentProgressHandler, self).pattern_matched(pattern_index, match)

if __name__ == '__main__':
    from infobiotics.shared.api import chdir
    chdir('../../tests/mcss/models')
    McssExperiment('module1.params').configure()
