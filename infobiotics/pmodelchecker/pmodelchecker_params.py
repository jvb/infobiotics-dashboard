from infobiotics.shared.api import Params

class PModelCheckerParams(Params):

    # PRISMExperiment and MC2Experiment
    model_specification = File(directory_name='_cwd', auto_set=True, filter=['*.xml','*.lpp'], desc='the filename(.lpp) of the model to check') #TODO have multiple wildcards in one filter?
    model_checker = Enum(['PRISM','MC2'], desc='the name of model checker to use')
    number_samples = Long(desc='the number of simulations to used when approximation is applied')
#
#    # PRISMExperiment
#    PRISM_model = File('PRISM_model.sm', filter=['*.sm','*'],desc='the filename(.sm) of the intermediate PRISM model')
#    temporal_formulas = File(desc='') #TODO MC2-specific? desc
#    formula_parameters = Str(desc='') #TODO PRISM-specific? desc
#    model_parameters = Str('') #TODO desc
#    confidence = Float(0.1, desc='the confidence level used when approximating the answer to a formula')
#    precision = Float(1.0, desc='the precision used when approximating the answer to a formula')
#    results_file = File('results.txt', desc='') #TODO desc
#    states_file = File('states.psm', desc='')  #TODO desc
#    task = Enum(['Approximate','Translate','Build','Verify'], desc='')  #TODO desc
#    transitions_file = File(desc='')  #TODO desc
##    parameters_file = File(desc='a filename for the parameters of the PRISM model')

    # MC2Experiment
    simulations_generatedHDF5 = Bool(False, desc='whether the simulations have already been run')
    simulations_file_hdf5 = File(directory_name='_cwd', auto_set=True, filter=['*.h5','*'], desc='the filename(.h5) of the simulation')
    simulations_generatedMC2 = Bool(False, desc='whether the TODO have already been run')
    simulations_file_MC2 = File(directory_name='_cwd', auto_set=True, filter=['*.mc2','*'], desc='the filename(.mc2) of the simulation converted to MC2 format')
    mcss_params_file = File(directory_name='_cwd', auto_set=True, filters=['*.params'], desc='TODO')

#    def parameters_names(self):
#        return [
#            'model_specification',
#            'model_checker',
#            'number_samples',
#            'formula_parameters',
#            'PRISM_model',
#            'temporal_formulas',
#            'model_parameters',
#            'confidence',
#            'precision',
#            'results_file',
#            'states_file',
#            'task',
#            'transitions_file',
#            'simulations_generatedHDF5',
#            'simulations_file_hdf5',
#            'simulations_generatedMC2',
#            'simulations_file_MC2',
#            'mcss_params_file',
#        ]


