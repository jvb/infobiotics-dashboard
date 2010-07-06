from infobiotics.commons.traits.api import RelativeFile, RelativeDirectory
from enthought.preferences.api import PreferencesHelper
from enthought.preferences.ui.api import PreferencesPage
from enthought.traits.ui.api import View, Group, Item

# it is necessary to duplicate preference trait definitions in Helpers and Pages so the definitions are shared here
EXECUTABLE_TRAIT = RelativeFile(absolute=True, auto_set=True, executable=True, exists=True) # executable implies exists 
DIRECTORY_TRAIT = RelativeDirectory(absolute=True, auto_set=True, writable=True, exists=True, desc='the location file paths can be relative to.') # writable alone does not implies exists
# names of preferences traits must be public, i.e. not begin with '_'

import infobiotics.preferences # calls set_default_preferences, do not remove

class ParamsPreferencesHelper(PreferencesHelper):
    
#    def _preferences_default(self):
#        ''' Needed to override this method in PreferencesHelper because it was
#        picking up the wrong preferences even after set_default_preferences()! '''
#        from infobiotics.preferences import preferences
#        return preferences
    
    def _preferences_path(self):
        raise NotImplementedError('ParamsPreferencesHelper subclasses must provide a preferences_path, probably via a module-level constant such as PREFERENCES_PATH.')
    
    executable = EXECUTABLE_TRAIT 
    directory = DIRECTORY_TRAIT

class ParamsPreferencesPage(PreferencesPage):
    
#    def _preferences_default(self):
#        ''' Must override this method in PreferencesHelper or else it picks up 
#        the wrong preferences even after set_default_preferences()! '''
#        from infobiotics.preferences import preferences
#        return preferences

    def _preferences_path_default(self):
        raise NotImplementedError('ParamsPreferencesPage subclasses must provide a preferences_path, probably via a module-level constant such as PREFERENCES_PATH.')

    def _category_default(self):
        return '' # default to a top-level page
    
    def _name_default(self):
        raise NotImplementedError('ParamsPreferencesPage subclasses must provide a name, which might be the same as the preferences_path.')
    
    executable = EXECUTABLE_TRAIT
#    directory = DIRECTORY_TRAIT
    
    view = View(
        Group(
            'executable',
#            'directory',
            show_border=True,
        ),        
    )


if __name__ == '__main__':

    PREFERENCES_PATH = 'mcss'
    
    class McssParamsPreferencesHelper(ParamsPreferencesHelper):
        preferences_path = PREFERENCES_PATH 
    
    class McssParamsPreferencesPage(ParamsPreferencesPage):
        preferences_path = PREFERENCES_PATH
        name = PREFERENCES_PATH

    helper = McssParamsPreferencesHelper() 
    print 'helper.executable =', helper.executable
    print 'helper.directory =', helper.directory

    page = McssParamsPreferencesPage() 
    print 'page.executable =', page.executable
    print 'page.directory =', page.directory
    page.configure_traits()
    page.preferences.save() # doesn't do anything
    print 'page.executable =', page.executable
    print 'page.directory =', page.directory #FIXME doesn't change!
