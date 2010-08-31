from enthought.envisage.ui.workbench.api import WorkbenchActionSet
from enthought.envisage.ui.action.api import Group, Action
            
class McssActionSet(WorkbenchActionSet):
    
    id = 'infobiotics.dashboard.plugins.mcss.action_set.McssActionSet'

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
        Action(path='MenuBar/Experiments', class_name='infobiotics.dashboard.plugins.mcss.actions:McssExperimentAction'),
        Action(path='ToolBar/Experiments', class_name='infobiotics.dashboard.plugins.mcss.actions:McssExperimentAction'),
    ]
