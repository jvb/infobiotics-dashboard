from infobiotics.commons.traits.api import RelativeFile, RelativeDirectory
from enthought.preferences.api import PreferencesHelper
#from infobiotics.core.preferences_helper import PreferencesHelper
from enthought.preferences.ui.api import PreferencesPage
from enthought.traits.api import Str, Unicode, TraitError
from enthought.traits.ui.api import View, Group, Item
#import infobiotics.preferences # calls set_default_preferences, do not remove #TODO done in Params

#import logging
#logger = logging.getLogger(__name__)
#logger.setLevel(logging.WARN)
#logger.addHandler(logging.StreamHandler())

Executable = RelativeFile(auto_set=True, absolute=True, executable=True) # executable=True implies exists=True
Directory = RelativeDirectory(absolute=True, auto_set=True, writable=True, readable=True, desc='the location file paths can be relative to.') # readable=True implies exists=True

# names of preferences traits must be public, i.e. not begin with '_'

class ParamsPreferencesHelper(PreferencesHelper):
    
    executable = Executable
    directory = Directory

    def _preferences_default(self):
        '''Overridden because it was picking up the wrong preferences even 
        after set_default_preferences().'''
        from infobiotics.preferences import preferences
        return preferences
    
    def _preferences_path(self):
        raise NotImplementedError('ParamsPreferencesHelper subclasses must provide a preferences_path, probably via a module-level constant such as PREFERENCES_PATH.')
    
    # copied from PreferencesHelper and added TraitError exception handling
    def _get_value(self, trait_name, value):
        """ Get the actual value to set.

        This method makes sure that any required work is done to convert the
        preference value from a string. Str traits or those with the metadata
        'is_str=True' will just be passed the string itself.

        """

        trait = self.trait(trait_name)
        handler = trait.handler

        # If the trait type is 'Str' then we just take the raw value.
        if isinstance(handler, Str) or trait.is_str:
            pass
            
        # If the trait type is 'Unicode' then we convert the raw value.
        elif isinstance(handler, Unicode):
            value = unicode(value)

        # Otherwise, we eval it!
        else:
            try:
                value = eval(value)

            # If the eval fails then there is probably a syntax error, but
            # we will let the handler validation throw the exception.
            except:
                pass

        if handler.validate is not None:
            # Any traits have a validator of None.
            try:
                validated = handler.validate(self, trait_name, value)
            except TraitError, e:
#                logger.exception(e)
                validated = handler.get_default_value()[1] 
#                validated = handler.validate(self, trait_name, handler.get_default_value()[1])
#                if hasattr(handler, 'post_setattr'):
#                    ...
        else:
            validated = value

        return validated

class ParamsPreferencesPage(PreferencesPage):
    
    executable = Executable
#    directory = Directory
    
    def _preferences_default(self):
        '''Overridden because it was picking up the wrong preferences even 
        after set_default_preferences().'''
        from infobiotics.preferences import preferences
        return preferences

    def _preferences_path_default(self):
        raise NotImplementedError('ParamsPreferencesPage subclasses must provide a preferences_path, probably via a module-level constant such as PREFERENCES_PATH.')

#    def _category_default(self):
#        return '' # default to a top-level page
    
    def _name_default(self):
        raise NotImplementedError('ParamsPreferencesPage subclasses must provide a name, which might be the same as the preferences_path.')
    
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
