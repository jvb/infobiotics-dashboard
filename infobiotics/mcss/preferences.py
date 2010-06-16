from infobiotics.common.api import ParamsPreferencesHelper, ParamsPreferencesPage

PREFERENCES_PATH = 'mcss'

class McssParamsPreferencesHelper(ParamsPreferencesHelper):
    preferences_path = PREFERENCES_PATH 

class McssParamsPreferencesPage(ParamsPreferencesPage):
    preferences_path = PREFERENCES_PATH
    name = PREFERENCES_PATH
