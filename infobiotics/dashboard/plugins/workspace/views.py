from enthought.pyface.workbench.api import View as PyFaceView

class ExamplePyFaceView(PyFaceView):
    ''' An example native-widget view for a workbench application plugin
    perspective.
    
    View are used to present information to the user to help them perform their
    current task. For example they can show the structure of a document as a 
    tree where clicking on a tree node moves the cursor to the relevant 
    section. 
    
    A PyFaceView must override create_control to return a native widget.
     
    '''
    category = 'Example'
    id = 'infobiotics.dashboard.plugins.example.views.ExamplePyFaceView'
    name = 'ExamplePyFaceView'
    position = 'right' # the position to occupy; often overriden in PerspectiveItem(... 
    width = 0.3 # the proportion of the window to occupy, from 0.0 to 1.0

    def create_control(self, parent):
        ''' An example 'create_control' implementation.
        
        '''
        from PyQt4 import QtGui
        widget = QtGui.QWidget(parent)
        palette = widget.palette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor('white'))
        widget.setPalette(palette)
        widget.setAutoFillBackground(True)
        return widget
    

from enthought.pyface.workbench.api import TraitsUIView
from enthought.traits.ui.api import View, Item
from enthought.traits.api import Instance
from enthought.envisage.ui.workbench.workbench_window import WorkbenchWindow

class ExampleTraitsUIView(TraitsUIView):
    ''' An example TraitsUI view for a workbench application plugin 
    perspective.
    
    View are used to present information to the user to help them perform their
    current task. For example they can show the structure of a document as a 
    tree where clicking on a tree node moves the cursor to the relevant 
    section. 
    
    A TraitsUIView must contain a View object.
    
    '''
    category = 'Example'
    id = 'infobiotics.dashboard.plugins.example.views.ExampleTraitsUIView'
    name = 'ExampleTraitsUIView'
    position = 'right'
    width = 0.3

    window_trait = Instance(WorkbenchWindow)

    def _window_trait_default(self):
        return self.window

    traits_view = View(
        Item('window_trait', label='window')
    )    