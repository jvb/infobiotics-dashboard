''' Displaying a list of objects as their views. '''

from enthought.traits.api import HasTraits, Int, Button, Str, List
from enthought.traits.ui.api import View, HGroup, Item, ListEditor, InstanceEditor

class MySubClass(HasTraits):
    ''' The class of objects in the list. '''
    
    my_int = Int
    my_button = Button
    my_str = Str
    
    view = View(
        HGroup(
            Item('my_int', show_label=True),
            Item('my_button', show_label=False),
            Item('my_str', show_label=True),
        )
    )

class MySubClass2(HasTraits):
    ''' The class of objects in the list. '''
    
    my_button = Button
    my_str = Str
    
    view = View(
        HGroup(
            Item('my_button', show_label=False),
            Item('my_str', show_label=True),
        )
    )

class MainClass(HasTraits):
    ''' The class of an object with the list. '''
    my_list = List(MySubClass)
#    my_list = List(HasTraits)
    
    push = Button
    pop = Button 
    
    traits_view = View(
        'push',
        'pop',
        Item('my_list',
            show_label=False,
            style='readonly',
            editor=ListEditor(
                editor=InstanceEditor(),
                style='custom',
            )
        ),
        resizable=True,
        width=400, height=400,
        id='list_of_instances',
    )

    def _my_list_default(self):
        return [
            MySubClass(),
#            MySubClass2(),
            MySubClass(),
        ]

    def _push_fired(self):
        self.my_list.append(MySubClass())
        
    def _pop_fired(self):
        self.my_list.pop()


if __name__ == '__main__':
    MainClass().configure_traits()
