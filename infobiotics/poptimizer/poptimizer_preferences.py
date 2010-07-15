from infobiotics.common.api import ParamsPreferencesHelper, ParamsPreferencesPage

PREFERENCES_PATH = 'poptimizer' #TODO

class POptimizerParamsPreferencesHelper(ParamsPreferencesHelper):
    preferences_path = PREFERENCES_PATH 

class POptimizerParamsPreferencesPage(ParamsPreferencesPage):
    preferences_path = PREFERENCES_PATH
    name = PREFERENCES_PATH
