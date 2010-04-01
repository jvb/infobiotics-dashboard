# This file is part of the Infobiotics Dashboard. See LICENSE for copyright.
# $Id: actions.py 411 2010-01-25 18:03:26Z jvb $
# $HeadURL: https://psiren.cs.nott.ac.uk/repos/infobiotics/dashboard/trunk/infobiotics/dashboard/plugins/poptimizer/actions.py $
# $Author: jvb $
# $Revision: 411 $
# $Date: 2010-01-25 18:03:26 +0000 (Mon, 25 Jan 2010) $

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
