from __future__ import division


from infobiotics.pmodelchecker.prism.prism_params_handler import PRISMParamsHandler 
from infobiotics.pmodelchecker.pmodelchecker_experiment_handler import PModelCheckerExperimentHandler

class PRISMExperimentHandler(PRISMParamsHandler, PModelCheckerExperimentHandler):
    '''_params_group from PRISMParamsHandler and 
    perform functionality from PModelCheckerExperimentHandler'''
    
    def show_results(self):
        if self.model.task in ('Approximate', 'Verify'):
            PModelCheckerExperimentHandler.show_results(self)


from infobiotics.pmodelchecker.pmodelchecker_experiment import PModelCheckerExperiment
from infobiotics.pmodelchecker.prism.prism_params import PRISMParams
from traits.api import Str, Int, on_trait_change 

class PRISMExperiment(PRISMParams, PModelCheckerExperiment):
    '''TODO'''

    def __handler_default(self):
        return PRISMExperimentHandler(model=self)

    _current_property = Str
    _max_properties = Int(1) # pmodelchecker treats properties that are the same as one, which can cause problems in update_progress
    _property_index = Int(0)

    _stdout_pattern_list = [
        '[0-9]+ properties:', # '2 properties:',
        'Simulating: .+\]',
        'Sampling complete: [0-9]+ iterations in [0-9]+[.][0-9]+ seconds \(average [0-9]+[.][0-9]+\)', # 'Sampling complete: 10000 iterations in 234.15 seconds (average 0.023415)',
        '[0-9]+%',
        'Error:.*', # PRISM gets errors on stdout
        'Exception in thread "main" java',
#        'Parsing model file ".+"...', # 'Parsing model file "constitutive.sm"...',
#        'Parsing properties file ".+"...', # 'Parsing properties file "formulas.temp"...',
#        'Exporting results to file ".+"...', # 'Exporting results to file "Const_results.psm"...',
    ] 

    message = Str

    def _message_default(self):
        if self.task == 'Approximate':
            return 'Approximating %s' % self._current_property if self._current_property != '' else ''
        elif self.task == 'Verify':
            return 'Verifying %s' % self._current_property
        elif self.task == 'Build':
            return 'Building PRISM model %s' % self.PRISM_model
        elif self.task == 'Translate':
            return 'Translating PRISM model %s' % self.PRISM_model
            
    @on_trait_change('_current_property')
    def update_message(self):
        self.message = self._message_default()

    def _reset_progress_traits(self):
        '''Prevent TraitError where _progress_percentage is calculated to be > 100'''
        self._current_property = ''
        self._max_properties = 1
        self._property_index = 0
        PModelCheckerExperiment._reset_progress_traits(self) # resets _progress_percentage

    def _stdout_pattern_matched(self, pattern_index, match):
        pattern = match.group()
        if pattern_index == 0:
            self._max_properties = int(pattern.split(' properties:')[0])
        elif pattern_index == 1:
            self._current_property = pattern.split('Simulating: ')[1].strip()
        elif pattern_index == 2:
            self._property_index += 1
        elif pattern_index == 3:
            property_progress = int(pattern.strip('%'))
            subtotal = property_progress + (100 * (self._property_index))
            total = 100 * self._max_properties
            self._progress_percentage = (subtotal / total) * 100
        elif pattern_index > 3:
            self._stderr_pattern_matched(-1, match)


if __name__ == '__main__':
    experiment = PRISMExperiment()
#    print 'executable', experiment.executable
    experiment.configure()
