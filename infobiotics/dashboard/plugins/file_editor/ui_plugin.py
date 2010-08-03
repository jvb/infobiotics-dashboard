from enthought.envisage.api import Plugin
from enthought.traits.api import List

ACTION_SETS = 'enthought.envisage.ui.workbench.action_sets'

class FileEditorPlugin(Plugin):

    id = "enthought.plugins.file_editor"
    
    name = 'File Editor plugin'

    action_sets = List(contributes_to=ACTION_SETS)
    def _action_sets_default(self):
        from action_set import FileEditorActionSet
        return [FileEditorActionSet]
