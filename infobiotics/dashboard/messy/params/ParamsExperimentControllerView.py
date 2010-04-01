from infobiotics.dashboard.params.ParamsControllerView import ParamsControllerView
from infobiotics.dashboard.params.api import load_save_perform_actions

class ParamsExperimentControllerView(ParamsControllerView):
    buttons = ['Undo','Revert','OK', 'Cancel'] + load_save_perform_actions
