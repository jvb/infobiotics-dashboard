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


from enthought.etsconfig.api import ETSConfig 
ETSConfig.toolkit = 'qt4' # set toolkit to 'qt4' (TraitsBackendQt) before any Traits imports; os.environ['ETS_TOOLKIT']='qt4' also works
ETSConfig.company = 'infobiotics' # use ~/.infobiotics (or "Application Data\infobiotics" on Windows) instead of ~/.enthought for storing preferences


from infobiotics.commons.traits.relative_file import RelativeFile

_params_program_trait = RelativeFile # shared trait definition for preference this is used by PreferencesHelper and PreferencesPage


from enthought.preferences.api import PreferencesHelper

class TestPreferencesHelper(PreferencesHelper):
    preferences_path = 'Test' 

    params_program = _params_program_trait # must be public, i.e. does not begin with '_'


from enthought.traits.api import HasTraits
from enthought.preferences.api import bind_preference

class Test(HasTraits):
    params_program = _params_program_trait # must be public, i.e. does not begin with '_'
    
    def __init__(self, **traits):
        super(Test, self).__init__(**traits)
        bind_preference(self, 'params_program', 'Test.params_program')#, preferences) # uses global preferences via get_default_preferences()
    
    def save_default_preferences(self):
        helper = TestPreferencesHelper() # must use a PreferencesHelper and not a PreferencesPage
        helper.params_program = 'billy'
        helper.preferences.save()
#        # equivalent to:
#        from enthought.preferences.api import get_default_preferences
#        preferences = get_default_preferences()
#        preferences.set('Test.params_program', 'Jon2')
#        preferences.save()


from enthought.preferences.ui.api import PreferencesPage
from enthought.traits.ui.api import View, Group

class TestPreferencesPage(PreferencesPage):
    preferences_path = 'Test'
    category = ''
    name = 'Test'
    
    params_program = _params_program_trait # must be public, i.e. does not begin with '_'
    
    view = View(
        Group(
            'params_program',
            show_border=True,
        ),        
    )


from enthought.traits.ui.api import Controller, View, Group, Item, MenuBar, Menu, Action 
from enthought.traits.api import Instance, List
from enthought.preferences.ui.api import PreferencesManager 
    
class TestHandler(Controller):
        
    a_preferences_page = Instance(TestPreferencesPage, ())
#    def _a_preferences_page_default(self):
#        return TestPreferencesPage()
    
    preferences_pages = List(PreferencesPage)
    def _preferences_pages_default(self):
        return [self.a_preferences_page]
    
    def edit_preferences(self, info):
        preferences_manager = PreferencesManager(pages=self.preferences_pages) # must pass in pages manually 
        ui = preferences_manager.edit_traits(kind='modal') # should edit preferencs modally
        if ui.result: # only save preferences if OK pressed
            for page in self.preferences_pages: # save preferences for each page as they could have different preferences nodes (files)
                page.preferences.save() # must save preferences manually
#                print 'Saved', page.preferences.filename
        
    view = View(
        Group(
            Item('params_program', style='readonly'),
            show_border=True,
        ),
        menubar = MenuBar(
            Menu(
                Action(
                    name='&Preferences...', 
                    action='edit_preferences', 
                    tooltip='TODO',
                    enabled_when='len(controller.preferences_pages) > 0', # 
                ),
                name='&Tools'
            ),
        ),
        width=640, height=480,
        resizable=True,
    )

    
if __name__ == '__main__':
    TestHandler(model=Test()).configure_traits()
    