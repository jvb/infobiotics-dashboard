from traits.api import HasTraits, File, Directory 
from traitsui.api import View, Item, FileEditor, DirectoryEditor

class Workspace(HasTraits):
    
    directory = Directory('/home/jvb/Desktop/motifs')
    file = File('directory')
    
    traits_view = View(
        Item('directory',
             show_label=False, 
             style='custom', 
             editor=DirectoryEditor(),
        ),
        Item('file', 
             show_label=False, 
             style='custom', 
             editor=FileEditor(filter=['*.lpp', ]),
        ),
        width=600, height=400,                   
    )
    
if __name__ == '__main__':
    Workspace().configure_traits()

 