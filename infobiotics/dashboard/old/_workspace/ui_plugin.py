from envisage.api import Plugin
from traits.api import List

class ExampleUIPlugin(Plugin):

    # 'IPlugin' interface
    id = 'infobiotics.dashboard.example.ui_plugin.ExampleUIPlugin' # The plugin's unique identifier
    name = 'Example' # The plugin's name (suitable for displaying to the user)

    # Contributions to extension points made by this plugin

    action_sets = List(contributes_to='envisage.ui.workbench.action_sets')
    def _action_sets_default(self):
        return []
#        from action_set import ExampleActionSet
#        return [ExampleActionSet]

    perspectives = List(contributes_to='envisage.ui.workbench.perspectives')
    def _perspectives_default(self):
        from perspectives import ExamplePerspective
        return [ExamplePerspective]

    views = List(contributes_to='envisage.ui.workbench.views')
    def _views_default(self):
        from views import ExampleTraitsUIView, ExamplePyFaceView
        return [ExampleTraitsUIView, ExamplePyFaceView] 

    preferences_pages = List(contributes_to='envisage.ui.workbench.preferences_pages')
    def _preferences_pages_default(self):
        return []
#        from preferences_page import ExamplePreferencesPage
#        return [ExamplePreferencesPage]
