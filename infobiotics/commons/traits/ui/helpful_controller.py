from enthought.traits.api import Property, Str, Bool, List, Tuple, HasTraits
from enthought.traits.ui.api import Controller, View, Item
from enthought.traits.ui.menu import Action, Menu
from infobiotics.commons import webbrowsing

help_action = Action(
    name='&Help', # the '&' might cause problems with KeyBindings...
    action='help',
    visible_when='handler.has_help',
)

class HelpStr(HasTraits):
    help_str = Str

class HelpfulController(Controller):

    has_help = Property(Bool, depends_on='help_urls, help_strs')

    def _get_has_help(self):
        return True if len(self.help_urls) + len(self.help_strs) > 0 else False
    
    # using multiple named help urls or strings we can offer a menu of different help topics 
    help_urls = List(Tuple(Str, Str))
    help_strs = List(Tuple(Str, Str))
    
    def help(self, info): # called by help_action
        ''' Opens a help window on the first item of help_strs or help_urls. '''
        if len(self.help_strs) > 0:
            name, help_str = self.help_strs[0]
            if len(help_str) > 0: #TODO unnecessary?
                HelpStr(help_str=str).edit_traits(
                    view=View(
                        Item('help_str', show_label=False, style='custom'), # TraitsUI (at least TraitsBackendQt) checks Str traits for HTML syntax and uses the appropriate editor automatically
                        buttons=['OK'],
                        width=640, height=480,
                        scrollable=True,
                        resizable=True,
                        title=name,
                        id = '%s.help' % self.__class__.__name__
                    )
                )
        elif len(self.help_urls) > 0:
            name, help_url = self.help_urls[0]
            if len(help_url) > 0:
                webbrowsing.dedicated_window(help_url)
    
    def get_help_actions(self):
        ''' Create a list of actions and add methods for them to this class. '''
        actions = []
        for i, help_url in enumerate(self.help_urls):
            name, help_url = help_url
            def action_method(self, info):
                webbrowsing.dedicated_window(help_url)
            action = 'help_url_%s' % i
            setattr(self.__class__, action, action_method)
            actions.append(Action(name=name, action=action))
        for i, help_str in enumerate(self.help_strs):
            name, help_str = help_str
            def action_method(self, info):
                HelpStr(help_str=help_str).edit_traits(
                    view=View(
                        Item('help_str', show_label=False, style='custom'),
                        buttons=['OK'],
                        width=640, height=480,
                        scrollable=True,
                        resizable=True,
                        title=name,
                        id = '%s.help' % self.__class__.__name__,
#                        parent = self.info.ui.control,
                    )
                )
            action = 'help_str_%s' % i
            setattr(self.__class__, action, action_method)
            actions.append(Action(name=name, action=action))
        return actions
    
    def get_help_menu(self):
        actions = self.get_help_actions()
        if len(actions) > 0:
            # for python2.5 compatibility:
            kwargs = {'name':'&Help'}
            return Menu(*actions, **kwargs)
#            return Menu(*actions, name='&Help')
        else:
            return
    
    def get_help_action(self):
        return help_action


def test_get_help_actions():
    class Test(HelpfulController):
        help_urls = [('Google','http://www.google.com/')]
        help_strs = [('Test','testing'),('Test2','testing again')]
    t = Test()
    for action in t.get_help_actions():
        print action.name, action.action
    t.help_str_1(info='')
    print t.get_help_menu()
    
if __name__ == '__main__':
    test_get_help_actions()
    
    class Test(HasTraits):
        
    
    
    h.configure_traits(model=t)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    