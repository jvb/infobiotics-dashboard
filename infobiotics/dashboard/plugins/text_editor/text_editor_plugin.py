from enthought.envisage.api import Plugin
from enthought.traits.api import List

ACTION_SETS = 'enthought.envisage.ui.workbench.action_sets'

class TextEditorPlugin(Plugin):

    id = "enthought.plugins.text_editor"
    
    name = 'Text Editor plugin'

    action_sets = List(contributes_to=ACTION_SETS)
    def _action_sets_default(self):
        from text_editor_action_set import TextEditorActionSet
        return [TextEditorActionSet]
