from infobiotics.common.api import ParamsHandler
from poptimizer_params_group import poptimizer_params_group
from enthought.traits.api import Trait

class POptimizerParamsHandler(ParamsHandler):

    def _params_group_default(self):
        return poptimizer_params_group
    
    id = 'POptimizerParamsHandler'

    help_urls = [
        ('Documentation','http://www.infobiotics.org/infobiotics-workbench/optimisation/optimisation_Claudio.html'),
    ]
    
    filters = [ # used to create wildcard and filter traits for FileDialog and OpenFileDialog respectively
        ('Experiment parameters', ['*.params','*.xml']), 
        ('All files', ['*']),
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
#        'Direct Method with queue',
#        {
#            'Direct Method with queue'               : 'dmq',
#            'Direct Method (Gillespie68)'            : 'dm',
#            'Logarithmic Direct Method (Cao2007)'    : 'ldm',
#            'Direct Method with growth and division' : 'dmgd',
#            'Direct Method (Cellular Potts)'         : 'dmcp',
#        },
#        desc='the stochastic simulation algorithm to use',
#    )
#
#    simulation_algorithm_reversed = { # needed because we can't assign to simulation_algorithm_ #TODO this means traits_repr is probably wrong for Traits - but we use Enum in Params subclass so it doesn't matter
#        'dmq'  : 'Direct Method with queue', 
#        'dm'   : 'Direct Method (Gillespie68)',
#        'ldm'  : 'Logarithmic Direct Method (Cao2007)',
#        'dmgd' : 'Direct Method with growth and division',
#        'dmcp' : 'Direct Method (Cellular Potts)',
#    }
#
#    def init(self, info):
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
    execfile('poptimizer_params.py')
    
