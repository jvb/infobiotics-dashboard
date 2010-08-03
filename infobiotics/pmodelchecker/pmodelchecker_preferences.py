from infobiotics.core.params_preferences import ParamsPreferencesHelper, ParamsPreferencesPage

PREFERENCES_PATH = 'pmodelchecker'

class PModelCheckerParamsPreferencesHelper(ParamsPreferencesHelper):
    preferences_path = PREFERENCES_PATH 

class PModelCheckerParamsPreferencesPage(ParamsPreferencesPage):
    preferences_path = PREFERENCES_PATH
    name = PREFERENCES_PATH
