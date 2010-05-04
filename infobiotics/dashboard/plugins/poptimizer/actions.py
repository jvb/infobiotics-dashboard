from enthought.pyface.action.api import Action
from infobiotics.api import POptimizerExperiment

class POptimizerExperimentAction(Action):
    name = 'Optimisation (POptimizer)'
    tooltip = 'Optimise the structure and parameters and of a Lattice Population P system model.'
    def perform(self, event=None):
        obj = POptimizerExperiment(application=self.window.workbench.application)
#        obj.load()
        obj.edit()
