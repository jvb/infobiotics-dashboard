# This file is part of the Infobiotics Workbench. See LICENSE for copyright.
# $Id: __init__.py 286 2009-08-25 17:51:05Z jvb $
# $HeadURL: https://psiren.cs.nott.ac.uk/repos/infobiotics/gui-current/trunk/src/metamodel/__init__.py $
# $Author: jvb $
# $Revision: 286 $
# $Date: 2009-08-25 18:51:05 +0100 (Tue, 25 Aug 2009) $


from SimulationDatasets import Simulation, attributesOfRange
from actions import addActions, createAction

import sys
import numpy

#import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure

from PyQt4.QtCore import *
from PyQt4.QtGui import *


class HistogramWidget(QMainWindow):

    def setTimeIndex(self, timeIndex):
        self.setData(self.amounts[:, timeIndex])
        
    def setData(self, data=None):
        if data is None:
            self.data = numpy.random.normal(1, 1, 1000)
        else:
            self.data = data
        self.onDraw() 


    def __init__(self, title, amounts, timepoints, parent=None):
        QMainWindow.__init__(self, parent)
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.title = title
        self.amounts = amounts
        self.timepoints = timepoints
        
        self.createMenu()
        self.createStatusBar()
        self.createCentralWidget()
        
#        self.setTimeIndex(0)
        self.timeSlider.setValue(0)

    def closeEvent(self, event):
        self.parent().removeToolBar(self.toolBar)
        QWidget.closeEvent(self, event)
        
    def updateBinsSliderToolTip(self, value):
        self.binsSlider.setToolTip('%s' % value)
        
    def createCentralWidget(self):
        self.centralWidget = QWidget(self)

        self.dpi = 100
        figure = Figure((5.0, 4.0), dpi=self.dpi)
        self.canvas = FigureCanvas(figure)
        self.canvas.setParent(self.centralWidget)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.canvas.mpl_connect('pick_event', self.onPick)

        self.axes = figure.add_subplot(111)
#        self.axes.hold(False) # use self.axes.clear in onDraw() instead
        
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.centralWidget)
        self.toolBar = self.parent().addToolBar(self.title)
        self.toolBar.setObjectName(self.title)
        self.toolBarAction = self.toolBar.addWidget(self.mpl_toolbar)
        
        self.showGridCheckBox = QCheckBox("Show &Grid")
        self.showGridCheckBox.setChecked(False)
        self.connect(self.showGridCheckBox, SIGNAL('stateChanged(int)'), self.onDraw)
        
        self.logScaleCheckBox = QCheckBox("&Log scale")
        self.logScaleCheckBox.setChecked(False)
        self.connect(self.logScaleCheckBox, SIGNAL('stateChanged(int)'), self.onDraw)
        
        self.logBaseComboBox = QComboBox()
        self.logBaseComboBox.setToolTip('Log &base')
        self.logBaseComboBox.addItems(QStringList([u'10', u'2', unicode(numpy.e)]))
        self.logBaseComboBox.setEnabled(self.logScaleCheckBox.checkState())
        self.connect(self.logBaseComboBox, SIGNAL('currentIndexChanged(int)'), self.onDraw)
        self.connect(self.logScaleCheckBox, SIGNAL('stateChanged(int)'), self.logBaseComboBox.setEnabled)
        
        binsSliderLabel = QLabel('Bins:')
        self.binsSlider = QSlider(Qt.Horizontal)
        self.binsSlider.setRange(5, 100)
        self.binsSlider.setValue(20)
        self.binsSlider.setTracking(True)
        self.binsSlider.setTickPosition(QSlider.TicksBelow)
        self.connect(self.binsSlider, SIGNAL('valueChanged(int)'), self.onDraw)
        self.connect(self.binsSlider, SIGNAL('valueChanged(int)'), self.updateBinsSliderToolTip)
        
        # Layout with box sizers
        h = QHBoxLayout()
        for w in [self.showGridCheckBox,
                  self.logScaleCheckBox, self.logBaseComboBox,
                  binsSliderLabel, self.binsSlider,
                  ]:
            h.addWidget(w)
            h.setAlignment(w, Qt.AlignVCenter)

        timeSliderLabel = QLabel('Time:')
        self.timeSlider = QSlider(Qt.Horizontal)
        self.timeSlider.setTracking(True)
        self.timeSlider.setTickPosition(QSlider.TicksBelow)
        self.connect(self.timeSlider, SIGNAL('valueChanged(int)'), self.setTimeIndex)
        start, stop, step = attributesOfRange(self.timepoints)
        self.timeSlider.setRange(start, stop)
        self.timeSlider.setSingleStep(step)
        
                
        h2 = QHBoxLayout()
        h2.addWidget(timeSliderLabel)
        h2.addWidget(self.timeSlider)
        
        v = QVBoxLayout(self.centralWidget)
        v.addWidget(self.canvas)
