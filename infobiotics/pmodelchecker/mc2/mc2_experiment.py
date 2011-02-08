from __future__ import division
from infobiotics.pmodelchecker.api import PModelCheckerExperiment
from infobiotics.pmodelchecker.mc2.api import MC2Params
from enthought.traits.api import Str, Int, Range

class MC2Experiment(MC2Params, PModelCheckerExperiment):

    def __handler_default(self):
        from infobiotics.pmodelchecker.mc2.api import MC2ExperimentHandler
        return MC2ExperimentHandler(model=self)

#    _pattern_list = [
#        'Running mcss',
#        'Simulation number [0-9]+ of [0-9]+', # previously 'Generating simulations in MC2 format'
#        'Running MC2',
#    ]
#        
#    def _output_pattern_matched(self, pattern_index, match):
#        if pattern_index == 0:
#            self.status = match
#        elif pattern_index == 1:
#            head, tail = match.split(' of ')
#            self.max_simulation = int(tail) # see below
#            self.simulation = int(head.split('Simulation number ')[1])
#        elif pattern_index == 2:
#            self.status = match
#        else:
#            super(MC2Experiment, self)._output_pattern_matched(self, pattern_index, match)
#        
#    min_simulation = Int(0) # because Range(0, 'max_simulation') which raises: "TypeError: unsupported operand type(s) for -: 'int' and 'code'"
#    max_simulation = Int(1)
#    simulation = Range('min_simulation', 'max_simulation')


#    @on_trait_change('model.max_simulation, model.simulation')
#    def update_progress(self):
#        self.progress = int((100 / self.max_simulation) * self.simulation) 



if __name__ == '__main__':
    experiment = MC2Experiment()
#    experiment.load('../../../tests/workbench_examples/motifs/NAR/pmodelchecker_example/NAR_MC2.params')
    experiment.load('../../../examples/NAR-pmodelchecker/model_checking_mc2.params')
    experiment.configure()
    
