from enthought.traits.ui.qt4.editor import Editor
from PyQt4.QtGui import QWidget, QSizePolicy, QGridLayout
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from enthought.traits.ui.basic_editor_factory import BasicEditorFactory
from enthought.traits.api import Bool

class _MPLFigureEditor(Editor):
#    scrollable = True
    
    def init(self, parent):
        ''' self.value is the trait being edited. '''
        
        widget = QWidget()
        widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout = QGridLayout(widget)
        canvas = FigureCanvas(self.value)
        canvas.resize(200,200)
        toolbar = NavigationToolbar(canvas, widget)
        if self.factory.toolbar:
            layout.addWidget(toolbar)
        layout.addWidget(canvas)
        self.control = widget

#        self.set_tooltip('')
    
    def update_editor(self):
        pass
#        self.control.update()

#    def update(self, value):
#        self.control.figure.canvas.draw()
    

class MPLFigureEditor(BasicEditorFactory):
    klass = _MPLFigureEditor
    toolbar = Bool