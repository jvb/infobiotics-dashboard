from infobiotics.dashboard.api import PModelCheckerExpect, error_string_group 
from enthought.traits.api import View, Item

mc2_expect_view = View(
    Item('status', style='readonly'),
    Item('simulation'),
    error_string_group,
)                      


class MC2Expect(PModelCheckerExpect):
    pattern_list = [
        'Running mcss',
        'Simulation number [0-9]+ of [0-9]+', # previously 'Generating simulations in MC2 format'
        'Running MC2',
    ]
        
    def pattern_matched(self, pattern_index, match):
        if pattern_index == 0:
            self.status = match
        elif pattern_index == 1:
            head, tail = match.split(' of ')
#            self.max_simulation = int(tail) # see below
            self.simulation = int(head.split('Simulation number ')[1])
        elif pattern_index == 2:
            self.status = match
        else:
            ParamsExpect.pattern_matched(self, pattern_index, match)
    
#    parameters = MC2Parameters
    def params_file_changed(self, params_file):
#        self.parameters = MC2Parameters(params_file)
        parameters = MC2Parameters(params_file)
        self.max_simulation = parameters.number_samples
        self.max_simulation = McssParameters(parameters.mcss_params_file).runs
        
    status = Str
    min_simulation = Int(0) # because Range(0, 'max_simulation') which raises: "TypeError: unsupported operand type(s) for -: 'int' and 'code'"
    max_simulation = Int(1)
    simulation = Range('min_simulation', 'max_simulation')

    view = View(
        Item('status', style='readonly'),
        Item('simulation'),
        error_string_group,
    )


if __name__ == '__main__':
    e = MC2Expect(params_program='./expect_tester', params_file='./Const_MC2.params.stdout', args=['0.00001'], max_simulation=10000)
#    e = MC2Expect(['/home/jvb/src/pmodelchecker-0.0.7/examples/Const/modelCheckingMC2/Const_MC2.params'])
    e.start()
    e.configure_traits()
    if hasattr(e, 'child'): 
        e.child.terminate(True)
        