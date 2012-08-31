import infobiotics # set up TraitsUI backend before traits imports
from traits.api import Trait
from infobiotics.core.params_handler import ParamsHandler
from mcsscmaes_params_group import mcsscmaes_params_group
from mcsscmaes_preferences import McssCmaesParamsPreferencesPage
import os.path

class McssCmaesParamsHandler(ParamsHandler):
    ''' Reformulates a few of traits of McssCmaesParams. '''

    preferences_page = McssCmaesParamsPreferencesPage()

    def _params_group_default(self):
        return mcsscmaes_params_group

    id = 'McssCmaesParamsHandler'

    help_urls = [
#        ('Quick start', 'http://www.infobiotics.org/infobiotics-workbench/quickStart/quickStart.html'),
#        ('Tutorial', 'http://www.infobiotics.org/infobiotics-workbench/tutorial/modelSimulation.html'),
#        ('Tutorial using SBML model specification', 'http://www.infobiotics.org/infobiotics-workbench/tutorial/tutorial_2.html'),
#        ('Documentation', 'http://www.infobiotics.org/infobiotics-workbench/modelSimulation/modelSimulation.html'),
    ]

#    model_format = Trait(
#        'P system XML',
#        {
#            'P system XML'                 : 'xml',
#            'SBML'                         : 'sbml',
#        },
#        desc='the model specification format',
#    )
#
#    model_format_reversed = {
#        'xml'  : 'P system XML',
#        'sbml' : 'SBML',
#    }
#
#    simulation_algorithm = Trait(
#        'Multicompartment Gillespie Enhanced Queue',
#        {
#            'Multicompartment Gillespie Direct Method'                           : 'dm',
##            'Multicompartment Gillespie Logarithmic Direct Method'               : 'ldm',
#            'Multicompartment Gillespie Queue'                                   : 'dmq',
#            'Multicompartment Gillespie Enhanced Queue'                          : 'dmq2',
#            'Multicompartment Gillespie Direct Method with growth and division'  : 'dmgd',
#            'Multicompartment Gillespie Direct Method Cellular Potts'            : 'dmcp',
#            'Multicompartment Gillespie Queue with growth'                       : 'dmqg',
#            'Multicompartment Gillespie Enhanced Queue with growth'              : 'dmq2g',
#            'Multicompartment Gillespie Enhanced Queue with growth and division' : 'dmq2gd',
#        },
#        desc='the stochastic simulation algorithm to use',
#    )
#
#    simulation_algorithm_reversed = { # needed because we can't assign to simulation_algorithm_ #TODO this means traits_repr is probably wrong for Traits - but we use Enum in Params subclass so it doesn't matter
#        'dm'     : 'Multicompartment Gillespie Direct Method',
##        'ldm'    : 'Multicompartment Gillespie Logarithmic Direct Method',
#        'dmq'    : 'Multicompartment Gillespie Queue',
#        'dmq2'   : 'Multicompartment Gillespie Enhanced Queue',
#        'dmgq'   : 'Multicompartment Gillespie Direct Method with growth and division',
#        'dmcp'   : 'Multicompartment Gillespie Direct Method Cellular Potts',
#        'dmqg'   : 'Multicompartment Gillespie Queue with growth',
#        'dmq2g'  : 'Multicompartment Gillespie Enhanced Queue with growth',
#        'dmq2gd' : 'Multicompartment Gillespie Enhanced Queue with growth and division',
#    }
#
#    def init(self, info):
#        super(McssCmaesParamsHandler, self).init(info)
#        self.sync_trait('model_format_', info.object, alias='model_format', mutual=False) # doesn't sync mutually even if mutual=True, this just makes it explicit
#        self.sync_trait('simulation_algorithm_', info.object, alias='simulation_algorithm', mutual=False) # ditto
#
#    def object_model_file_changed(self, info):
#        ext = os.path.splitext(info.object.model_file)[1].lower()
#        if ext == '.sbml':
#            self.model_format = 'SBML'
#        else:
#            self.model_format = 'P system XML'
#
#    def object_model_format_changed(self, info):
#        self.model_format = self.model_format_reversed[info.object.model_format]
#
#    def object_simulation_algorithm_changed(self, info):
#        self.simulation_algorithm = self.simulation_algorithm_reversed[info.object.simulation_algorithm]


if __name__ == '__main__':
    execfile('mcsscmaes_params.py')
