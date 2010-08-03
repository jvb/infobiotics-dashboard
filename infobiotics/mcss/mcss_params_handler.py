import infobiotics # set up TraitsUI backend before traits imports
from enthought.traits.api import Trait
from infobiotics.core.params_handler import ParamsHandler
from mcss_params_group import mcss_params_group
from mcss_preferences import McssParamsPreferencesPage
import os.path

class McssParamsHandler(ParamsHandler):
    ''' Reformulates a few of traits of McssParams. '''

    preferences_page = McssParamsPreferencesPage() 
    
    def _params_group_default(self):
        return mcss_params_group
    
    id = 'McssParamsHandler'
    
    help_urls = [
        ('Quick start', 'http://www.infobiotics.org/infobiotics-workbench/quickStart/quickStart.html'),
        ('Tutorial','http://www.infobiotics.org/infobiotics-workbench/tutorial/modelSimulation.html'),
        ('Tutorial using SBML model specification', 'http://www.infobiotics.org/infobiotics-workbench/tutorial/tutorial_2.html'),
        ('Documentation','http://www.infobiotics.org/infobiotics-workbench/modelSimulation/modelSimulation.html'),
    ]
    
    model_format = Trait(
        'P system XML',
        {
            'P system XML'                 : 'xml',
            'SBML'                         : 'sbml',
        },
        desc='the model specification format',
    )
    
    model_format_reversed = {
        'xml'  : 'P system XML',
        'sbml' : 'SBML',
    }

    simulation_algorithm = Trait(
        'Direct Method with queue',
        {
            'Direct Method with queue'               : 'dmq',
            'Direct Method (Gillespie68)'            : 'dm',
            'Logarithmic Direct Method (Cao2007)'    : 'ldm',
            'Direct Method with growth and division' : 'dmgd',
            'Direct Method (Cellular Potts)'         : 'dmcp',
        },
        desc='the stochastic simulation algorithm to use',
    )

    simulation_algorithm_reversed = { # needed because we can't assign to simulation_algorithm_ #TODO this means traits_repr is probably wrong for Traits - but we use Enum in Params subclass so it doesn't matter
        'dmq'  : 'Direct Method with queue', 
        'dm'   : 'Direct Method (Gillespie68)',
        'ldm'  : 'Logarithmic Direct Method (Cao2007)',
        'dmgd' : 'Direct Method with growth and division',
        'dmcp' : 'Direct Method (Cellular Potts)',
    }

    def init(self, info):
        self.sync_trait('model_format_', info.object, alias='model_format', mutual=False) # doesn't sync mutually even if mutual=True, this just makes it explicit
        self.sync_trait('simulation_algorithm_', info.object, alias='simulation_algorithm', mutual=False) # ditto
        super(McssParamsHandler, self).init(info)

    def object_model_file_changed(self, info):
        ext = os.path.splitext(info.object.model_file)[1].lower() 
        if ext == '.sbml':
            self.model_format = 'SBML'
        else:
            self.model_format = 'P system XML'

    def object_model_format_changed(self, info):
        self.model_format = self.model_format_reversed[info.object.model_format]

    def object_simulation_algorithm_changed(self, info):
        self.simulation_algorithm = self.simulation_algorithm_reversed[info.object.simulation_algorithm]


if __name__ == '__main__':
    execfile('mcss_params.py')
    