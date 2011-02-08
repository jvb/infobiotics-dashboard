from __future__ import division
from infobiotics.pmodelchecker.api import PModelCheckerExperiment
from infobiotics.pmodelchecker.mc2.api import MC2Params

class MC2Experiment(MC2Params, PModelCheckerExperiment):

    def __handler_default(self):
        from infobiotics.pmodelchecker.mc2.api import MC2ExperimentHandler
        return MC2ExperimentHandler(model=self)

    _stdout_pattern_list = [
        'Running mcss',
        'Simulation number [0-9]+ of [0-9]+', # previously 'Generating simulations in MC2 format'
        'Running MC2',
    ]
        
    def _stdout_pattern_matched(self, pattern_index, match):
        if pattern_index == 0:
            self.message = match
        elif pattern_index == 1:
            head, tail = match.split(' of ')
            max_simulation = int(tail)
            simulation = int(head.split('Simulation number ')[1])
            self._progress_percentage = (100 / max_simulation) * simulation
        elif pattern_index == 2:
            self.message = match
        else:
            super(MC2Experiment, self)._stdout_pattern_matched(self, pattern_index, match)
        


if __name__ == '__main__':
    experiment = MC2Experiment()
    experiment.load('/home/jvb/phd/eclipse/infobiotics/dashboard/examples/infobiotics-examples-20110208/quickstart-NAR/model_checking_mc2.params')
    experiment.perform()
#    experiment.configure()
