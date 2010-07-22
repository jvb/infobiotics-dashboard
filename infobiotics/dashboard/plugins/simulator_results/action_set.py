from enthought.envisage.ui.workbench.api import WorkbenchActionSet
from enthought.envisage.ui.action.api import Group, Action
            
class SimulatorResultsActionSet(WorkbenchActionSet):

    id = 'infobiotics.dashboard.plugins.simulator_results.action_set'

    groups = [
        Group(
            id='ResultsGroup',
            path='MenuBar/File',
            after='TextFileGroup', #TODO enthought.plugins.text_editor.text_editor_action_set
        ),
    ]

    actions = [
        Action(
            name='Open &mcss results...', 
            class_name='infobiotics.dashboard.plugins.simulator_results.actions:SimulatorResultsAction', 
            group='ResultsGroup',
            path='MenuBar/File', 
        ),
    ]