#        v.addWidget(self.mpl_toolbar)
        v.addLayout(h2)
        v.addLayout(h)
        
        self.setCentralWidget(self.centralWidget)


    def onDraw(self):
        """ Redraws the figure. """
        
        self.axes.clear()
        
        self.axes.set_title(self.title)
        
        self.axes.grid(self.showGridCheckBox.isChecked())
        
        self.axes.set_yscale('log' if self.logScaleCheckBox.isChecked() else 'linear',
                             basey=float(self.logBaseComboBox.currentText()))

#        mu, sigma = 100, 15
#        x = mu + sigma * np.random.randn(10000)
#        
#        fig = plt.figure()
#        ax = fig.add_subplot(111)
#        
#        # the histogram of the data
#        n, bins, patches = ax.hist(x, 50, normed=1, facecolor='green', alpha=0.75)
#        
#        # hist uses np.histogram under the hood to create 'n' and 'bins'.
#        # np.histogram returns the bin edges, so there will be 50 probability
#        # density values in n, 51 bin edges in bins and 50 patches.  To get
#        # everything lined up, we'll compute the bin centers
#        bincenters = 0.5*(bins[1:]+bins[:-1])
#        # add a 'best fit' line for the normal PDF
#        y = mlab.normpdf( bincenters, mu, sigma)
#        l = ax.plot(bincenters, y, 'r--', linewidth=1)
#        
#        ax.set_xlabel('Smarts')
#        ax.set_ylabel('Probability')
#        #ax.set_title(r'$\mathrm{Histogram\ of\ IQ:}\ \mu=100,\ \sigma=15$')
#        ax.set_xlim(40, 160)
#        ax.set_ylim(0, 0.03)
#        ax.grid(True)
#        
#        plt.show()
        
        self.axes.hist(self.data,
                       bins=self.binsSlider.value(),
                       cumulative=False,
                       histtype='bar', #'barstacked','step','stepfilled',
                       log=False)
        
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
        
        loadFileAction = createAction(self, "&Save plot",
                                           shortcut="Ctrl+S",
                                           slot=self.savePlot,
                                           tip="Save the plot")
        quitAction = createAction(self, "&Quit",
                                       slot=self.close,
                                       shortcut="Ctrl+Q",
                                       tip="Close the application")
        
        addActions(self.fileMenu, (loadFileAction, None, quitAction))
        
#        aboutAction = createAction(self, "&About", 
#                                        shortcut='F1', 
#                                        slot=self.onAbout, 
#                                        tip='About the demo')
#        self.helpMenu = self.menuBar().addMenu("&Help")
#        addActions(self.helpMenu, (aboutAction,))
#
#
#    def onAbout(self):
#            msg = """ A demo of using PyQt with matplotlib:
#            
#        * Use the matplotlib navigation bar
#        * Add values to the text box and press Enter (or click "Draw")
#        * Show or hide the grid
#        * Drag the binsSlider to modify the width of the bars
#        * Save the plot to a file using the File menu
#        * Click on a bar to receive an informative message
#        """
#            QMessageBox.about(self, "About the demo", msg)#.strip())
        
        

if __name__ == "__main__":
    QApplication([])
    w = HistogramWidget()
    w.show()
    from shared.widgets import centre_window; centre_window(w)
    qApp.exec_()
