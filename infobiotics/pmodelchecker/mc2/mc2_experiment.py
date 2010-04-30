from infobiotics.pmodelchecker.api import PModelCheckerExperiment
from enthought.traits.api import Str, Int

class MC2Experiment(PModelCheckerExperiment):

    _pattern_list = [
        'Running mcss',
        'Simulation number [0-9]+ of [0-9]+', # previously 'Generating simulations in MC2 format'
        'Running MC2',
    ]
        
    def _output_pattern_matched(self, pattern_index, match):
        if pattern_index == 0:
            self.status = match
        elif pattern_index == 1:
            head, tail = match.split(' of ')
#            self.max_simulation = int(tail) # see below
            self.simulation = int(head.split('Simulation number ')[1])
        elif pattern_index == 2:
            self.status = match
        else:
            super(MC2Experiment, self)._output_pattern_matched(self, pattern_index, match)
        
    status = Str
    min_simulation = Int(0) # because Range(0, 'max_simulation') which raises: "TypeError: unsupported operand type(s) for -: 'int' and 'code'"
    max_simulation = Int(1)
    simulation = Range('min_simulation', 'max_simulation')

#    view = View(
#        Item('status', style='readonly'),
#        Item('simulation'),
#        error_string_group,
#    )


if __name__ == '__main__':
    experiment = MC2Experiemnt()
    experiment.load('test/Const/modelCheckingMC2/Const_MC2.params')
    experiment.configure()