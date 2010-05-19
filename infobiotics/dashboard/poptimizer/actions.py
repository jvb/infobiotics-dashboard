from enthought.pyface.action.api import Action as PyFaceAction
from poptimizer_experiment import POptimizerExperiment

class POptimizerExperimentAction(PyFaceAction):
    name = 'Optimisation (POptimizer)'
    tooltip = 'Optimise the parameters and structure of a P system model.'
    def perform(self, event=None):
        obj = POptimizerExperiment(application=self.window.workbench.application)
        obj.load()
        obj.edit(kind='modal')#nonmodal')

#from infobiotics.dashboard.plugins.experiments.params_experiment_editor import ParamsExperimentEditor
#
#class NewPOptimizerExperimentAction(PyFaceAction): #TODO change to NewPOptimizerExperimentAction
#    '''
#     
#    '''
#    name = 'POptimizer'
#    tooltip = 'Optimize a model'
#    
#    def perform(self, event=None):
#        self.window.workbench.edit(
#            obj=POptimizerExperiment(), 
#            kind=ParamsExperimentEditor,
#            use_existing=False
#        )
