from enthought.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'qt4'
from enthought.traits.ui.qt4.editor import Editor
from PyQt4.QtGui import QWidget, QSizePolicy, QGridLayout, QIcon
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from enthought.traits.ui.basic_editor_factory import BasicEditorFactory
from enthought.traits.api import Bool
import os

# http://groups.google.com/group/pyinstaller/msg/64e9a5987ba102f3
class VMToolbar(NavigationToolbar): 
    def __init__(self, plotCanvas, parent): 
        NavigationToolbar.__init__(self, plotCanvas, parent) 
    def _icon(self, name): 
        #dirty hack to use exclusively .png and thus avoid .svg usage 
        #because .exe generation is problematic with .svg 
        name = name.replace('.svg','.png') 
        return QIcon(os.path.join(self.basedir, name)) 

class _MatplotlibFigureEditor(Editor):
#    scrollable = True
    
    def init(self, parent):
        ''' self.value is the trait being edited. '''

        figure = self.value
        canvas = FigureCanvas(figure)
        
        widget = QWidget()
        widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        layout = QGridLayout(widget)
        
        if self.factory.toolbar:
            toolbar = VMToolbar(canvas, widget, coordinates=True)
            if self.factory.toolbar_above:
                layout.addWidget(toolbar)
                layout.addWidget(canvas)
            else:
                layout.addWidget(canvas)
                layout.addWidget(toolbar)
        else:
            layout.addWidget(canvas)
        
        self.control = widget
    
    def update_editor(self):
        pass
        

class MatplotlibFigureEditor(BasicEditorFactory):
    klass = _MatplotlibFigureEditor
    toolbar = Bool
    toolbar_above = Bool(True)
