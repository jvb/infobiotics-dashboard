from enthought.traits.api import HasTraits
from enthought.traits.file import File
from enthought.traits.directory import Directory
from enthought.traits.ui.api import View, Item
from enthought.traits.ui.qt4.file_editor2 import FileEditor

class Test(HasTraits):
#    view = View(
#        'directory',
#        Item('file', 
#            editor=FileEditor( # overrides trait args
#                auto_set=True, 
##                directory='/home/jvb/src',
##                directory_name='directory',
#            ),
#        ),
#    )

#    directory = Directory('/home/jvb/phd/eclipse/infobiotics/dashboard/tests/mcss/models')
    directory = Directory('tests/mcss/models')
    
    file = File(
        exists=True,
        auto_set=True,
        directory='/home/jvb/phd',
        directory_name='directory',
    )
    
    def _file_changed(self):
        print self.file
    
if __name__ == '__main__':
    t = Test()
#    t.file = 'test.py'
    t.configure_traits()
    