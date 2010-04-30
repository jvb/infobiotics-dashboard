from infobiotics.pmodelchecker.api import PModelCheckerParams
from infobiotics.shared.api import Bool, File

class MC2Params(PModelCheckerParams):
    
    _parameter_set_name = 'mc2'
    
    def _handler_default(self):
#        from infobiotics.pmodelchecker.mc2.mc2_params_handler import MC2ParamsHandler
        from mc2_params_handler import MC2ParamsHandler
        return MC2ParamsHandler(model=self)
    
    model_checker = 'MC2'

    def translate_model_specification(self):
        super(MC2Params, self).translate_model_specification(self._cwd, self.model_specification)
    
    def parameter_names(self):
        ''' Returns the subset of PModelChecker parameter names required for a 
        PModelChecker experiment with MC2. '''
        parameter_names = [
                'model_specification',
                'model_checker',
                'temporal_formulas',
                'number_samples',
                'results_file',
                'simulations_generatedHDF5',
                'simulations_file_hdf5',
                'simulations_generatedMC2',
                'simulations_file_MC2',
            ]
        if self.simulations_generatedHDF5:
            return parameter_names
        else:
            return parameter_names + [
                'mcss_params_file',
            ]
        

if __name__ == '__main__':
    parameters = MC2Params()
    parameters.load('test/Const/Const_MC2.params')
    parameters.configure()
    