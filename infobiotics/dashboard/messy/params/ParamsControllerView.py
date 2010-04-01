from enthought.traits.ui.api import View
from enthought.traits.api import This
from infobiotics.dashboard.params.api import load_save_actions

class ParamsControllerView(View):
    buttons = ['Undo','Revert','OK', 'Cancel'] + load_save_actions
    resizable = True
    scrollable = False
    id = This.__name__