from infobiotics.pmodelchecker.api import PModelCheckerParams, ModelParameters  
from infobiotics.shared.api import (
    File, Instance, DelegatesTo, Range, Float, Long, Str, Enum, Trait, Bool, 
    Button, Property
) 

class PRISMParams(PModelCheckerParams):

    _parameter_set_name = 'prism'

    def _handler_default(self):
        from infobiotics.pmodelchecker.prism_params_handler import PRISMParamsHandler
        return PRISMParamsHandler(model=self)

    model_checker = 'PRISM'
    model_specification = File(exists=True, filter=['*.lpp *.xml'], desc='the filename of the model to check') #TODO have multiple wildcards in one filter?
    PRISM_model = File('PRISM_model.sm', filter=['*.sm','*'], desc='the filename of the intermediate PRISM model')
#    _model_parameters = Instance('ModelParameters')
##    def __model_parameters_default(self):
##        return ModelParameters(prism_experiment=self)
#    model_parameters = DelegatesTo('_model_parameters')
    model_parameters = Str(desc="a string stating the values of the parameters in the model as follows: 'param=lb:ub:s,param=lb:ub:s,...' where lb is the lower bound, up is the upper bound and s is the step")
    temporal_formulas = File(desc='') #TODO desc
    formula_parameters = Str(desc='') #TODO PRISM-specific? desc
    task = Enum(['Approximate','Translate','Build','Verify'], desc='')  #TODO desc
    confidence = Float(0.1, desc='the confidence level used when approximating the answer to a formula')
    precision = Float(1.0, desc='the precision used when approximating the answer to a formula')
    results_file = File('results.txt', desc='') #TODO desc
    states_file = File('states.psm', desc='')  #TODO desc
    transitions_file = File(desc='')  #TODO desc
    number_samples = Long(desc='the number of simulations to used when approximation is applied')
    
    def parameter_names(self):
        ''' Returns the subset of PModelChecker parameter names required for a 
        PRISMExperiment.
        
        '''
        return [
            'model_checker',
            'model_specification',
            'PRISM_model',
#            'model_parameters',
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
            

if __name__ == '__main__':
    parameters = PRISMParams()
    parameters.load('test/Const/modelCheckingPRISM/Const_PRISM.params')
    parameters.configure()
                        