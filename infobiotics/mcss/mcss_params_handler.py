import infobiotics # set up TraitsUI backend before traits imports
from traits.api import Trait, Enum
from infobiotics.core.params_handler import ParamsHandler
from mcss_preferences import McssParamsPreferencesPage
import os.path


# We use Mapped Traits to give explanatory names to users and CLI parsable ones to mcss 
# see http://docs.enthought.com/traits/traits_user_manual/custom.html#mapped-traits

dmq2 = 'Multicompartment Gillespie Enhanced Queue'
dm = 'Multicompartment Gillespie Direct Method'
ode1 = 'ODE solver'
von_Neumann_neighbourhood = 'von Neumann (4: N, E, S, W)' 
RungeKutta4th = 'Explicit 4th order (classical) Runge-Kutta'
LatticePopulationPsystem = 'Lattice Population P system'

default_model_format = LatticePopulationPsystem
default_simulation_algorithm = dmq2
default_neighbourhood = von_Neumann_neighbourhood
default_ode_solver = RungeKutta4th

def reversedict(d):
	return dict((value, key) for key, value in d.iteritems())

model_formats = { 
	'Lattice Population P system' 	: 'lpp',
	'P system XML'				 	: 'xml',
	'SBML'						 	: 'sbml',
}
model_formats_reversed = reversedict(model_formats)

simulation_algorithms = {
# working
	dmq2 	: 'dmq2',
	dm 		: 'dm',

#	ode1 	: 'ode1',
	ode1 	: 'ode1',

## broken
#	'Multicompartment Gillespie Enhanced Queue with growth' 				: 'dmq2g',
#	'Multicompartment Gillespie Enhanced Queue with growth and division' 	: 'dmq2gd',
#	'Multicompartment Gillespie Logarithmic Direct Method' 					: 'ldm',
#	'Multicompartment Gillespie Direct Method Cellular Potts'				: 'dmcp',
#
## broken and obsolete
#	'Multicompartment Gillespie Queue'										: 'dmq',
#	'Multicompartment Gillespie Queue with growth' 							: 'dmqg',
#	'Multicompartment Gillespie Direct Method with growth and division' 	: 'dmgd',
}
simulation_algorithms_reversed = reversedict(simulation_algorithms)
## OrderedDict not recognized as dict by Trait factory method (uses Python's types module definition - which doesn't/can't include OrderedDict - when it should probably use isinstance)
#from collections import OrderedDict
#simulation_algorithms_reversed = OrderedDict([(dmq2,dmq2), (dm,dm), (ode1,ode)])
#simulation_algorithms = OrderedDict(reversed(simulation_algorithms_reversed))

neighbourhoods = { 
	von_Neumann_neighbourhood 					: '4',
	'Moore (8: N, NE, E, SE, S, SW, W, NW)' 	: '8',
}
neighbourhoods_reversed = reversedict(neighbourhoods)

ode_solvers_reversed = { 
#mcss/Psystem.cpp:159
#if((strcmp(parameters.simulation_algorithm, "ode1") == 0)) {
#	if((strcmp(parameters.ode_solver, "rk2") == 0))
#			simalg->setOdeSolver(gsl_odeiv_step_rk2);
#	if((strcmp(parameters.ode_solver, "rk4") == 0))
#			simalg->setOdeSolver(gsl_odeiv_step_rk4);
#	if((strcmp(parameters.ode_solver, "rkf45") == 0))
#			simalg->setOdeSolver(gsl_odeiv_step_rkf45);
#	if((strcmp(parameters.ode_solver, "rkck") == 0))
#			simalg->setOdeSolver(gsl_odeiv_step_rkck);
#	if((strcmp(parameters.ode_solver, "rk8pd") == 0))
#			simalg->setOdeSolver(gsl_odeiv_step_rk8pd);
#	if((strcmp(parameters.ode_solver, "rk2imp") == 0))
#			simalg->setOdeSolver(gsl_odeiv_step_rk2imp);
#	if((strcmp(parameters.ode_solver, "rk4imp") == 0))
#			simalg->setOdeSolver(gsl_odeiv_step_rk4imp);
#	if((strcmp(parameters.ode_solver, "bsimp") == 0))
#			simalg->setOdeSolver(gsl_odeiv_step_bsimp);
#	if((strcmp(parameters.ode_solver, "gear1") == 0))
#			simalg->setOdeSolver(gsl_odeiv_step_gear1);
#	if((strcmp(parameters.ode_solver, "gear2") == 0))
#			simalg->setOdeSolver(gsl_odeiv_step_gear2);
	'rk2' 		: 'Explicit embedded Runge-Kutta (2, 3) method',
	'rk4' 		: RungeKutta4th,
	'rkf45' 	: 'Explicit embedded Runge-Kutta-Fehlberg (4, 5) method',
	'rkck' 		: 'Explicit embedded Runge-Kutta Cash-Karp (4, 5) method',
	'rk8pd' 	: 'Explicit embedded Runge-Kutta Prince-Dormand (8, 9) method',
	'rk2imp' 	: 'Implicit Gaussian second order Runge-Kutta',
	'rk4imp' 	: 'Implicit Gaussian 4th order Runge-Kutt',
	'bsimp' 	: 'Implicit Bulirsch-Stoer method of Bader and Deuflhard',
	'gear1' 	: 'gsl_odeiv_step_gear1',
	'gear2' 	: 'gsl_odeiv_step_gear2',
}
ode_solvers = reversedict(ode_solvers_reversed)


