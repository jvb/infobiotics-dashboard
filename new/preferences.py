''' A dialog that the uses PreferencesPages to manage preferences.

There is a menu action 'Preferences...' that opens a PreferencesManager 
displaying the PreferencesPages.

Preferences are bound to traits on objects using:
    bind_preference(obj, trait_name, full_preferences_path_inc_preference_name)  

Each PreferencesPage should share (public) trait definitions with a sister
PreferencesHelper that handle the conversion and validation of preferences from
strings in a .ini file to trait values, and enables programmatic getting and  
setting (and loading and saving) of preferences.

'''

PREFERENCES_PATH = 'Test'


from enthought.etsconfig.api import ETSConfig 
ETSConfig.toolkit = 'qt4' # set toolkit to 'qt4' (TraitsBackendQt) before any Traits imports; os.environ['ETS_TOOLKIT']='qt4' also works
ETSConfig.company = 'infobiotics' # use ~/.infobiotics (or "Application Data\infobiotics" on Windows) instead of ~/.enthought for storing preferences

from enthought.traits.api import Str
PREFERENCES_TRAIT = Str # shared trait definition for preference this is used by PreferencesHelper and PreferencesPage


from enthought.preferences.api import PreferencesHelper

class TestPreferencesHelper(PreferencesHelper):
    preferences_path = PREFERENCES_PATH 

    a_preference = PREFERENCES_TRAIT # must be public, i.e. does not begin with '_'


from enthought.traits.api import HasTraits
from enthought.preferences.api import bind_preference

class Test(HasTraits):
    a_preference = PREFERENCES_TRAIT # must be public, i.e. does not begin with '_'
    
    def __init__(self, **traits):
        super(Test, self).__init__(**traits)
#        bind_preference(self, 'a_preference', 'Test.a_preference')#, preferences) # uses global preferences via get_default_preferences()
    
    def save_default_preferences(self):
        helper = TestPreferencesHelper() # must use a PreferencesHelper and not a PreferencesPage
        helper.a_preference = 'billy'
        helper.preferences.save()
#        # equivalent to:
#        from enthought.preferences.api import get_default_preferences
#        preferences = get_default_preferences()
#        preferences.set('Test.a_preference', 'Jon2')
#        preferences.save()


from enthought.preferences.ui.api import PreferencesPage
from enthought.traits.ui.api import View, Group

class TestPreferencesPage(PreferencesPage):
    preferences_path = PREFERENCES_PATH
    category = '' # this is a top-level page
    name = PREFERENCES_PATH
    
    a_preference = PREFERENCES_TRAIT # must be public, i.e. does not begin with '_'
    
    view = View(
        Group(
            'a_preference',
            show_border=True,
        ),        
    )


from enthought.traits.ui.api import Controller, View, Group, Item, MenuBar, Menu, Action 
from enthought.traits.api import Instance, List, Property
from enthought.preferences.ui.api import PreferencesManager 
    
class TestHandler(Controller):
        
    a_preferences_page = Instance(TestPreferencesPage, None)
#    def _a_preferences_page_default(self):
#        return TestPreferencesPage()
    
    preferences_pages = List(PreferencesPage)
    def _preferences_pages_default(self):
        return [self.a_preferences_page]

    _preferences_pages = Property(depends_on='preferences_pages')
    def _get__preferences_pages(self):
        return [page for page in self.preferences_pages if page is not None]
    
    def edit_preferences(self, info):
        preferences_manager = PreferencesManager(pages=self._preferences_pages) # must pass in pages manually 
        ui = preferences_manager.edit_traits(kind='modal') # should edit preferencs modally
        if ui.result: # only save preferences if OK pressed
            for page in self.preferences_pages: # save preferences for each page as they could have different preferences nodes (files)
                page.preferences.save() # must save preferences manually
#                print 'Saved', page.preferences.filename
        
    view = View(
        Group(
            Item('a_preference', style='readonly'),
            show_border=True,
        ),
        menubar = MenuBar(
            Menu(
                Action(
                    name='&Preferences...', 
                    action='edit_preferences', 
                    tooltip='TODO',
                    enabled_when='len(controller._preferences_pages) > 0', # 
                ),
                name='&Tools'
            ),
        ),
        width=640, height=480,
        resizable=True,
    )

    
if __name__ == '__main__':
    TestHandler(model=Test()).configure_traits()
    