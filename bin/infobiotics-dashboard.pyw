#!/usr/bin/env python
# THIS FILE IS AUTOMATICALLY CREATED
'''Single entry-point for Infobiotics Workbench.

With zero arguments it launches the Infobiotics Workbench/Dashboard (Envisage Workbench), 
with one argument it launches the individual experiment/command GUI (e.g. 'McssExperiment().configure()') and
with two arguments it launches the experiment and either sets the model_file/model_specification trait or loads the parameters from the second argument.

Having a single entry-point means it can be frozen (py2exe, py2app, etc.) and
called from Eclipse...
'''

# "Application asked to unregister timer 0x1c000011 which is not registered in this thread. Fix application."
# This is a bug in Qt 4.7 under Ubuntu that will be fixed in Qt 4.8 

from __future__ import with_statement

import sys
import os.path

import setproctitle

# fix matplotlib backend problems on Windows
if sys.platform.startswith('win'):
    # http://www.py2exe.org/index.cgi/MatPlotLib
    import matplotlib
    matplotlib.use('qt4agg') # overrule configuration
    import pylab #TODO remove?

import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import infobiotics.__version__

# set default log level for all loggers that use infobiotics.commons.api.logging (infobiotics.commons.unified_logging)  
from infobiotics.commons.api import logging
logging.level = logging.ERROR
#logging.level = logging.DEBUG #TODO comment out in release

simulate = 'mcss'#'simulate'
simulation_results = 'mcss-results'
check_mc2 = 'pmodelchecker-mc2'#'check-mc2'
check_prism = 'pmodelchecker-prism'#'check-prism'
checking_results = 'pmodelchecker-results'
optimise = 'poptimizer'#optimise
optimisation_results = 'poptimizer-results' 
commands = (simulate, simulation_results, check_mc2, check_prism, checking_results, optimise, optimisation_results)

def help():
    return '''Infobiotics Workbench {version}

{self} [command [file]]

commands:
 {commands_}
 
file types:
 .params ({simulate}, {check_prism}, {check_mc2}, {optimise}, {optimisation_results})  
 .sbml, .lpp, .xml ({simulate}, {check_prism}, {check_mc2})
 .h5 ({simulation_results})
 .mc2, .psm ({checking_results})
'''.format(
    version=infobiotics.__version__, 
    self=os.path.basename(__file__), 
    commands_='\n '.join(commands),
    **globals()
)


def main(argv):
    args = argv[1:]
    
    if len(args) == 0:
        setproctitle.setproctitle('Infobiotics Dashboard')        
        from infobiotics.dashboard import run
        exitcode = run.main()
        sys.exit(exitcode)
    
    command = args[0].lower()

    if len(args) > 2 or command.lower() not in commands:
        sys.exit(help())

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
            sys.exit(help())
    
    if command == optimisation_results:
        if params:
            from infobiotics.poptimizer.poptimizer_experiment import POptimizerExperiment
            from infobiotics.poptimizer.poptimizer_results import POptimizerResults
            return POptimizerResults(experiment=POptimizerExperiment(params)).configure()
        else:
            sys.exit(help())
            
    if command == simulate:
        from infobiotics.mcss.mcss_experiment import McssExperiment as Experiment
    elif command == check_mc2:
        from infobiotics.pmodelchecker.mc2.mc2_experiment import MC2Experiment as Experiment
    elif command == check_prism:
        from infobiotics.pmodelchecker.prism.prism_experiment import PRISMExperiment as Experiment
    elif command == optimise:
        from infobiotics.poptimizer.poptimizer_experiment import POptimizerExperiment as Experiment
    
    experiment = Experiment()

    setproctitle.setproctitle(experiment.executable_name)
    
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
#    experiment.perform() # useful for debugging without threads


dir = os.path.dirname(__file__)

def test_relative_path_to_model():
    main(sys.argv + ['mcss', '../examples/mcss/models/module1.sbml'])

def test_absolute_path_to_model():
    main(sys.argv + ['mcss', dir + '../examples/mcss/models/module1.sbml'])

def test_relative_path_to_params():
    main(sys.argv + ['pmodelchecker-mc2', '../examples/pmodelchecker/pulsePropagation/pulse_MC2.params'])

def test_absolute_path_to_params():
    main(sys.argv + ['poptimizer', dir + '../examples/poptimizer/fourinitial/four_initial_inputpara.params'])

def test_wrong_params_for_experiment():
    main(sys.argv + ['poptimizer', '../examples/mcss/models/reactions1.params'])

def test_absolute_path_to_model2():
    main(sys.argv + ['pmodelchecker-prism', dir + '../examples/pmodelchecker/pulsePropagation/pulsePropagation.lpp'])
    
def test_absolute_path_to_params2():
    main(sys.argv + ['pmodelchecker-prism', dir + '../examples/pmodelchecker/NAR/modelCheckingPRISM/NAR_PRISM.params'])
    

if __name__ == '__main__':
    main(sys.argv)
#    test_relative_path_to_model()
#    test_absolute_path_to_model()
#    test_relative_path_to_params()
#    test_absolute_path_to_params()
#    test_wrong_params_for_experiment()
#    test_absolute_path_to_model2()
#    test_absolute_path_to_params2()
