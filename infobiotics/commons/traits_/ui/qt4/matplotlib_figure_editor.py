from traits.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'qt4'
from traitsui.qt4.editor import Editor
from PyQt4.QtGui import QWidget, QSizePolicy, QGridLayout, QIcon
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from traitsui.basic_editor_factory import BasicEditorFactory
from traits.api import Bool
import os
from infobiotics.commons.matplotlib.matplotlib_figure_size import resize_and_save_matplotlib_figure

# http://groups.google.com/group/pyinstaller/msg/64e9a5987ba102f3
class VMToolbar(NavigationToolbar): 
    def __init__(self, plotCanvas, parent, coordinates): 
        NavigationToolbar.__init__(self, plotCanvas, parent, coordinates) 
    def _icon(self, name): 
        #dirty hack to use exclusively .png and thus avoid .svg usage 
        #because .exe generation is problematic with .svg 
        name = name.replace('.svg','.png') 
        return QIcon(os.path.join(self.basedir, name)) 

class VMToolbarWithSaveResizedAction(VMToolbar):
    def __init__(self, plotCanvas, parent, coordinates):
        VMToolbar.__init__(self, plotCanvas, parent, coordinates)
        a = self.addAction(self._icon('filesave.svg'), 'Save resized', self.resize_and_save)
        a.setIconText('Save resized')
        a.setToolTip('Save the figure resized in inches or pixels')
    def resize_and_save(self):
        resize_and_save_matplotlib_figure(self.canvas.figure)

class _MatplotlibFigureEditor(Editor):
#    scrollable = True
    
    def init(self, parent):
        ''' self.value is the trait being edited. '''

        figure = self.value
        canvas = FigureCanvas(figure)
        canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        widget = QWidget(parent.parent()) # might break if Traits UI changes Editor parent in future releases
        widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        layout = QGridLayout(widget)
        
        if self.factory.toolbar:
            toolbar = VMToolbarWithSaveResizedAction(canvas, widget, coordinates=True)
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
