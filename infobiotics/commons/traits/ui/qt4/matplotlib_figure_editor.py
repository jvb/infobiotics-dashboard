from enthought.traits.ui.qt4.editor import Editor
from enthought.traits.api import Instance
from PyQt4.QtGui import QWidget, QSizePolicy
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from enthought.traits.ui.basic_editor_factory import BasicEditorFactory

class _MPLFigureEditor(Editor):
    scrollable = True
    widget = Instance(QWidget)
    
    def init(self, parent):
        ''' self.value is the trait being edited. '''
        
#        # with additional widgets such as the Matplotlib navigation toolbar
#        widget = QWidget()
#        widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
#        layout = QGridLayout(widget)
#        mpl_control = FigureCanvas(self.value)
#        layout.addWidget(mpl_control)
#        toolbar = NavigationToolbar(mpl_control, widget)
#        layout.addWidget(toolbar)

        # without additional widgets
        widget = FigureCanvas(self.value)
        widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
#        widget.setMinimumSize(300,300)
        
        self.control = widget
#        self.set_tooltip('')
    
    def update_editor(self):
        pass
#        self.control.update()

    def update(self, value):
        self.widget.figure.canvas.draw()
    

class MPLFigureEditor(BasicEditorFactory):
    klass = _MPLFigureEditor
