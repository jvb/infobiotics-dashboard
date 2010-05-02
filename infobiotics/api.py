from enthought.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'qt4'
ETSConfig.company = 'infobiotics'

from mcss.api import McssExperiment

#from pmodelchecker.api import PModelCheckerExperiment
from pmodelchecker.mc2.api import MC2Experiment
from pmodelchecker.prism.api import PRISMExperiment

#from poptimizer.api import POptimizerExperiment #FIXME see poptimizer.api
