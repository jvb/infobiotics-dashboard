import sys
import os.path
import infobiotics.__version__

def help():
    return '''Infobiotics Workbench %s

Usage: ibw <experiment>

Available experiments are:
 mcss
 pmodelchecker
 poptimizer
 
''' % (infobiotics.__version__)

simulate = 'mcss'#'simulate'
check = 'pmodelchecker'#'check'
optimise = 'poptimizer'#optimise

def fail():
    sys.exit(help())
    

def main():
    path, filename = os.path.split(sys.argv[0])
    args = sys.argv[1:]
#    print path, filename, args
    if len(args) == 0:
        fail()
    if len(args) > 2:
        fail()
    experiment = args[0].lower()
    if experiment not in (simulate, check, optimise):
        fail()
    if len(args) == 2:
        model = args[1]
        if not os.path.exists(model):
            sys.exit("The model file '%s' does not exist" % model)
    if experiment == simulate:
        from infobiotics.mcss.mcss_experiment import McssExperiment
        if len(model)
        McssExperiment.configure()
    elif experiment == check:
        print check
    elif experiment == optimise:
        print optimise
    else:
        fail()


if __name__ == '__main__':
    sys.argv += ['mcss', 'model']
    main()
