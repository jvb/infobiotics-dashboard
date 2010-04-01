# This file is part of the Infobiotics Dashboard. See LICENSE for copyright.
# $Id: actions.py 408 2010-01-25 15:19:58Z jvb $
# $HeadURL: https://psiren.cs.nott.ac.uk/repos/infobiotics/dashboard/trunk/infobiotics/dashboard/plugins/pmodelchecker/actions.py $
# $Author: jvb $
# $Revision: 408 $
# $Date: 2010-01-25 15:19:58 +0000 (Mon, 25 Jan 2010) $

import os; os.environ['ETS_TOOLKIT']='qt4'
from enthought.pyface.action.api import Action as PyFaceAction
from prism_experiment import PRISMExperiment
from mc2_experiment import MC2Experiment

class PRISMExperimentAction(PyFaceAction):
    name = 'PModelChecker (PRISM)'
    tooltip = 'Load a PRISM experiment from a parameters file.'
    def perform(self, event=None):
        obj = PRISMExperiment(application=self.window.workbench.application)
        obj.load()    
        obj.edit(kind='modal')#nonmodal')

class MC2ExperimentAction(PyFaceAction):
    name = 'PModelChecker (MC2)'
    tooltip = 'Load an MC2 experiment from a parameters file.'
    def perform(self, event=None):
        obj = MC2Experiment(application=self.window.workbench.application)
        obj.load()    
        obj.edit(kind='modal')#nonmodal')


#from pmodelchecker_experiment_editor import PModelCheckerExperimentEditor
#from infobiotics.dashboard.plugins.experiments.params_experiment_editor import ParamsExperimentEditor
#from enthought.traits.api import File, Enum, Str
#from enthought.traits.ui.api import View, Item, Group

#class NewPModelCheckerAction(PyFaceAction): #TODO change to NewPModelCheckerExperimentAction
#    name = 'PModelChecker'
#    tooltip = 'Check a model'
#    
#    message = Str('Please select a model checker to use:')
#    choice = Enum(['PRISM','MC2'])
#     
#    choice_view = View(
#        Group(
#            Item('message', style='readonly', show_label=False),
#            Item('choice', style='custom', show_label=False),
#            show_border=True,
#        ),
#        buttons = ['OK','Cancel']
#    )
#    
#    def perform(self, event=None):
#        preferences = self.window.application.preferences
#        print preferences.dump()
##        print preferences.get('infobiotics.dashboard.plugins.pmodelchecker.path_to_pmodelchecker')
##        print preferences.get('infobiotics.dashboard.plugins.pmodelchecker.path_to_mc2')
##        print preferences.get('infobiotics.dashboard.plugins.pmodelchecker.path_to_prism')
#        
#        ui = self.edit_traits(kind='modal')
#        if not ui.result:
#            return
#        
#        if self.choice == 'PRISM':
#            from prism_experiment import PRISMExperiment
#            obj = PRISMExperiment()
#        elif self.choice == 'MC2':
#            from mc2_experiment import MC2Experiment
#            obj = MC2Experiment()
#        else:
#            return
#
#        self.window.workbench.edit(
#            obj,
##            kind=PModelCheckerExperimentEditor,
#            kind=ParamsExperimentEditor,
#            use_existing=False
#        )
