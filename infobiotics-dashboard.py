#!/usr/bin/env python
# THIS FILE IS AUTOMATICALLY CREATED
'''Single entry-point for Infobiotics Workbench.

With zero arguments it launches the Infobiotics Workbench/Dashboard (Envisage Workbench), 
with one argument it launches the individual experiment/command GUI (e.g. 'McssExperiment().configure()') and
with two arguments it launches the experiment and either sets the model_file/model_specification trait or loads the parameters from the second argument.

Having a single entry-point means it can be frozen (py2exe, py2app, etc.) and
called from Eclipse...
'''

from __future__ import with_statement


# bbfreeze
import py2imports


# "Application asked to unregister timer 0x1c000011 which is not registered in this thread. Fix application."
# This is a bug in Qt 4.7 under Ubuntu that will be fixed in Qt 4.8 


import sys
import os.path

from traits.trait_errors import TraitError

#import infobiotics.qstring

simulate = 'mcss'#'simulate'
simulation_results = 'mcss-results'
check_mc2 = 'pmodelchecker-mc2'#'check-mc2'
check_prism = 'pmodelchecker-prism'#'check-prism'
checking_results = 'pmodelchecker-results'
optimise = 'poptimizer'#optimise
optimisation_results = 'poptimizer-results' 
commands = (simulate, simulation_results, check_mc2, check_prism, checking_results, optimise, optimisation_results)


executable = sys.argv[0]
#executable = os.path.abspath(executable)
if os.path.splitext(executable)[1].lower() in ('.exe','') :
	executable = executable.strip('.exe')
else:
	executable = 'python ' + executable

import warnings
with warnings.catch_warnings():
	warnings.simplefilter("ignore")
	from infobiotics import version
	
def usage():
	return '''Infobiotics Workbench {version}

{executable} [command [file]]

commands:
 {commands_}
 
file types:
 .params ({simulate}, {check_prism}, {check_mc2}, {optimise}, {optimisation_results})  
 .sbml, .lpp, .xml ({simulate}, {check_prism}, {check_mc2})
 .h5 ({simulation_results})
 .mc2, .psm ({checking_results})
'''.format(
	commands_='\n '.join(commands),
	**globals()
)

def exit(message, exit_code=1):
	if os.isatty(sys.stdout.fileno()):
		print message
		sys.exit(exit_code)
	from PyQt4.QtGui import QApplication, QMessageBox
	app = QApplication([])
	QMessageBox.warning(None, 'Missing dependency', message, buttons=QMessageBox.Ok, defaultButton=QMessageBox.Ok)
	sys.exit(exit_code)

def missing_executable(executable):
	message =  ''
	message += 'Problem with Infobiotics Workbench installation: '
	message += '\n executable "{executable}" not found in PATH. '.format(executable=executable if not sys.platform == 'win32' else executable+'.exe')
	message += '\nUpdate PATH or reinstall.'
#	message += 'PATH="{PATH}"'.format(PATH=os.environ['PATH'])
	exit(message)

from infobiotics.thirdparty.which import which, WhichError
try:
	mcss = which('mcss')
#	print mcss
#	raise WhichError() # test
except WhichError:
	missing_executable('mcss')


def main(argv):
	args = argv[1:]
	
	try:
		if len(args) == 0:
			
#			import setproctitle
#			setproctitle.setproctitle('Infobiotics Dashboard')
					
			from infobiotics.dashboard import run
			exitcode = run.main()
			sys.exit(exitcode)
		
		command = args[0].lower()

		if len(args) > 2 or command.lower() not in commands:
			exit(usage(), 2)

		params = ''
		model = ''
		results = ''
		
		if len(args) == 2:
			args1 = args[1]
			if not os.path.exists(args1):
				sys.exit("The file '%s' does not exist" % args1)
			if not os.path.isabs(args1):
				args1 = os.path.normpath(os.path.join(os.getcwd(), args1))
			if args1.lower().endswith('.params'):
				params = args1
			elif args1.lower().endswith('.lpp'):
				model = args1
			elif command == simulate and args1.lower().endswith('.sbml'):
				# mcss accepts SBML models too
				model = args1
			elif command == simulation_results and args1.lower().endswith('.h5'):
				results = args1
			elif command == checking_results and args1.lower().rsplit('.')[1] in ('mc2', 'psm'):
				results = args1

		if model:
			directory, model = os.path.split(model)
		
		if command == simulation_results:
			from infobiotics.mcss.results import mcss_results_widget
			return mcss_results_widget.main(results)

		if command == checking_results:
			if results:
				from infobiotics.pmodelchecker.pmodelchecker_results import PModelCheckerResults
				return PModelCheckerResults(results).configure()
			else:
				sys.exit(usage())
		
		if command == optimisation_results:
			if params:
				from infobiotics.poptimizer.poptimizer_experiment import POptimizerExperiment
				from infobiotics.poptimizer.poptimizer_results import POptimizerResults
				return POptimizerResults(experiment=POptimizerExperiment(params)).configure()
			else:
				sys.exit(usage())
				
		if command == simulate:
			from infobiotics.mcss.mcss_experiment import McssExperiment as Experiment #@UnusedImport
		elif command == check_mc2:
			from infobiotics.pmodelchecker.mc2.mc2_experiment import MC2Experiment as Experiment #@UnusedImport @Reimport
		elif command == check_prism:
			from infobiotics.pmodelchecker.prism.prism_experiment import PRISMExperiment as Experiment #@UnusedImport @Reimport
		elif command == optimise:
			from infobiotics.poptimizer.poptimizer_experiment import POptimizerExperiment as Experiment #@Reimport
		
		experiment = Experiment()

#		import setproctitle
#		setproctitle.setproctitle(experiment.executable_name)
		
		if command == simulate:
			if model != '':
				experiment.directory = directory
				experiment.model_file = model

		elif command in (check_mc2, check_prism):
			if model != '':
				experiment.directory = directory
				experiment.model_specification = model

		if params != '':
			experiment.load(params)

		experiment.configure() # starts event loop
#		experiment.perform() # useful for debugging without threads
	except TraitError as e:
		message = e.args[0]
		if "The 'executable' trait of a " in message:
			executable = message.split("'")[5]
			if len(executable) > 0:
				missing_executable(executable)
		exit(e)
		
		
if __name__ == '__main__':
	main(sys.argv)# + ['mcss-results'])
