from enthought.pyface.action.api import Action
from infobiotics.dashboard.pmodelchecker.api import PRISMDashboardExperiment, MC2DashboardExperiment
from infobiotics.pmodelchecker.pmodelchecker_results import PModelCheckerResults
from enthought.pyface.api import FileDialog, OK
from editor import PModelCheckerResultsEditor 
from infobiotics.dashboard.pmodelchecker import commons

class PRISMExperimentAction(Action):
    name = 'PModelChecker: PRISM'
    tooltip = 'Check properties of a model using PRISM.'
    def perform(self, event=None):
        PRISMDashboardExperiment(application=self.window.workbench.application).edit()

class MC2ExperimentAction(Action):
    name = 'PModelChecker: MC2'
    tooltip = 'Check properties of a model using MC2.'
    def perform(self, event=None):
        MC2DashboardExperiment(application=self.window.workbench.application).edit()

class PModelCheckerResultsAction(Action):
    name = 'PModelChecker Results'
    tooltip = 'Visualise checked properties.'
    def perform(self, event=None):
        fd = FileDialog(
            wildcard=FileDialog.create_wildcard('PModelChecker results files', ['*.psm','*.mc2']),
            title='Select a PModelChecker results file',
        )
        if fd.open() != OK:
            return
        commons.edit_pmodelchecker_results_file(
            file=fd.path,
#            application=self.application,
            application=self.window.application,
#            application=self.window.workbench.application,
        )
        

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
