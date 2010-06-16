from infobiotics.commons.traits.api import RelativeFile, RelativeDirectory
from enthought.preferences.api import PreferencesHelper
from enthought.preferences.ui.api import PreferencesPage
from enthought.traits.ui.api import View, Group 

# it is necessary to duplicate preference trait definitions in Helpers and Pages so the definitions are shared here
EXECUTABLE_TRAIT = RelativeFile
DIRECTORY_TRAIT = RelativeDirectory

# names of preferences traits must be public, i.e. not begin with '_'

class ParamsPreferencesHelper(PreferencesHelper):

    def _preferences_path(self):
        raise NotImplementedError('ParamsPreferencesHelper subclasses must provide a preferences_path, probably via a module-level constant such as PREFERENCES_PATH.')
    
    executable = EXECUTABLE_TRAIT 
    directory = DIRECTORY_TRAIT

class ParamsPreferencesPage(PreferencesPage):
    
    def _preferences_path_default(self):
        raise NotImplementedError('ParamsPreferencesPage subclasses must provide a preferences_path, probably via a module-level constant such as PREFERENCES_PATH.')

    def _category_default(self):
        return '' # default to a top-level page
    
    def _name_default(self):
        raise NotImplementedError('ParamsPreferencesPage subclasses must provide a name, which might be the same as the preferences_path.')
    
    executable = EXECUTABLE_TRAIT
    directory = DIRECTORY_TRAIT
    
    view = View(
        Group(
            'executable',
            show_border=True,
        ),        
    )

#TODO use in Params
#from enthought.preferences.ui.api import PreferencesPage, PreferencesManager
#from enthought.traits.api import HasTraits, Instance, List, Undefined
#from enthought.preferences.api import bind_preference
#from enthought.traits.ui.api import Controller, View, Group, Item, MenuBar, Menu, Action 
#
#class Params(HasTraits):
#    executable = EXECUTABLE_TRAIT # must be public, i.e. does not begin with '_'
#    
#    def __init__(self, **traits):
#        super(Params, self).__init__(**traits)
#        bind_preference(self, 'executable', 'Params.executable') # uses global preferences via get_default_preferences()
#    
#    def save_default_preferences(self):
#        helper = ParamsPreferencesHelper() # must use a PreferencesHelper and not a PreferencesPage
#        helper.executable = 'example'
#        helper.preferences.save()
##        # equivalent to:
##        from enthought.preferences.api import get_default_preferences
##        preferences = get_default_preferences()
##        preferences.set('Params.executable', 'example')
##        preferences.save()
    
