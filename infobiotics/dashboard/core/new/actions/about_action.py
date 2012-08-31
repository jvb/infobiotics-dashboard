from pyface.action.api import Action
from traits.api import Property, Bool

class AboutAction(Action):
    name = '&About'
    description = 'Display information about the application'
    tooltip = "Show the 'About' dialog"

    enabled = Property(Bool)
    def _get_enabled(self):
        if self.window is not None and self.window.application.about_dialog is not None:
            return True
        return False

    def perform(self, event):
        perform(self.window)

def perform(window):
    window.application.about()
    