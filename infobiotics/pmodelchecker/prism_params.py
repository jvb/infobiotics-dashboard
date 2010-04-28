from infobiotics.pmodelchecker.api import PModelCheckerParams, ModelParameters
from infobiotics.shared.api import (
    File, Instance, DelegatesTo, Range, Float, Long, Str, Enum, Trait, Bool, 
    Button, Property, can_read
)

class PRISMParams(PModelCheckerParams):

    _parameter_set_name = 'prism'

    def _handler_default(self):
        from infobiotics.pmodelchecker.prism_params_handler import PRISMParamsHandler
        return PRISMParamsHandler(model=self)

    model_checker = 'PRISM'
    model_specification = File(readable=True, filter=['Lattice Population P systems (*.lpp)','P system XML files (*.xml)','All files (*)'], desc='the filename of the model to check') #TODO have multiple wildcards in one filter?
    PRISM_model = File('PRISM_model.sm', writable=True, auto_set=False, filter=['PRISM models (*.sm)','All files (*)'], desc='the filename of the intermediate PRISM model')

    model_parameters = Str(desc="a string stating the values of the parameters in the model as follows: 'param=lb:ub:s,param=lb:ub:s,...' where lb is the lower bound, up is the upper bound and s is the step")

    temporal_formulas = File #TODO desc
    
    formula_parameters = Str #TODO desc #FIXME PRISM-specific?
    
    task = Enum(['Approximate','Translate','Build','Verify'])  #TODO desc
    confidence = Float(0.1, desc='the confidence level used when approximating the answer to a formula')
    precision = Float(1.0, desc='the precision used when approximating the answer to a formula')
    results_file = File('results.txt') #TODO desc
    states_file = File('states.psm')  #TODO desc
    transitions_file = File  #TODO desc
    number_samples = Long(desc='the number of simulations to used when approximation is applied')
    
    def parameter_names(self):
        ''' Returns the subset of PModelChecker parameter names required for a 
        PRISMExperiment.
        
        '''
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
    #            'formula_parameters', # done by model checker
                'task',
                'confidence',
                'precision',
                'results_file',
                'states_file',
                'transitions_file',
                'number_samples',
            ]    

    def load(self, file=''):
        super(PRISMParams, self).load(file)
        if not can_read(self.PRISM_model):
            if self.model_specification != '':
                self.translate_model_specification_to_PRISM_model()

    def translate_model_specification_to_PRISM_model(self):
        from infobiotics.pmodelchecker.api import PRISMExperiment
        translate_experiment = PRISMExperiment(_cwd=self._cwd) #TODO why is task already Translate?
#        translate_experiment.trait('PRISM_model').handler.exists=False
        translate_experiment.trait_set(model_specification=self.model_specification, PRISM_model=self.PRISM_model, task='Translate')
        #TODO parameter_names = ['model_specification','PRISM_model','task']
        import tempfile
        temp_file = tempfile.NamedTemporaryFile(dir=translate_experiment._cwd) 
        temp_file_name = temp_file.name
        translate_experiment.save(temp_file_name)
        translate_experiment.perform()
        import os.path
        if not os.path.exists(os.path.abspath(os.path.join(translate_experiment._cwd, translate_experiment.PRISM_model))):
            del temp_file
            raise Exception('%s was not created.' % self.PRISM_model)
        self.PRISM_model = ''
        self.PRISM_model = translate_experiment.PRISM_model


if __name__ == '__main__':
    parameters = PRISMParams()
    parameters.load('test/Const/modelCheckingPRISM/Const_PRISM.params')
    parameters.configure()
                        