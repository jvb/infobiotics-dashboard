import os.path
from infobiotics.pmodelchecker.api import (
    PModelCheckerExperiment, 
)
from infobiotics.pmodelchecker.prism.api import PRISMParams
from enthought.traits.api import Enum, Property, Str, Int, Range, Bool

class PRISMExperiment(PRISMParams, PModelCheckerExperiment):

    def _handler_default(self):
        from infobiotics.pmodelchecker.prism.api import PRISMExperimentHandler
        return PRISMExperimentHandler(model=self)

#    pattern_list = [
#        '[0-9]+ properties:', # '2 properties:',
#        'Simulating: .+\]',
#        '[0-9]+%',
#        'Sampling complete: [0-9]+ iterations in [0-9]+[.][0-9]+ seconds \(average [0-9]+[.][0-9]+\)', # 'Sampling complete: 10000 iterations in 234.15 seconds (average 0.023415)',
#        'Exception in thread "main" java',
##        'Parsing model file ".+"...', # 'Parsing model file "constitutive.sm"...',
##        'Parsing properties file ".+"...', # 'Parsing properties file "formulas.temp"...',
##        'Exporting results to file ".+"...', # 'Exporting results to file "Const_results.psm"...',
#    ]
#        
#    def pattern_matched(self, pattern_index, match):
#        if pattern_index == 0:
#            self.max_properties = int(match.split(' properties:')[0])
#        elif pattern_index == 1:
#            self.current_property = match.split('Simulating: ')[1].strip()
#        elif pattern_index == 2:
#            self.property_progress = int(match.strip('%'))
#        elif pattern_index == 3:
#            self.property_index += 1
#        elif pattern_index == 4:
#            self.error_string = match
#        elif pattern_index > 4:
#            super(PRISMExperiment, self).pattern_matched(self, pattern_index, match)
#
#    current_property = Str
#    max_properties = Int(1)
#    property_index = Int(0)
#    property_progress = Range(0, 100)

#    #TODO uncomment?
#    def perform(self, thread=True):
#        # if prism model doesn't exist quickly do a Translate to create it #FIXME this shouldn't be the case
#        if hasattr(self, 'PRISM_model_'):
#            if not os.path.exists(self.PRISM_model_) and not self.task == 'Translate':
#                self.translate_model_specification()
#        return super(PRISMExperiment, self).perform(thread) #FRAGILE must return True here or the PRISMExperimentProgressHandler is never shown


def test_model_parameters():
    import os
    os.chdir('../../../examples/NAR-pmodelchecker/')
    print 'cwd =', os.getcwd()
    print
    
    print "os.path.exists('modelParameters.xml') =", os.path.exists('modelParameters.xml') 
    experiment = PRISMExperiment()
    print 'experiment.model_specification =', experiment.model_specification 
    print 
    
    file = 'model_checking_prism.params'
    experiment.load(file)
    print 'loaded', file
    print "os.path.exists('modelParameters.xml') =", os.path.exists('modelParameters.xml') 
    print 'experiment.model_specification =', experiment.model_specification 
    print
    
#    experiment.configure()
    

if __name__ == '__main__':
#    experiment = PRISMExperiment()
##    experiment.load('../../../tests/workbench_examples/motifs/NAR/pmodelchecker_example/NAR_PRISM.params')
#    experiment.load('../../../examples/NAR-pmodelchecker/model_checking_prism.params')
#    experiment.configure()
    test_model_parameters()
    