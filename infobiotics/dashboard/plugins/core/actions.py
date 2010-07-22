from enthought.pyface.action.api import Action


class UndoAction(Action):
#    id = 'infobiotics.dashboard.plugins.core.actions.UndoAction'
    name = '&Undo'
    tooltip = 'Undo the last change.'
    accelerator = 'Ctrl-z'

    def perform(self, event=None):
        active_editor = self.window.active_editor
        if active_editor is not None:
            if hasattr(active_editor, 'ui'):
                ui = active_editor.ui
                if ui.history is not None and ui.history.can_undo:
                    ui.handler._on_undo(ui.info)


class RedoAction(Action):
#    id = 'infobiotics.dashboard.plugins.core.actions.RedoAction'
    name = '&Redo'
    tooltip = 'Redo the previously undone action.'
    accelerator = 'Ctrl-y'

    def perform(self, event=None):
        active_editor = self.window.active_editor
        if active_editor is not None:
            if hasattr(active_editor, 'ui'):
                ui = self.window.active_editor.ui
                if ui.history is not None and ui.history.can_redo:
                    ui.handler._on_redo(ui.info)
