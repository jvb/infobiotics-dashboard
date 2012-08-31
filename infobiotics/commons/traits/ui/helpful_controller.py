from enthought.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'qt4' 
from enthought.traits.api import Property, Str, Bool, List, Tuple, HasTraits
from enthought.traits.ui.api import Controller, View, Item
from enthought.traits.ui.menu import Action, Menu, MenuBar
from infobiotics.commons import webbrowsing
        
class HelpStr(HasTraits):
    help_str = Str

help_action = Action(
    name='&Help', # the '&' might cause problems with KeyBindings...
    action='help',
    visible_when='handler.has_help',
)

class HelpfulController(Controller):

    def get_help_action(self):
        return help_action

    def help(self, info): # called by help_action (above)
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
                        id='%s.help' % self.__class__.__name__
                    )
                )
        elif len(self.help_urls) > 0:
            name, help_url = self.help_urls[0]
            if len(help_url) > 0:
                webbrowsing.dedicated_window(help_url)
    
    has_help = Property(Bool, depends_on='help_urls, help_strs')

    def _get_has_help(self):
        return True if len(self.help_urls) + len(self.help_strs) > 0 else False
    
    # using multiple named help urls or strings we can offer a menu of different help topics 
    help_urls = List(Tuple(Str, Str))
    help_strs = List(Tuple(Str, Str))
    
    def create_help_url_action_method(self, url):
        ''' Ensures method creation not done in loop otherwise help_url 
        changes and all actions open the same URL. '''
        def action_method(self, info):
            webbrowsing.dedicated_window(url)
        return action_method
        
    def create_help_str_action_method(self, str, name):
        def action_method(self, info):
            HelpStr(help_str=str).edit_traits(
                view=View(
                    Item('help_str', show_label=False, style='custom'),
                    buttons=['OK'],
                    width=640, height=480,
                    scrollable=True,
                    resizable=True,
                    title=name,
                    id='%s.help' % self.__class__.__name__,
#                    parent = self.info.ui.control,
                )
            )
        return action_method 
    
    def get_help_actions(self):
        ''' Create a list of actions and add methods for them to this class. '''
        actions = []
        for i, help_str in enumerate(self.help_strs):
            name, str = help_str # unpack tuple
            action_method = self.create_help_str_action_method(str, name) # create action method
            action_method_name = 'help_str_%s' % i
            setattr(self.__class__, action_method_name, action_method) # add to object
            actions.append(Action(name=name, action=action_method_name)) # add to action list
        for i, help_url in enumerate(self.help_urls):
            name, url = help_url
            action_method = self.create_help_url_action_method(url)
            action_method_name = 'help_url_%s' % i
            setattr(self.__class__, action_method_name, action_method)
            actions.append(Action(name=name, action=action_method_name))
        return actions # return actions list
    
    def get_help_menu(self):
        actions = self.get_help_actions()
        if len(actions) > 0:
            kwargs = {'name':'&Help'}
            return Menu(*actions, **kwargs)
            # for python2.5 compatibility, instead of:
            #return Menu(*actions, name='&Help') 
    

if __name__ == '__main__':
    
    class Model(HasTraits):
        s = Str
    
    class Handler(HelpfulController):
        help_urls = [
            ('Tutorial', 'http://www.infobiotics.org/infobiotics-workbench/tutorial/modelCheckingMC2.html'),
            ('MC2 webpage', 'http://www.brc.dcs.gla.ac.uk/software/mc2/'),
        ]
        
        help_strs = [('Test', 'testing'), ('Test2', 'testing again')]
        
        def traits_view(self):
            return View(
                's',
                menubar=MenuBar(
                    self.get_help_menu(),
                ),
            )
            
    m = Model(s='test')
    h = Handler(model=m)
#    view = View(
#        's',
#        menubar = MenuBar(
#            h.get_help_menu(),
#        ),
#    )
    h.configure_traits()#view=view)
    
