from infobiotics.common.api import Params, ParamsRelativeFile
from enthought.traits.api import Enum, Str, Float, Bool
from infobiotics.commons.traits.api import LongGreaterThanZero
import os.path

class PModelCheckerParams(Params):
    ''' Base class for PRISMParams and MC2Params. '''

    executable_name = 'pmodelchecker'
    
    _parameters_name = 'pmodelchecker'

    # PRISMParams and MC2Params ---

    model_checker = Enum(['PRISM','MC2'], desc='the name of the model checker to use, PRISM or MC2')

    model_specification = ParamsRelativeFile(readable=True, filter=['Lattice Population P systems (*.lpp)','All files (*)'], desc='name of the file containing the model specification as an LPP-system')
    positions = Str('all', desc="a string stating the positions of the P systems under study.\nThe format of the string is the following: 'x_1,y_1:x_2,y_2: ... :x_n,y_n'")
    molecular_species = Str('all', desc="a string stating the name of the molecular species under study.\nThe format of the string is the following: 'moleculeName_1,moleculeName_2, ...,moleculeName_n'")

    temporal_formulas = ParamsRelativeFile(writable=True, desc='the name of the file containing the temporal logic formulas formalising the properties to check')
    formula_parameters = Str(desc="a string stating the values of the parameters in the formulas as follows:\n'param=lb:ub:s,param=lb:ub:s, ...' where lb is the lower bound, up is the upper bound and s is the step.\nParameters with a single value can also be specified as follows:\n'param=value,param=value, ...'")

    number_samples = LongGreaterThanZero(desc='the number of simulations to generate')
    precision = Float(1.0, desc='the precision to achieve with respect to a real value')
    confidence = Float(0.1, desc='the confidence to achieve with respect to a real value')

    results_file = ParamsRelativeFile('results.txt', desc='the name of the file to write the answers to the temporal logic formulas generated by the model checker')

    # PRISMParams only ---
    
    PRISM_model = ParamsRelativeFile('PRISM_model.sm', writable=True, auto_set=False, filter=['PRISM models (*.sm)','All files (*)'], desc='the name of the file to output the translation of the input LPP model into the PRISM language')
    
    model_parameters = Str(desc="a string stating the values of the parameters in the model as follows: 'param=lb:ub:s,param=lb:ub:s,...' where lb is the lower bound, up is the upper bound and s is the step")
    
    task = Enum(['Approximate','Translate','Build','Verify'], desc='the task to perform: Translate LPP-system into the PRISM language; Build corresponding Markov chain; Verify or Approximate the input properties')
    
    states_file = ParamsRelativeFile('states.sm', desc='the name of the file to output the states of the Markov chain generated from the LPP-system when using PRISM with the tasks Build or Verify')
    transitions_file = ParamsRelativeFile('transitions.sm', desc='the name of the file to output the transitions of the Markov chain generated from the LPP-system when using PRISM with the tasks Build or Verify')

    # MC2Params only ---
    
    simulations_generatedHDF5 = Bool(False, desc='a flag to determine if the simulations needed to run MC2 are available in HDF5 format')
    simulations_file_hdf5 = ParamsRelativeFile(exists_name='simulations_generatedHDF5', writable=True, filter=['*.h5','*'], desc='the filename(.h5) of the simulation')
    
    simulations_generatedMC2 = Bool(False, desc='a flag to determine if the simulations needed to run MC2 are available in MC2 format')
    simulations_file_MC2 = ParamsRelativeFile(exists_name='simulations_generatedMC2', writable=True, filter=['*.mc2','*'], desc='the filename(.mc2) of the simulation converted to MC2 format')
    
    mcss_params_file = ParamsRelativeFile(filters=['*.params'], desc='the name of the file containing the parameters to run mcss in order to generate the necessary simulations when using MC2 as the model checker')
    
    def _model_specification_changed(self):
        if os.path.isfile(self.model_specification):
            self.translate_model_specification() # must be reimplemented in subclasses

    def translate_model_specification(self, dir, model_specification, PRISM_model=''):
        ''' Performs an experiment with task='Translate' to generate the 
        PRISM model and modelParameters.xml from LPP model specification. '''
        import tempfile
        if PRISM_model == '':
            PRISM_model_temp_file = tempfile.NamedTemporaryFile(dir=dir)
            PRISM_model = PRISM_model_temp_file.name
            
        from prism.api import PRISMExperiment
        translate_experiment = PRISMExperiment(_cwd=dir)
        translate_experiment.trait_setq(model_specification=model_specification, PRISM_model=PRISM_model, task='Translate')
        
        params_temp_file = tempfile.NamedTemporaryFile(dir=dir) 
        params_temp_file_name = params_temp_file.name
        translate_experiment.save(params_temp_file_name)
        translate_experiment.perform()
    
    #    import os.path
    #    if not os.path.exists(os.path.abspath(os.path.join(translate_experiment._cwd, translate_experiment.PRISM_model))):
    #        del temp_file
    #        raise Exception('%s was not created.' % self.PRISM_model)


if __name__ == '__main__':
    execfile('prism/prism_params.py')
    