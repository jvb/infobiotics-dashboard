from infobiotics.pmodelchecker.pmodelchecker_params import PModelCheckerParams

class MC2Params(PModelCheckerParams):
    
    def _handler_default(self):
        from infobiotics.pmodelchecker.mc2.api import MC2ParamsHandler
        return MC2ParamsHandler(model=self)

    def _preferences_helper_default(self):
        from infobiotics.pmodelchecker.mc2.mc2_preferences import MC2ParamsPreferencesHelper
        return MC2ParamsPreferencesHelper()

    _parameter_set_name = 'mc2'
    
    model_checker = 'MC2'
    task = 'Approximate' # for PModelCheckerExperimentHandler.show_results
    temporal_formulas = 'temporal_formulas.pltl'

    def parameter_names(self): #TODO make Property?
        ''' Returns the subset of PModelChecker parameter names required for a 
        PModelChecker experiment with MC2. '''
        parameter_names = [
            'model_specification',
            'model_checker',
            'temporal_formulas',
            'number_samples',
            'results_file',
            'simulations_generatedHDF5',
            'simulations_generatedMC2',
        ]
        if self.simulations_generatedMC2:
            return parameter_names + [
                'simulations_file_MC2',
            ]
        if self.simulations_generatedHDF5:
            return parameter_names + [
                'simulations_file_hdf5',
                'simulations_file_MC2',
            ]
        else:
            return parameter_names + [
                'mcss_params_file',
                'simulations_file_hdf5',
                'simulations_file_MC2',
            ]
        

if __name__ == '__main__':
    parameters = MC2Params()
    parameters.configure()
    
