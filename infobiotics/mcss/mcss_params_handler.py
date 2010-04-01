from infobiotics.shared.api import ParamsHandler, Trait
from infobiotics.mcss.api import mcss_params_view

class McssParamsHandler(ParamsHandler):
    ''' Reformulates a few of traits of McssParams. '''

    traits_view = mcss_params_view
    id='McssParamsHandler' # for saving window position and size
    
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

    def object_model_file_changed(self, info):
        import os.path
        ext = os.path.splitext(info.object.model_file)[1].lower() 
#        print ext
        if ext == '.sbml':
            info.object.model_format_ = 'sbml'

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
