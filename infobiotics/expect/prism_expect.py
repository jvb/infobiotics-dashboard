from infobiotics.dashboard.api import PModelCheckerExpect

class PRISMExpect(PModelCheckerExpect):
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

    view = View(
        HGroup(
            Item('status', show_label=False, style='readonly'),
        ),
        Item('property_progress'),
        Item('overall_progress'),
        Item('error_string', style='readonly', emphasized=True),
        resizable=True,
        id='PRISMExpect.view',
    )
    

if __name__ == '__main__':
    e = PRISMExpect(params_program='./expect_tester', params_file='./Const_PRISM.params.stdout', args=['0.1'])
#    e = PRISMExpect(['/home/jvb/src/pmodelchecker-0.0.7/examples/Const/modelCheckingPRISM/Const_PRISM.params'], task='Approximate')
    e.start()
    e.configure_traits()
    if hasattr(e, 'child'): 
        e.child.terminate(True)
