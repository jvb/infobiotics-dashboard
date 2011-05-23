#!/usr/bin/env python
'''
Single entry-point for Infobiotics Workbench.

With zero arguments it launches the Infobiotics Workbench/Dashboard (Envisage Workbench), 
with one argument it launches the individual experiment/command GUI (e.g. 'McssExperiment().configure()') and
with two arguments it launches the experiment and either sets the model_file/model_specification trait or loads the parameters from the second argument.

Having a single entry-point means it can be frozen (py2exe, py2app, etc.) and
called from Eclipse...
'''

# "Application asked to unregister timer 0x1c000011 which is not registered in this thread. Fix application."
# This is a bug in Qt 4.7 under Ubuntu that will be fixed in Qt 4.8 

import sys
import os.path

import setproctitle

# fix matplotlib backend problems on Windows
if sys.platform.startswith('win'):
    # http://www.py2exe.org/index.cgi/MatPlotLib
    import matplotlib
    matplotlib.use('qt4agg') # overrule configuration
    import pylab #TODO remove?
    
import infobiotics.__version__

# set default log level for all loggers that use infobiotics.commons.api.logging (infobiotics.commons.unified_logging)  
from infobiotics.commons.api import logging
logging.level = logging.ERROR
#logging.level = logging.DEBUG #TODO comment out in release

simulate = 'mcss'#'simulate'
check_mc2 = 'pmodelchecker-mc2'#'check-mc2'
check_prism = 'pmodelchecker-prism'#'check-prism'
optimise = 'poptimizer'#optimise
commands = (simulate, check_mc2, check_prism, optimise)

def help():
    return '''Infobiotics Workbench %s

Usage: infobiotics <experiment> (<model/params>)

Available experiments are:
 
 %s
''' % (infobiotics.__version__, '\n '.join(commands))


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
    if model != '':
        directory, model = os.path.split(model)
#    else:
#        directory = os.getcwd()

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


def test_relative_path_to_model():
    main(sys.argv + ['mcss', '../examples/infobiotics-examples-20110208/mcss/models/module1.sbml'])

def test_absolute_path_to_model():
    main(sys.argv + ['mcss', '/home/jvb/workspaces/workspace/infobiotics-dashboard/examples/infobiotics-examples-20110208/mcss/models/module1.sbml'])

def test_relative_path_to_params():
    main(sys.argv + ['pmodelchecker-mc2', '../examples/infobiotics-examples-20110208/pmodelchecker/pulsePropagation/pulse_MC2.params'])

def test_absolute_path_to_params():
    main(sys.argv + ['poptimizer', '/home/jvb/workspaces/workspace/infobiotics-dashboard/examples/infobiotics-examples-20110208/poptimizer/fourinitial/four_initial_inputpara.params'])

def test_wrong_params_for_experiment():
    main(sys.argv + ['poptimizer', '../examples/infobiotics-examples-20110208/mcss/models/reactions1.params'])

def test_absolute_path_to_model2():
    main(sys.argv + ['pmodelchecker-prism', '/home/jvb/workspaces/workspace/infobiotics-dashboard/examples/infobiotics-examples-20110208/pmodelchecker/pulsePropagation/pulsePropagation.lpp'])
    
def test_absolute_path_to_params2():
    main(sys.argv + ['pmodelchecker-prism', '/home/jvb/workspaces/workspace/infobiotics-dashboard/examples/infobiotics-examples-20110208/pmodelchecker/NAR/modelCheckingPRISM/NAR_PRISM.params'])
    

if __name__ == '__main__':
#    main(sys.argv) #TODO uncomment
    main(sys.argv + ['mcss'])
    #TODO comment
#    test_relative_path_to_model()
#    test_absolute_path_to_model()
#    test_relative_path_to_params()
#    test_absolute_path_to_params()
#    test_wrong_params_for_experiment()
#    test_absolute_path_to_model2()
#    test_absolute_path_to_params2()
