from infobiotics.pmodelchecker.pmodelchecker_params import PModelCheckerParams  

class PRISMParams(PModelCheckerParams):

    _parameter_set_name = 'prism'

    model_checker = 'PRISM'
    model_specification = File(filter=['*.xml','*.lpp'], desc='the filename(.lpp) of the model to check') #TODO have multiple wildcards in one filter?
    PRISM_model = File('PRISM_model.sm', filter=['*.sm','*'],desc='the filename(.sm) of the intermediate PRISM model')
    _model_parameters = Instance(ModelParameters)
    def __model_parameters_default(self):
        return ModelParameters(prism_experiment=self)
    model_parameters = DelegatesTo('_model_parameters')
    temporal_formulas = File(desc='') #TODO desc
    formula_parameters = Str(desc='') #TODO PRISM-specific? desc
    task = Enum(['Approximate','Translate','Build','Verify'], desc='')  #TODO desc
#    confidence = Float(0.1, desc='the confidence level used when approximating the answer to a formula')
    confidence = Trait(
        '90% (0.1)',
        {
            '90% (0.1)' : '0.1',
            '95% (0.05)' : '0.05',
            '99% (0.01)' : '0.01',
            'custom' : '_custom_confidence',#TEST should be fixed in set_parameter_from_trait... in ParamsExperiment
        },
        desc='the confidence level used when approximating the answer to a formula'
    )
    _custom_confidence = Range(0.0, 1.0, 0.1, mode='text')
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
#            'model_checker',
            'model_specification',
            'PRISM_model',
            'model_parameters',
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





    def _PRISM_model_changed(self):
#        print 'PModelCheckerExperiment._PRISM_model_changed'
        try:
            with open(self.PRISM_model, 'r') as f:
                self._prism_model_str = f.read()
                self._prism_model_dirty = False
        except IOError, e:
            logger.error(e)

    _prism_model_dirty = Bool(False)
        
    _prism_model_str = Str

    def _prism_model_str_changed(self, value):
        self._prism_model_dirty = True
    
    _show_prism_model = Bool(False)
    
    edit_prism_model = Button

    def _edit_prism_model_fired(self):
        from enthought.traits.ui.api import View, Item, CodeEditor, TextEditor
        self.edit_traits(
            kind='nonmodal', 
            view=View(
                Item('_prism_model_str', 
                     style='custom',
                     editor=TextEditor()), 
                buttons=['OK','Revert','Undo','Redo'],
                resizable=True,
            ),
        )

#    _open_in_new_window = Button('TODO') # open in new text editor syncing? #TODO add to view
    
    generate_prism_model = Button
    
    def _generate_prism_model_fired(self): #TODO
        pass
        #TODO do some validation
#            path = self.path
        from tempfile import NamedTemporaryFile
        tmp = NamedTemporaryFile().name

        generate_experiment = PRISMExperiment(model_specification=self.model_specification, PRISM_model=self.PRISM_model, task='Translate')
        generate_experiment.save(tmp)
        generate_experiment.perform()
        
    def _temporal_formulas_changed(self):
        print 'got here'
        try:
            with open(self.temporal_formulas, 'r') as f: 
                _temporal_formulas_str = f.read()
                #TODO create TemporalFormula objects by parsing temporal_formulas
                
        except IOError:
            logger.error(e)
            
            
            
    def has_valid_parameters(self):
        ''' Tests parameter values and enables 'Perform' action if successful.
        
        '''
        from infobiotics.dashboard.shared.files import can_read, can_write

        #TODO switch on self.task?

        problems = []

        if not can_read(self.model_specification):
            problems.append('Model specification %s cannot be read' % self.model_specification)
        else:
            # further tests
            pass
            #TODO try and parse model_specification
        
        if self.number_samples < 1:
            problems.append('The number of samples must be greater than 1')
        
        #formula_parameters should have been moved to pmodelchecker...
                
        #TODO model_parameters
        print self.confidence, self.confidence_
        if not self.confidence < 0.5:
            problems.append('Confidence must be greater than 50% (less than 0.5)')
        
        if not self.precision > 0:
            problems.append('Precision must be greater than 0')
                
        if not can_write(self.results_file):
            problems.append('Results file %s cannot be written' % self.results_file)
        
        if not can_write(self.states_file):
            problems.append('States file %s cannot be written' % self.states_file)
                
        if not can_write(self.transitions_file):
            problems.append('Transitions file %s cannot be written' % self.transitions_file)
        
        if not can_write(self.parameters_file):
            problems.append('Parameters file %s cannot be written' % self.parameters_file)
        
        if not can_read(self.PRISM_model):
            problems.append('PRISM model %s cannot be read' % self.PRISM_model)
            #FIXME prints when changed from bad to good file!

        if not can_write(self.PRISM_model):
            problems.append('PRISM model %s cannot be written' % self.PRISM_model)

        #TODO more tests

        print problems, '\n'
        
#        self.perform_action.tooltip = 'OK'
        if len(problems) > 0:
            self.problem = '\n'.join(problems)
        else:
            self.problem = ''
#            # call superclass's validate method
#            return super(PRISMExperiment, self).has_valid_parameters()
            return True
        

    def perform(self):#*args, **kwargs):#TODO override traits here self.trait_setq(**kwargs)
        
        # if prism model doesn't exist quickly do a Translate to create it
        if not os.path.exists(os.path.abspath(self.prism_model)):
            task = self.task
            self.task = 'Translate' # always generates modelParamaters.xml
            #TODO parameter_names = ['model_specification','PRISM_model','task']
            super(PRISMExperiment, self).perform()
            self.task = task
            if not os.path.exists(self.prism_model):
                raise Exception('%s could not be created.' % self.prism_model)
        
        
        
        super(PRISMExperiment, self).perform()
                    