from pmodelchecker_params import PModelCheckerParams
from infobiotics.shared.api import Bool, File


class MC2Params(PModelCheckerParams):
    
    _parameter_set_name = 'mc2'
    
    def _handler_default(self):
        from infobiotics.pmodelchecker.api import MC2ParamsHandler
        return MC2ParamsHandler(model=self)
    
    model_checker = 'MC2'

    #TODO commented traits are defined in PModelCheckerParams

#    model_specification = File(readable=True, filter=['Lattice Population P systems (*.lpp)','All files (*)'])
    
    simulations_generatedHDF5 = Bool(False, desc='whether the simulations have already been run')
    simulations_file_hdf5 = File(exists_name='simulations_generatedHDF5', writable=True, filter=['*.h5','*'], desc='the filename(.h5) of the simulation')
    
    simulations_generatedMC2 = Bool(False, desc='whether the TODO have already been run')
    simulations_file_MC2 = File(exists_name='simulations_generatedMC2', writable=True, filter=['*.mc2','*'], desc='the filename(.mc2) of the simulation converted to MC2 format')
    
    mcss_params_file = File(filters=['*.params'], desc='TODO')
    
#    temporal_formulas = File(writable=True)
#    formula_parameters = Str

#    number_samples = Long
#    precision = Float(1.0)
#    confidence = Float(0.1)

#    results_file = File('results.txt') #TODO desc
    
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
    parameters.load('test/Const/modelCheckingMC2/Const_MC2.params')
    parameters.configure()
    