class McssParamsHandler(ParamsHandler):
	''' Reformulates a few of traits of McssParams. '''

	preferences_page = McssParamsPreferencesPage()

	def _params_group_default(self):
		from mcss_params_group import mcss_params_group
		return mcss_params_group

	id = 'McssParamsHandler'

	help_urls = [
		('Quick start', 'http://www.infobiotics.org/infobiotics-workbench/quickStart/quickStart.html'),
		('Tutorial', 'http://www.infobiotics.org/infobiotics-workbench/tutorial/modelSimulation.html'),
		('Tutorial using SBML model specification', 'http://www.infobiotics.org/infobiotics-workbench/tutorial/tutorial_2.html'),
		('Documentation', 'http://www.infobiotics.org/infobiotics-workbench/modelSimulation/modelSimulation.html'),
	]

	model_format = Trait(
		default_model_format,
		model_formats,
		desc='the model specification format',
	)

	simulation_algorithm_type = Enum('stochastic-discrete', 'deterministic-continuous')

	def _simulation_algorithm_type_changed(self):
		if self.simulation_algorithm_type == 'deterministic-continuous':
			self.simulation_algorithm = ode1
		else:
			self.simulation_algorithm = default_simulation_algorithm#simulation_algorithms_reversed[self.model.simulation_algorithm]

	simulation_algorithm = Trait(
		default_simulation_algorithm,
		simulation_algorithms,
		desc='the stochastic simulation algorithm to use',
	)

	ode_solver = Trait(
		default_ode_solver,
		ode_solvers,
		desc='the ODE solver to use (from the GNU Scientific Library)',
	)

	neighbourhood = Trait(
		default_neighbourhood,#'4',
		neighbourhoods,
		desc='the neighbourhood for non-vector transport rules',
	)

	def init(self, info):
		super(McssParamsHandler, self).init(info)
		
		# remember traits
		model_format = info.object.model_format
		simulation_algorithm = info.object.simulation_algorithm
		ode_solver = info.object.ode_solver
		neighbourhood = info.object.neighbourhood

		# remember dirty
		dirty = info.object._dirty

		self.sync_trait('model_format_', info.object, alias='model_format', mutual=False) # doesn't sync mutually even if mutual=True, this just makes it explicit
		self.sync_trait('simulation_algorithm_', info.object, alias='simulation_algorithm', mutual=False) # ditto
		self.sync_trait('ode_solver_', info.object, alias='ode_solver', mutual=False)
		self.sync_trait('neighbourhood_', info.object, alias='neighbourhood', mutual=False)

		# reset traits
		info.object.model_format = model_format
		info.object.simulation_algorithm = simulation_algorithm
		info.object.ode_solver = ode_solver
		info.object.neighbourhood = neighbourhood

		# reset dirty 
		info.object._dirty = dirty

	def object_model_file_changed(self, info):
		ext = os.path.splitext(info.object.model_file)[1].lower()
		# quietly set traits
		if ext == '.sbml':
			self.trait_setq(model_format='SBML')#self.model_format = 'SBML'
		else:
			self.trait_setq(model_format=LatticePopulationPsystem)#self.model_format = LatticePopulationPsystem 

	def object_model_format_changed(self, info):
		self.model_format = model_formats_reversed[info.object.model_format]

	def object_simulation_algorithm_changed(self, info):
		self.simulation_algorithm = simulation_algorithms_reversed[info.object.simulation_algorithm]

	def object_ode_solver_changed(self, info):
		self.ode_solver = ode_solvers_reversed[info.object.ode_solver]

	def object_neighbourhood_changed(self, info):
		self.neighbourhood = neighbourhoods_reversed[info.object.neighbourhood]
		

if __name__ == '__main__':
	execfile('mcss_params.py')
