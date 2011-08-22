import infobiotics # set up TraitsUI backend before traits imports
from enthought.traits.api import Trait, Int
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
            'Deterministic solver'  : 'ode1',
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
        'ode1'  : 'Deterministic solver',
        'dm'    : 'Multicompartment Gillespie Direct Method',
        'ldm'   : 'Multicompartment Gillespie Logarithmic Direct Method',
        'dmq'   : 'Multicompartment Gillespie Queue',
        'dmq2'  : 'Multicompartment Gillespie Enhanced Queue',
        'dmgd'  : 'Multicompartment Gillespie Direct Method with growth and division',
        'dmcp'  : 'Multicompartment Gillespie Direct Method Cellular Potts',
        'dmqg'  : 'Multicompartment Gillespie Queue with growth',
        'dmq2g' : 'Multicompartment Gillespie Enhanced Queue with growth',
        'dmq2gd': 'Multicompartment Gillespie Enhanced Queue with growth and division',
    }

    ode_solver = Trait(
        'gsl_odeiv_step_rk2',
        {
            'gsl_odeiv_step_rk2'   : 'rk2',
            'gsl_odeiv_step_rk4'   : 'rk4',
            'gsl_odeiv_step_rkf45' : 'rkf45',
            'gsl_odeiv_step_rkck'  : 'rkck',
            'gsl_odeiv_step_rk8pd' : 'rk8pd',
            'gsl_odeiv_step_rk2imp': 'rk2imp',
            'gsl_odeiv_step_rk4imp': 'rk4imp',
            'gsl_odeiv_step_bsimp' : 'bsimp',
            'gsl_odeiv_step_gear1' : 'gear1',
            'gsl_odeiv_step_gear2' : 'gear2',
        },
        desc='the ODE solver to use',
    )

    ode_solver_reversed = {
        'rk2'   : 'gsl_odeiv_step_rk2',
        'rk4'   : 'gsl_odeiv_step_rk4',
        'rkf45' : 'gsl_odeiv_step_rkf45',
        'rkck'  : 'gsl_odeiv_step_rkck',
        'rk8pd' : 'gsl_odeiv_step_rk8pd',
        'rk2imp': 'gsl_odeiv_step_rk2imp',
        'rk4imp': 'gsl_odeiv_step_rk4imp',
        'bsimp' : 'gsl_odeiv_step_bsimp',
        'gear1' : 'gsl_odeiv_step_gear1',
        'gear2' : 'gsl_odeiv_step_gear2',
    }
    """
    mcss/Psystem.cpp:159
    if((strcmp(parameters.simulation_algorithm, "ode1") == 0)) {
        if((strcmp(parameters.ode_solver, "rk2") == 0))
                simalg->setOdeSolver(gsl_odeiv_step_rk2);
        if((strcmp(parameters.ode_solver, "rk4") == 0))
                simalg->setOdeSolver(gsl_odeiv_step_rk4);
        if((strcmp(parameters.ode_solver, "rkf45") == 0))
                simalg->setOdeSolver(gsl_odeiv_step_rkf45);
        if((strcmp(parameters.ode_solver, "rkck") == 0))
                simalg->setOdeSolver(gsl_odeiv_step_rkck);
        if((strcmp(parameters.ode_solver, "rk8pd") == 0))
                simalg->setOdeSolver(gsl_odeiv_step_rk8pd);
        if((strcmp(parameters.ode_solver, "rk2imp") == 0))
                simalg->setOdeSolver(gsl_odeiv_step_rk2imp);
        if((strcmp(parameters.ode_solver, "rk4imp") == 0))
                simalg->setOdeSolver(gsl_odeiv_step_rk4imp);
        if((strcmp(parameters.ode_solver, "bsimp") == 0))
                simalg->setOdeSolver(gsl_odeiv_step_bsimp);
        if((strcmp(parameters.ode_solver, "gear1") == 0))
                simalg->setOdeSolver(gsl_odeiv_step_gear1);
        if((strcmp(parameters.ode_solver, "gear2") == 0))
                simalg->setOdeSolver(gsl_odeiv_step_gear2);
    """

    def init(self, info):
        super(McssParamsHandler, self).init(info)
        
        # remember traits
        model_format = info.object.model_format
        simulation_algorithm = info.object.simulation_algorithm
        ode_solver = info.object.ode_solver

        # remember dirty
        dirty = info.object._dirty

        self.sync_trait('model_format_', info.object, alias='model_format', mutual=False) # doesn't sync mutually even if mutual=True, this just makes it explicit
        self.sync_trait('simulation_algorithm_', info.object, alias='simulation_algorithm', mutual=False) # ditto
        self.sync_trait('ode_solver_', info.object, alias='ode_solver', mutual=False)

        # reset traits
        info.object.model_format = model_format
        info.object.simulation_algorithm = simulation_algorithm
        info.object.ode_solver = ode_solver

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
#        if old != 'ode1' and new == 'ode1':
#            self._runs = self.runs
#            self.runs = 1
#        elif old=='ode1' and new != 'ode1':
#            self.runs = self._runs 

    _runs = Int(1)

    def object_ode_solver_changed(self, info):
        self.ode_solver = self.ode_solver_reversed[info.object.ode_solver]


if __name__ == '__main__':
    execfile('mcss_params.py')
