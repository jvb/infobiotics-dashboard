from infobiotics.pmodelchecker.api import PModelCheckerParams
from infobiotics.shared.api import File, Str, Enum

class PRISMParams(PModelCheckerParams):

    _parameter_set_name = 'prism'

    def _handler_default(self):
        from infobiotics.pmodelchecker.prism_params_handler import PRISMParamsHandler
        return PRISMParamsHandler(model=self)

    model_checker = 'PRISM'
    PRISM_model = File('PRISM_model.sm', writable=True, auto_set=False, filter=['PRISM models (*.sm)','All files (*)'], desc='the name of the file to output the translation of the input LPP model into the PRISM language')
    model_parameters = Str(desc="a string stating the values of the parameters in the model as follows: 'param=lb:ub:s,param=lb:ub:s,...' where lb is the lower bound, up is the upper bound and s is the step")
    task = Enum(['Approximate','Translate','Build','Verify'], desc='the task to perform: Translate LPP-system into the PRISM language; Build corresponding Markov chain; Verify or Approximate the input properties')
    states_file = File('states.sm', desc='the name of the file to output the states of the Markov chain generated from the LPP-system when using PRISM with the tasks Build or Verify')
    transitions_file = File('transitions.sm', desc='the name of the file to output the transitions of the Markov chain generated from the LPP-system when using PRISM with the tasks Build or Verify')
    results_file = 'results.psm'

    def translate_model_specification(self):
        super(PRISMParams, self).translate_model_specification(self._cwd, self.model_specification, self.PRISM_model)
        PRISM_model = self.PRISM_model
        self.PRISM_model = ''
        self.PRISM_model = PRISM_model
    
    def parameter_names(self):
        ''' Returns the subset of parameter names required for a particular 
        PRISMExperiment. '''
        if self.task == 'Translate':
            return [
                'model_checker',
                'model_specification',
                'PRISM_model',
                'task',
            ]
        else:
            return [
                'model_checker',
                'model_specification',
                'PRISM_model',
                'model_parameters',
                'temporal_formulas',
                'formula_parameters',
                'task',
                'confidence',
                'precision',
                'results_file',
                'states_file',
                'transitions_file',
                'number_samples',
            ]    


if __name__ == '__main__':
    parameters = PRISMParams()
    parameters.load('test/Const/modelCheckingPRISM/Const_PRISM.params')
    parameters.configure()
                        