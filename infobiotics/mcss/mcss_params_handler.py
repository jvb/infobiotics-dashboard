from infobiotics.shared.api import ParamsHandler, Instance, Trait, ParamsView, Item
from mcss_params import McssParams 
from mcss_params_group import mcss_params_group

class McssParamsHandler(ParamsHandler):
    ''' Reformulates a few of traits of McssParams. '''

    _parameters = Instance(McssParams)

    id='McssParamsHandler' # for saving window position and size
    title='mcss parameters' # does this do anything?
        
    def parameters_model_file_changed(self, info):
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
    
    traits_view = ParamsView(
        Item('_cwd', label='Working directory', tooltip='Relative paths will be relative to this directory.'),
        '_',
        mcss_params_group,
    )
