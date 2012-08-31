from enthought.envisage.ui.workbench.api import WorkbenchActionSet
from enthought.envisage.ui.action.api import Group, Action
            
class McssResultsActionSet(WorkbenchActionSet):

    id = 'infobiotics.dashboard.mcss.results.action_set'

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
            class_name='infobiotics.dashboard.mcss.results.actions:McssResultsAction',
            group='ResultsGroup',
            path='MenuBar/File',
        ),
    ]
