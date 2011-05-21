from __future__ import division
from infobiotics.pmodelchecker.pmodelchecker_experiment import PModelCheckerExperiment
from infobiotics.pmodelchecker.prism.prism_params import PRISMParams
from enthought.traits.api import Str, Int, Range, on_trait_change#, Enum, Property, Bool 

from infobiotics.pmodelchecker.prism.prism_params_handler import PRISMParamsHandler#, PRISMExperimentProgressHandler 
from infobiotics.pmodelchecker.pmodelchecker_experiment_handler import PModelCheckerExperimentHandler

class PRISMExperimentHandler(PRISMParamsHandler, PModelCheckerExperimentHandler):
    '''_params_group from PRISMParamsHandler and 
    perform functionality from PModelCheckerExperimentHandler'''
    
    def show_results(self):
        if self.model.task in ('Approximate', 'Verify'):
            PModelCheckerExperimentHandler.show_results(self)


class PRISMExperiment(PRISMParams, PModelCheckerExperiment):

    def __handler_default(self):
        return PRISMExperimentHandler(model=self)

#    def perform(self, thread=True):
#        # if prism model doesn't exist quickly do a Translate to create it
#        import os.path
#        if hasattr(self, 'PRISM_model_') and not os.path.exists(self.PRISM_model_) and not self.task == 'Translate':
#            print 'Translating model specification in PRISMExperiment.perform()'
#            self.translate_model_specification()
##        if self.message:
##            print self.message
#        super(PRISMExperiment, self).perform(thread)


    _stdout_pattern_list = [
        '[0-9]+ properties:', # '2 properties:',
        'Simulating: .+\]',
        'Sampling complete: [0-9]+ iterations in [0-9]+[.][0-9]+ seconds \(average [0-9]+[.][0-9]+\)', # 'Sampling complete: 10000 iterations in 234.15 seconds (average 0.023415)',
        '[0-9]+%',
#        'Parsing model file ".+"...', # 'Parsing model file "constitutive.sm"...',
#        'Parsing properties file ".+"...', # 'Parsing properties file "formulas.temp"...',
#        'Exporting results to file ".+"...', # 'Exporting results to file "Const_results.psm"...',
    ] 

    def _reset_progress_traits(self):
        '''Prevent TraitError where _progress_percentage is calculated to be > 100'''
        self._current_property = ''
        self._max_properties = 1
        self._property_index = 0
        PModelCheckerExperiment._reset_progress_traits(self) # resets _progress_percentage

    _current_property = Str
    _max_properties = Int(1) # pmodelchecker treats properties that are the same as one, which can cause problems in update_progress
    _property_index = Int(0)

    def _stdout_pattern_matched(self, pattern_index, match):
        if pattern_index == 0:
            self._max_properties = int(match.split(' properties:')[0])
        elif pattern_index == 1:
            self._current_property = match.split('Simulating: ')[1].strip()
        elif pattern_index == 2:
            self._property_index += 1
        elif pattern_index == 3:
            property_progress = int(match.strip('%'))
            subtotal = property_progress + (100 * (self._property_index))
            total = 100 * self._max_properties
            self._progress_percentage = (subtotal / total) * 100
        elif pattern_index > 3:
            super(PRISMExperiment, self).pattern_matched(self, pattern_index, match)
#        elif pattern_index == 4:
#            self.error_string = match
#            print self.error_string

    _stderr_pattern_list = [
        'Exception in thread "main" java',
#        ''' Error: parameters with same name and different ranges: 
#0:10:3000:10:100''',
    ] 
    
#    message = Str
#
#    def _message_default(self):
#        if self.task == 'Approximate':
#            return 'Approximating %s' % self._current_property if self._current_property != '' else ''
#        elif self.task == 'Verify':
#            return 'Verifying %s' % self._current_property
#        elif self.task == 'Build':
#            return 'Building PRISM model %s' % self.PRISM_model
#        elif self.task == 'Translate':
#            return 'Translating PRISM model %s' % self.PRISM_model
#            
#    @on_trait_change('_current_property')
#    def update_message(self):
##        print 'got here'
#        self.message = self._message_default()
##        print self.message
#    def _message_changed(self, value):
##        print 'got here too'
#        print self.message


if __name__ == '__main__':
    experiment = PRISMExperiment()
#    experiment.load('/home/jvb/phd/eclipse/infobiotics/dashboard/examples/infobiotics-examples-20110208/quickstart-NAR/model_checking_prism.params')
#    experiment._interaction_mode = 'gui'
#    experiment.perform(thread=True)
#    experiment.perform(thread=False)
#    experiment.perform(thread=False)
    experiment.configure()
