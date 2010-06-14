'''
Adapted from TraitsBackendWX/enthought/traits/ui/wx/progress_editor.py and uses
a TraitsBackendQt ProgressDialog as its control.

Can't use can_cancel=True because ProgressDialog sets up a cancel signal via 
the QDialogButtonBox that is not present for the widget. Maybe this can be 
wrapped in a traits Event instead...  

'''

from PyQt4 import QtGui, QtCore

from enthought.traits.api import Instance
from enthought.traits.ui.qt4.editor import Editor
from enthought.pyface.ui.qt4.progress_dialog import ProgressDialog

class SimpleEditor(Editor):
    """
    Show a progress bar with all the optional goodies

    """

    progress = Instance(ProgressDialog)

    #-- Editor interface ------------------------------------------------------

    def init ( self, parent ):
        """ Finishes initializing the editor by creating the underlying toolkit
            widget.
        """
        self.control = self.create_control( parent )
        self.set_tooltip()

    def create_control (self, parent):
        """
        Finishes initializing the editor by creating the underlying widget.
        """

        self.progress = ProgressDialog(title=self.factory.title,
                                       message=self.factory.message,
                                       min=self.factory.min,
                                       max=self.factory.max,
                                       can_cancel=self.factory.can_cancel,
                                       show_time=self.factory.show_time,
                                       show_percent=self.factory.show_percent)
        import time
        self.progress._start_time = time.time()

#        panel = wx.Panel(parent, -1)
        panel = QtGui.QWidget(parent.parent())
        
#        sizer = wx.BoxSizer(wx.VERTICAL)
#        panel.SetSizer(sizer)
#        panel.SetAutoLayout(True)
#        panel.SetBackgroundColour(wx.NullColor)
        sizer = QtGui.QVBoxLayout()
        panel.setLayout(sizer)

#        self.progress.dialog_size = wx.Size()
        self.progress.dialog_size = QtCore.QRect()

        # The 'guts' of the dialog.
        self.progress._create_message(panel, sizer)
        self.progress._create_gauge(panel, sizer)
        self.progress._create_percent(panel, sizer)
        self.progress._create_timer(panel, sizer)
        self.progress._create_buttons(panel, sizer)

#        panel.SetClientSize(self.progress.dialog_size)

#        panel.CentreOnParent()

        self.control = panel
        return self.control


    def update_editor(self):
        """
        Updates the editor when the object trait changes externally to the
        editor.
        """
        if not str(self.value) == '<undefined>':
            if self.value:
                self.progress.update(self.value)
        return
    
    
    
if __name__ == '__main__':
    import os; os.environ['ETS_TOOLKIT']='qt4'
    from enthought.traits.api import HasTraits, Range, Int, Button
    from enthought.traits.ui.api import View, Item, Spring, ProgressEditor
    #from progress_Editor import ProgressEditor
    
    progress_editor = ProgressEditor(
        title='title',
        min=0,
        max=100,
        message='message',
    #    can_cancel=True,
    #    can_ok=False,
        show_time=True,
        show_percent=True,
    )
    
    class TestProgressEditor(HasTraits):
        progress_min = Int(0)
        progress_max = Int(100)
        progress_increment = Int(1)
        progress = Range('progress_min', 'progress_max', 99)#'progress_min')
        increment = Button
        
        def _increment_fired(self):
            self.progress += self.progress_increment
    
        view = View(
            Item('progress', 
                editor=progress_editor,
                show_label=False,
            ),
            Spring(),
            Item('increment', show_label=False, enabled_when='object.progress <= (object.progress_max - object.progress_increment)'),
            resizable=True,
        )

    TestProgressEditor().configure_traits()
    