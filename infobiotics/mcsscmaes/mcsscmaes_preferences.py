from infobiotics.core.params_preferences import ParamsPreferencesHelper, ParamsPreferencesPage

PREFERENCES_PATH = 'mcsscmaes' #TODO

class McssCmaesParamsPreferencesHelper(ParamsPreferencesHelper):
    preferences_path = PREFERENCES_PATH 

class McssCmaesParamsPreferencesPage(ParamsPreferencesPage):
    preferences_path = PREFERENCES_PATH
    name = PREFERENCES_PATH

    # uses ParamsPreferencesPage view
    
