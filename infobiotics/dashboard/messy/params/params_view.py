from infobiotics.dashboard.params.api import load_save_actions 
from enthought.traits.ui.api import View, Group

params_view = View(
    Group(),
    buttons=['Undo','Revert','OK', 'Cancel'] + load_save_actions,
#    width=640, height=480,
    resizable=True,
    id='params_view',
)
