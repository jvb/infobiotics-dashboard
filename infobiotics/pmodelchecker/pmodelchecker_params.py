from infobiotics.core.params import Params
from infobiotics.core.api import ParamsRelativeFile, ModelFile
from traits.api import Enum, Str, Float, Bool, Range, on_trait_change, Property, cached_property, TraitError
import os.path
from infobiotics.commons.traits_.api import LongGreaterThanZero

from infobiotics.commons.api import logging
logger = logging.getLogger(__name__)

class PModelCheckerParams(Params):
    '''Base class for PRISMParams and MC2Params.'''

    def _preferences_helper_default(self):
        from infobiotics.pmodelchecker.pmodelchecker_preferences import PModelCheckerParamsPreferencesHelper
        return PModelCheckerParamsPreferencesHelper()
    
    executable_name = 'pmodelchecker'
    _parameters_name = 'pmodelchecker'

    # Both PRISM and MC2
    model_checker = Enum(['PRISM', 'MC2'], desc='the name of the model checker to use, PRISM or MC2')
    model_specification = ModelFile
    positions = Str('all', desc="a string stating the positions of the P systems under study.\nThe format of the string is the following: 'x_1,y_1:x_2,y_2: ... :x_n,y_n'")
    molecular_species = Str('all', desc="a string stating the name of the molecular species under study.\nThe format of the string is the following: 'moleculeName_1,moleculeName_2, ...,moleculeName_n'")
    temporal_formulas = ParamsRelativeFile('temporal_formulas', auto_set=False, writable=True, desc='the name of the file containing the temporal logic formulas formalising the properties to check')
    number_samples = LongGreaterThanZero(desc='the number of simulations to generate')
    precision = Float(1.0, desc='the precision to achieve with respect to a real value')
    confidence = Range(0.0, 1.0, 0.1, desc='the confidence to achieve with respect to a real value')
    results_file = ParamsRelativeFile('results.psm', writable=True, desc='the name of the file to write the answers to the temporal logic formulas generated by the model checker')
    PRISM_model = ParamsRelativeFile('PRISM_model.sm', writable=True, auto_set=False, filter=['PRISM models (*.sm)', 'All files (*)'], desc='the name of the file to output the translation of the input LPP model into the PRISM language')
    model_parameters = Str(desc="a string stating the values of the parameters in the model as follows: 'param=lb:ub:s,param=lb:ub:s,...' where lb is the lower bound, up is the upper bound and s is the step")
    task = Enum(['Approximate', 'Translate', 'Build', 'Verify'], desc='the task to perform: Translate LPP-system into the PRISM language; Build corresponding Markov chain; Verify or Approximate the input properties')
    
    # PRISM only
    states_file = ParamsRelativeFile('states.sm', desc='the name of the file to output the states of the Markov chain generated from the LPP-system when using PRISM with the tasks Build or Verify')
    transitions_file = ParamsRelativeFile('transitions.sm', desc='the name of the file to output the transitions of the Markov chain generated from the LPP-system when using PRISM with the tasks Build or Verify')

    # MC2 only
    simulations_generatedHDF5 = Bool(False, desc='a flag to determine if the simulations needed to run MC2 are available in HDF5 format')
    simulations_generatedMC2 = Bool(False, desc='a flag to determine if the simulations needed to run MC2 are available in MC2 format')
    simulations_file_hdf5 = ParamsRelativeFile(
        empty_ok_name='simulations_generatedMC2',
        auto_set=False,
        exists_name='_simulations_file_hdf5_exists',
        writable=True, #TODO writable_name in RelativeFile instead of not using can_write_file in RelativeFile._validate 
        filter=['*.h5', '*'],
        desc='the filename(.h5) of the simulation',
    )
    mcss_params_file = ParamsRelativeFile(
        empty_ok_name='_mcss_params_file_empty_ok', # True if simulations_generatedHDF5 or simulations_generatedMC2 else False 
        auto_set=False,
        filters=['*.params'],
        desc='the name of the file containing the parameters to run mcss in order to generate the necessary simulations when using MC2 as the model checker',
    )
    simulations_file_MC2 = ParamsRelativeFile(
        exists_name='simulations_generatedMC2',
        writable=True, #TODO writable_name in RelativeFile instead of not using can_write_file in RelativeFile._validate
        filter=['*.mc2', '*'],
        desc='the filename(.mc2) of the simulation converted to MC2 format',
    )

    # protected traits
    _model_specification_changed = Bool(False)
    _translated = Bool(False)
    _mcss_params_file_empty_ok = Property(Bool, depends_on='simulations_generatedHDF5, simulations_generatedMC2')
    _simulations_file_hdf5_exists = Property(Bool, depends_on='simulations_generatedHDF5, simulations_generatedMC2')

    @cached_property
    def _get__mcss_params_file_empty_ok(self):
        return self.simulations_generatedHDF5 or self.simulations_generatedMC2

    @cached_property
    def _get__simulations_file_hdf5_exists(self):
        '''Necessary because simulations_generatedMC2 overrides 
        simulations_generatedHDF5.'''
        if self.simulations_generatedMC2:
            return False
        elif self.simulations_generatedHDF5:
            return True
        return False

    @on_trait_change('model_specification', 'PRISM_model')
    def _change_directory__make_model_specification_relative__translate_to_PRISM_model(self, object, name, old, new):
        directory, model_specification = os.path.split(self.model_specification_)
        try:
            if directory != '':
                self.directory = directory #TODO os.path.normpath(directory)
        except TraitError, e:
            logger.warn(e)
        try:
            # problem: model_specification is appearing relative to the previous
            # directory
            # solution (avoiding infinite loop):
            # first set it without notifying change handlers
            self.trait_setq(model_specification=model_specification)
            # second notify change handlers by setting it
            self.model_specification = model_specification
        except TraitError, e:
            logger.warn(e)
        self.translate_model_specification()
    
    # public method
    def translate_model_specification(self):
        ''' Performs an experiment with task='Translate' to generate the 
        PRISM model and modelParameters.xml from self.model_specification. '''
        self._translated = False
        if self.model_specification == '': return # guard
        from infobiotics.pmodelchecker.prism.prism_experiment import PRISMExperiment # avoids circular import    
        translate = PRISMExperiment(only_bind_executable=True, directory=self.directory)
        if self.model_checker != 'PRISM':
            PRISM_model = '__temp__'
        else:
            PRISM_model = self.PRISM_model_
        translate.trait_setq(# set quietly otherwise this triggers _model_specification_changed above
            model_specification=self.model_specification_,
            PRISM_model=PRISM_model, # must set PRISM_model with PRISM_model_ as trait_setq doesn't trigger creation of shadow trait 
            task='Translate',
        ) 
        if translate.perform(thread=False, expecting_no_output=True):
            self._translated = True
        if self.model_checker != 'PRISM':
            os.remove(translate.PRISM_model_)
#        self._model_specification_changed = True if name == 'model_specification' else False # needed by PModelCheckerParamsHandler.model_specification_changed


if __name__ == '__main__':
    execfile('prism/prism_experiment.py')
            
