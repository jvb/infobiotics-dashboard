from infobiotics.shared.api import Params, Enum, Str, File, Long, Float

class PModelCheckerParams(Params):
    ''' Traits common to PRISMParams and MC2Params. '''
    
    _parameters_name = 'pmodelchecker'

    model_checker = Enum(['PRISM','MC2'], desc='the name of the model checker to use, PRISM or MC2')

    model_specification = File(readable=True, filter=['Lattice Population P systems (*.lpp)','All files (*)'], desc='name of the file containing the model specification as an LPP-system')
    positions = Str('all', desc="a string stating the positions of the P systems under study.\nThe format of the string is the following: 'x_1,y_1:x_2,y_2: ... :x_n,y_n'")
    molecular_species = Str('all', desc="a string stating the name of the molecular species under study.\nThe format of the string is the following: 'moleculeName_1,moleculeName_2, ...,moleculeName_n'")

    temporal_formulas = File(writable=True, desc='the name of the file containing the temporal logic formulas formalising the properties to check')
    formula_parameters = Str(desc="a string stating the values of the parameters in the formulas as follows:\n'param=lb:ub:s,param=lb:ub:s, ...' where lb is the lower bound, up is the upper bound and s is the step.\nParameters with a single value can also be specified as follows:\n'param=value,param=value, ...'")

    number_samples = Long(desc='the number of simulations to generate when taking an approximate or simulative approach to model checking')
    precision = Float(1.0, desc='the precision to achieve with respect to a real value when generating an estimate using approximate or simulative model checking')
    confidence = Float(0.1, desc='the confidence to achieve with respect to a real value when generating an estimate using approximate or simulative model checking')

    results_file = File('results.txt', desc='the name of the file to write the answers to the temporal logic formulas generated by the model checker')

    def _model_specification_changed(self):
        self.translate_model_specification()

    def translate_model_specification(self, dir, model_specification, PRISM_model=''):
        ''' Performs an experiment with task='Translate' to generate the 
        PRISM model and modelParameters.xml from LPP model specification. '''
        import tempfile
        if PRISM_model == '':
            PRISM_model_temp_file = tempfile.NamedTemporaryFile(dir=dir)
            PRISM_model = PRISM_model_temp_file.name
            
        from infobiotics.pmodelchecker.api import PRISMExperiment
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
    execfile('prism_params.py')
    