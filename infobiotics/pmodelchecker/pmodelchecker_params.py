from infobiotics.core.params import Params
from infobiotics.core.api import ParamsRelativeFile
from enthought.traits.api import Enum, Str, Float, Bool, Range, on_trait_change, Property
from infobiotics.commons.traits.api import LongGreaterThanZero
from infobiotics.pmodelchecker.pmodelchecker_preferences import PModelCheckerParamsPreferencesHelper
import tempfile
import sys
import os.path

class PModelCheckerParams(Params):
    ''' Base class for PRISMParams and MC2Params. '''

    preferences_helper = PModelCheckerParamsPreferencesHelper()

    executable_name = 'pmodelchecker'
    
    _parameters_name = 'pmodelchecker'

    # Both PRISM and MC2
    model_checker = Enum(['PRISM','MC2'], desc='the name of the model checker to use, PRISM or MC2')

    model_specification = ParamsRelativeFile(readable=True, filter=['Lattice Population P systems (*.lpp)','All files (*)'], desc='name of the file containing the model specification as an LPP-system')
    positions = Str('all', desc="a string stating the positions of the P systems under study.\nThe format of the string is the following: 'x_1,y_1:x_2,y_2: ... :x_n,y_n'")
    molecular_species = Str('all', desc="a string stating the name of the molecular species under study.\nThe format of the string is the following: 'moleculeName_1,moleculeName_2, ...,moleculeName_n'")

    temporal_formulas = ParamsRelativeFile('temporal_formulas', auto_set=False, writable=True, desc='the name of the file containing the temporal logic formulas formalising the properties to check')

    number_samples = LongGreaterThanZero(desc='the number of simulations to generate')
    precision = Float(1.0, desc='the precision to achieve with respect to a real value')
    confidence = Range(0.0, 1.0, 0.1, desc='the confidence to achieve with respect to a real value')

    results_file = ParamsRelativeFile('results.psm', desc='the name of the file to write the answers to the temporal logic formulas generated by the model checker')

    PRISM_model = ParamsRelativeFile('PRISM_model.sm', writable=True, auto_set=False, filter=['PRISM models (*.sm)','All files (*)'], desc='the name of the file to output the translation of the input LPP model into the PRISM language')
    
    model_parameters = Str(desc="a string stating the values of the parameters in the model as follows: 'param=lb:ub:s,param=lb:ub:s,...' where lb is the lower bound, up is the upper bound and s is the step")
    
    task = Enum(['Approximate','Translate','Build','Verify'], desc='the task to perform: Translate LPP-system into the PRISM language; Build corresponding Markov chain; Verify or Approximate the input properties')
    
    _model_specification_changed = Bool(False)
    _translated = Bool(False)
    
    # PRISM only
    states_file = ParamsRelativeFile('states.sm', desc='the name of the file to output the states of the Markov chain generated from the LPP-system when using PRISM with the tasks Build or Verify')
    transitions_file = ParamsRelativeFile('transitions.sm', desc='the name of the file to output the transitions of the Markov chain generated from the LPP-system when using PRISM with the tasks Build or Verify')

    # MC2 only
    simulations_generatedHDF5 = Bool(False, desc='a flag to determine if the simulations needed to run MC2 are available in HDF5 format')
    simulations_file_hdf5 = ParamsRelativeFile(empty_ok_name='_empty_ok', auto_set=False, exists_name='simulations_generatedHDF5', writable=True, filter=['*.h5','*'], desc='the filename(.h5) of the simulation')
    
    mcss_params_file = ParamsRelativeFile(empty_ok_name='_empty_ok', auto_set=False, filters=['*.params'], desc='the name of the file containing the parameters to run mcss in order to generate the necessary simulations when using MC2 as the model checker')

    _empty_ok = Property(Bool, depends_on='simulations_generatedHDF5, simulations_generatedMC2')
    def _get__empty_ok(self):
        return self.simulations_generatedHDF5 or self.simulations_generatedMC2
    
    simulations_generatedMC2 = Bool(False, desc='a flag to determine if the simulations needed to run MC2 are available in MC2 format')
    simulations_file_MC2 = ParamsRelativeFile(exists_name='simulations_generatedMC2', writable=True, filter=['*.mc2','*'], desc='the filename(.mc2) of the simulation converted to MC2 format')

    @on_trait_change('model_specification, PRISM_model')
    def translate_model_specification(self, object, name, old, new):
        ''' Performs an experiment with task='Translate' to generate the 
        PRISM model and modelParameters.xml from self.model_specification. '''
        
        self._translated = False
        
        # guard
        if self.model_specification == '':
            return
        
#        # can't get here that empty RelativeFiles are erroneous 
#        if hasattr(self, '_PRISM_model_tempfile') and self.PRISM_model_ != self._PRISM_model_tempfile.name:
#            # delete old temporary file
#            del self._PRISM_model_tempfile #TODO may not be enough now that 'delete=False' below
#        
#        if self.PRISM_model == '':
#            # create temporary file
#            self._PRISM_model_tempfile = tempfile.NamedTemporaryFile(suffix='.sm', dir=self.directory, delete=False)
#            self._PRISM_model_tempfile.close()
#            # trigger translation with temporary file
#            if sys.version_info[0] > 2 or (sys.version_info[0] == 2 and sys.version_info[1] >= 6): 
#                self.trait_set(PRISM_model=os.path.relpath(self._PRISM_model_tempfile.name, self.directory))
#            else:
#                self.trait_set(PRISM_model=self._PRISM_model_tempfile.name)
#            return
            
        from infobiotics.pmodelchecker.prism.api import PRISMExperiment # avoids circular import    
        translate = PRISMExperiment(directory=self.directory)
        translate.trait_setq( # set quietly otherwise this triggers _model_specification_changed above
            model_specification=self.model_specification, 
            PRISM_model=self.PRISM_model_, # must set PRISM_model with PRISM_model_ as trait_setq doesn't trigger creation of shadow trait 
            task='Translate',
        ) 
        translate.perform(thread=False)
        
        # needed by PModelCheckerParamsHandler.model_specification_changed
        if name == 'model_specification':
            self._model_specification_changed = True
        else:
            self._model_specification_changed = False

        self._translated = True


if __name__ == '__main__':
    execfile('prism/prism_experiment.py')
            