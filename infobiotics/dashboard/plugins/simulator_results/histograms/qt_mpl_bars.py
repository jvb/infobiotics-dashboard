"""
This demo demonstrates how to embed a matplotlib (mpl) plot 
into a PyQt4 GUI application, including:

* Using the navigation toolbar
* Adding data to the plot
* Dynamically modifying the plot's properties
* Processing mpl events
* Saving the plot to a file from a menu

The main goal is to serve as a basis for developing rich PyQt GUI
applications featuring mpl plots (using the mpl OO API).

Eli Bendersky (eliben@gmail.com)
License: this code is in the public domain
Last modified: 19.01.2009
"""


import sys, os, random

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        
        self.setAttribute(Qt.WA_DeleteOnClose)
        
        self.setWindowTitle('Demo: PyQt with matplotlib')

        self.createMenu()
        self.createCentralWidget()
        self.createStatusBar()

        self.textInputBox.setText('1 2 3 4')
        self.onDraw()


    def createCentralWidget(self):
        self.centralWidget = QWidget(self)
        
        # Create the mpl Figure and FigCanvas objects. 
        # 5x4 inches, 100 dots-per-inch
        #
        self.dpi = 100
        figure = Figure((5.0, 4.0), dpi=self.dpi)
        self.canvas = FigureCanvas(figure)
        self.canvas.setParent(self.centralWidget)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Since we have only one plot, we can use add_axes 
        # instead of add_subplot, but then the subplot
        # configuration tool in the navigation toolbar wouldn't
        # work.
        self.axes = figure.add_subplot(111)
        
        # Bind the 'pick' event for clicking on one of the bars
        self.canvas.mpl_connect('pick_event', self.onPick)
        
        # Create the navigation toolbar, tied to the canvas
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.centralWidget)
        
        # Other GUI controls
        self.textInputBox = QLineEdit()
        self.textInputBox.setMinimumWidth(200)
        self.connect(self.textInputBox, SIGNAL('editingFinished()'), self.onDraw)
        
        self.drawButton = QPushButton("&Draw")
        self.connect(self.drawButton, SIGNAL('clicked()'), self.onDraw)
        
        self.showGridCheckBox = QCheckBox("Show &Grid")
        self.showGridCheckBox.setChecked(False)
        self.connect(self.showGridCheckBox, SIGNAL('stateChanged(int)'), self.onDraw)
        
        sliderLabel = QLabel('Bar width (%):')
        self.binsSlider = QSlider(Qt.Horizontal)
        self.binsSlider.setRange(1, 100)
        self.binsSlider.setValue(20)
        self.binsSlider.setTracking(True)
        self.binsSlider.setTickPosition(QSlider.TicksBothSides)
        self.connect(self.binsSlider, SIGNAL('valueChanged(int)'), self.onDraw)
        
        # Layout with box sizers
        h = QHBoxLayout()
        for w in [self.textInputBox, self.drawButton, self.showGridCheckBox,
                  sliderLabel, self.binsSlider]:
            h.addWidget(w)
            h.setAlignment(w, Qt.AlignVCenter)
        
        v = QVBoxLayout(self.centralWidget)
        v.addWidget(self.canvas)
        v.addWidget(self.mpl_toolbar)
        v.addLayout(h)
        
        self.setCentralWidget(self.centralWidget)


    def onDraw(self):
        """ Redraws the figure. """
        text = unicode(self.textInputBox.text())
        self.data = map(int, text.split())
        
        x = range(len(self.data))

        # clear the axes and redraw the plot anew
        self.axes.clear()        
        self.axes.grid(self.showGridCheckBox.isChecked())
        
        self.axes.set_yscale('log')

        
        self.axes.bar(
            left=x,
            height=self.data,
            width=self.binsSlider.value() / 100.0,
            align='center',
            alpha=0.44,
            picker=5)
        
        self.canvas.draw()
    

    def savePlot(self):
        filters = "PNG (*.png)|*.png"
        
        filePath = unicode(QFileDialog.getSaveFileName(self, 'Save plot', '', filters))
        if filePath:
            self.canvas.print_figure(filePath, dpi=self.dpi)
            self.statusBar().showMessage('Saved to %s' % filePath, 2000)

    
    def onPick(self, event):
        # The event received here is of the type
        # matplotlib.backend_bases.PickEvent
        #
        # It carries lots of information, of which we're using
        # only a small amount here.
        box_points = event.artist.get_bbox().get_points()
        msg = "You've clicked on a bar with coords:\n %s" % box_points
        QMessageBox.information(self, "Click!", msg)

    
    def createStatusBar(self):
        self.statusText = QLabel("This is a demo")
        self.statusBar().addWidget(self.statusText, 1)
    
        
    def createMenu(self):        
        self.fileMenu = self.menuBar().addMenu("&File")
        
        loadFileAction = self.createAction("&Save plot",
                                           shortcut="Ctrl+S",
                                           slot=self.savePlot,
                                           tip="Save the plot")
        quitAction = self.createAction("&Quit",
                                       slot=self.close,
                                       shortcut="Ctrl+Q",
                                       tip="Close the application")
        
        self.addActions(self.fileMenu, (loadFileAction, None, quitAction))
        
        aboutAction = self.createAction("&About",
                                        shortcut='F1',
                                        slot=self.onAbout,
                                        tip='About the demo')
        self.helpMenu = self.menuBar().addMenu("&Help")
        self.addActions(self.helpMenu, (aboutAction,))


    def addActions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)


    def createAction(self, text, slot=None, shortcut=None,
                           icon=None, tip=None, checkable=False,
                           signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(":/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            self.connect(action, SIGNAL(signal), slot)
        if checkable:
            action.setCheckable(True)
        return action


    def onAbout(self):
            msg = """ A demo of using PyQt with matplotlib:
            
        * Use the matplotlib navigation bar
        * Add values to the text box and press Enter (or click "Draw")
        * Show or hide the grid
        * Drag the binsSlider to modify the width of the bars
        * Save the plot to a file using the File menu
        * Click on a bar to receive an informative message
        """
            QMessageBox.about(self, "About the demo", msg)#.strip())
        
        

def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    qApp.exec_()


if __name__ == "__main__":
    main()
