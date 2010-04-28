from infobiotics.pmodelchecker.api import PModelCheckerExperiment, PRISMParams
from infobiotics.shared.api import Enum, Property, Str, Int, Range, Bool

class PRISMExperiment(PModelCheckerExperiment, PRISMParams):

    def _handler_default(self):
        from infobiotics.pmodelchecker.prism_experiment_handler import PRISMExperimentHandler
        return PRISMExperimentHandler(model=self)

    pattern_list = [
        '[0-9]+ properties:', # '2 properties:',
        'Simulating: .+\]',
        '[0-9]+%',
        'Sampling complete: [0-9]+ iterations in [0-9]+[.][0-9]+ seconds \(average [0-9]+[.][0-9]+\)', # 'Sampling complete: 10000 iterations in 234.15 seconds (average 0.023415)',
        'Exception in thread "main" java',
#        'Parsing model file ".+"...', # 'Parsing model file "constitutive.sm"...',
#        'Parsing properties file ".+"...', # 'Parsing properties file "formulas.temp"...',
#        'Exporting results to file ".+"...', # 'Exporting results to file "Const_results.psm"...',
    ]
        
    def pattern_matched(self, pattern_index, match):
        if pattern_index == 0:
            self.max_properties = int(match.split(' properties:')[0])
        elif pattern_index == 1:
            self.current_property = match.split('Simulating: ')[1].strip()
        elif pattern_index == 2:
            self.property_progress = int(match.strip('%'))
        elif pattern_index == 3:
            self.property_index += 1
        elif pattern_index == 4:
            self.error_string = match
        elif pattern_index > 4:
            ParamsExpect.pattern_matched(self, pattern_index, match)

    task = Enum(['Translate', 'Approximate', 'Verify', 'Build'])
    status = Property(Str, depends_on='current_property')
    current_property = Str
    max_properties = Int(1)
    property_index = Int(0)
    property_progress = Range(0, 100)
    overall_progress = Property(Range(0.0, 100.0), depends_on='property_progress, property_index, max_properties')

    def _get_status(self):
        #TODO use self.parameters.task
        if self.task == 'Approximate':
            return 'Approximating %s' % self.current_property
        elif self.task == 'Verify':
            return 'Verifying %s' % self.current_property
        elif self.task == 'Build':
            return 'Building PRISM model'
        elif self.task == '...':
            return '...'
        
    def _get_overall_progress(self):
         subtotal = self.property_progress + (100 * self.property_index)
         total = 100 * self.max_properties
         return float((subtotal / total) * 100)

#    view = View(
#        HGroup(
#            Item('status', show_label=False, style='readonly'),
#        ),
#        Item('property_progress'),
#        Item('overall_progress'),
#        Item('error_string', style='readonly', emphasized=True),
#        resizable=True,
#        id='PRISMExpect.view',
#    )

    has_valid_parameters = Property(Bool)
    
    def _get_has_valid_parameters(self):
        errors = not super(PRISMExperiment, self).has_valid_parameters
        print 'errors =', errors
        print self.has_valid_parameters()
            
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



if __name__ == '__main__':
    PRISMExperiment().configure()
    