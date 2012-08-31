from envisage.api import Plugin
from traits.api import List

ACTION_SETS = 'envisage.ui.workbench.action_sets'

class FileEditorsPlugin(Plugin):

    id = "envisage.plugins.file_editor"
    
    name = 'File Editor plugin'

    action_sets = List(contributes_to=ACTION_SETS)
    def _action_sets_default(self):
        from action_set import FileEditorsActionSet
        return [FileEditorsActionSet]
