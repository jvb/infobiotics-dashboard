from infobiotics.pmodelchecker.api import PModelCheckerParams

class MC2Params(PModelCheckerParams):
    
    def _get_handler(self):
        from infobiotics.pmodelchecker.mc2.api import MC2ParamsHandler
        return MC2ParamsHandler(model=self)

    _parameter_set_name = 'mc2'
    
    model_checker = 'MC2'

    def translate_model_specification(self):
        super(MC2Params, self).translate_model_specification(self.directory, self.model_specification)
    
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
    