from enthought.traits.api import HasTraits, Int, Float
from enthought.traits.ui.api import View, Item
from infobiotics.dashboard.api import ParamsExpect, error_string_group


mcss_expect_view = View(
    Item('run', style='readonly'),
    Item('time_in_run', style='readonly'),
    error_string_group,
    width=300
)

    
class Parameters(HasTraits): pass


class McssParameters(Parameters):
    def __init__(self, params_file=None, **traits):
        if params_file is not None:
            self.load(params_file)
        super(McssParameters, self).__init__(**traits)

    
class McssExpect(ParamsExpect):
    pattern_list = [
        '[0-9]+ [0-9]+', # 'time_in_run, run'
    ] 
    params_program = 'mcss'

#    parameters = McssParameters
    def params_file_changed(self, params_file):
#        self.parameters = McssParameters(params_file)
        parameters = McssParameters(params_file)
        self.runs = parameters.runs
        self.max_time = parameters.max_time
    
    run = Int
    time_in_run = Float
    #TODO percentage progress using run, runs, time_in_run and max_time
    
    traits_view = mcss_expect_view
    
    def pattern_matched(self, pattern_index, match):
        if pattern_index == 0: # '1 20.5'
            time_in_run, run = match.split(' ')
            self.run = int(run)
            self.time_in_run = float(time_in_run)
        else:
            super(McssExpect, self).pattern_matched(pattern_index, match)


if __name__ == '__main__':
    e = McssExpect(params_file='/home/jvb/src/mcss-0.0.35-0.0.35/examples/models/reactions1.params', args=['show_progress=true', 'max_time=1000'])
    e.start()
    e.configure_traits()
    if hasattr(e, 'child'): 
        e.child.terminate(True)
        