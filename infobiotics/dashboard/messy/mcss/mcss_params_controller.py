from infobiotics.dashboard.mcss.api import mcss_params_controller_group
from infobiotics.dashboard.params.api import ParamsController, load_save_actions#, params_view
from enthought.traits.api import Trait, Instance
from enthought.traits.ui.api import View, Group, Item
import os.path

class McssParamsController(ParamsController):
    ''' Reformulates a few of traits of McssParams. '''

    id='mcss_params_controller' # for saving window position and size
    title='mcss parameters'
#    content = mcss_params_controller_group # doesn't work!

    def _content_default(self):
        return mcss_params_controller_group
        
    def object_params_file_changed(self, info):
        if info.initialized:
            info.ui.title = os.path.basename(info.object.params_file)
    
    def __init__(self, model=None, **metadata):
        ''' Initializes the object and sets the model, creating one if None 
        supplied. '''
        if model == None:
            from mcss_params import McssParams
            model = McssParams()
        super(McssParamsController, self).__init__(model, **metadata)
    
    def object_model_file_changed(self, info):
        import os.path
        if os.path.splitext(info.object.model_file)[1].lower() == '.sbml':
            self.model_format_ = 'sbml'
    
    model_format = Trait(
        'P system XML',
        {
            'P system XML'                 : 'xml',
            'SBML'                         : 'sbml',
#            'Lattice population P system'  : 'lpp',
        },
        desc='the model specification format',
    )

    def _model_format_changed(self, model_format):
        self.sync_trait('model_format_', self.model, alias='model_format')

    simulation_algorithm = Trait(
        'Direct Method with queue',
        {
            'Direct Method with queue'               : 'dmq',
            'Direct Method (Gillespie68)'            : 'dm',
            'Logarithmic Direct Method (Cao2007)'    : 'ldm',
            'Direct Method with growth and division' : 'dmgd',
            'Direct Method (Cellular Potts)'         : 'dmcp',
        },
        desc='the stochastic simulation algorithm to use'
    )

    def _simulation_algorithm_changed(self, simulation_algorithm):
        self.sync_trait('simulation_algorithm_', self.model, alias='simulation_algorithm')


if __name__ == '__main__':
    from enthought.traits.ui.api import Group, Item
    self = McssParamsController() 
#    self = McssParamsController(content=Group(Item('controller.id')))
#    McssParamsController(model=McssParams()).configure_traits()
    self.configure_traits()
    