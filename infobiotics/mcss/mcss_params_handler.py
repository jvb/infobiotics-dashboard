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
        ('Tutorial', 'http://www.infobiotics.org/infobiotics-workbench/tutorial/modelSimulation.html'),
        ('Tutorial using SBML model specification', 'http://www.infobiotics.org/infobiotics-workbench/tutorial/tutorial_2.html'),
        ('Documentation', 'http://www.infobiotics.org/infobiotics-workbench/modelSimulation/modelSimulation.html'),
    ]

    model_format = Trait(
        'Lattice Population P system',
        {
            'Lattice Population P system'  : 'lpp',
            'P system XML'                 : 'xml',
            'SBML'                         : 'sbml',
        },
        desc='the model specification format',
    )

    model_format_reversed = {
        'lpp'  : 'Lattice Population P system',
        'xml'  : 'P system XML',
        'sbml' : 'SBML',
    }

    simulation_algorithm = Trait(
        'Multicompartment Gillespie Enhanced Queue',
        {
            'Multicompartment Gillespie Direct Method'                           : 'dm',
#            'Multicompartment Gillespie Logarithmic Direct Method'               : 'ldm',
            'Multicompartment Gillespie Queue'                                   : 'dmq',
            'Multicompartment Gillespie Enhanced Queue'                          : 'dmq2',
            'Multicompartment Gillespie Direct Method with growth and division'  : 'dmgd',
            'Multicompartment Gillespie Direct Method Cellular Potts'            : 'dmcp',
            'Multicompartment Gillespie Queue with growth'                       : 'dmqg',
            'Multicompartment Gillespie Enhanced Queue with growth'              : 'dmq2g',
            'Multicompartment Gillespie Enhanced Queue with growth and division' : 'dmq2gd',
        },
        desc='the stochastic simulation algorithm to use',
    )

    simulation_algorithm_reversed = { # needed because we can't assign to simulation_algorithm_ #TODO this means traits_repr is probably wrong for Traits - but we use Enum in Params subclass so it doesn't matter
        'dm'     : 'Multicompartment Gillespie Direct Method',
#        'ldm'    : 'Multicompartment Gillespie Logarithmic Direct Method',
        'dmq'    : 'Multicompartment Gillespie Queue',
        'dmq2'   : 'Multicompartment Gillespie Enhanced Queue',
        'dmgd'   : 'Multicompartment Gillespie Direct Method with growth and division',
        'dmcp'   : 'Multicompartment Gillespie Direct Method Cellular Potts',
        'dmqg'   : 'Multicompartment Gillespie Queue with growth',
        'dmq2g'  : 'Multicompartment Gillespie Enhanced Queue with growth',
        'dmq2gd' : 'Multicompartment Gillespie Enhanced Queue with growth and division',
    }

    def init(self, info):
        super(McssParamsHandler, self).init(info)
        
        # remember traits
        model_format = info.object.model_format
        simulation_algorithm = info.object.simulation_algorithm

        # remember dirty
        dirty = info.object._dirty

        self.sync_trait('model_format_', info.object, alias='model_format', mutual=False) # doesn't sync mutually even if mutual=True, this just makes it explicit
        self.sync_trait('simulation_algorithm_', info.object, alias='simulation_algorithm', mutual=False) # ditto

        # reset traits
        info.object.model_format = model_format
        info.object.simulation_algorithm = simulation_algorithm
        
        # reset dirty 
        info.object._dirty = dirty

    def object_model_file_changed(self, info):
        ext = os.path.splitext(info.object.model_file)[1].lower()
        # quietly set traits
        if ext == '.sbml':
            self.trait_setq(model_format='SBML')#self.model_format = 'SBML'
        else:
            self.trait_setq(model_format='Lattice Population P system')#self.model_format = 'Lattice Population P system' 

    def object_model_format_changed(self, info):
        self.model_format = self.model_format_reversed[info.object.model_format]

    def object_simulation_algorithm_changed(self, info):
        self.simulation_algorithm = self.simulation_algorithm_reversed[info.object.simulation_algorithm]


if __name__ == '__main__':
    execfile('mcss_params.py')
