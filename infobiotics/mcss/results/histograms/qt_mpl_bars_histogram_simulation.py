import sys

import numpy

from PyQt4.QtCore import *
from PyQt4.QtGui import *

#import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure


class HistogramMainWindow(QMainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.createMenu()
        self.createStatusBar()
        self.createCentralWidget()

        self.createData()
        

    def createData(self):
                
        run_indicies = [0]
        compartment_indicies = range(1000)#[0]
        species_indicies = [0]
        
        if len(compartment_indicies) > 1 and len(run_indicies) > 1:
            pass
            # ask user if they want to average runs or select one compartment only
        
        import tables
        h5 = tables.openFile('/home/jvb/phd/models/circularPattern_05.h5')
        root = h5.root

        # for each/sum species
        # produce a 2D array of species amount x time
        # across multiple compartments for one run or the average of all runs
        # or 
        # across multiple runs in one compartment   
        
        instances = len(compartment_indicies)
#        instances = len(run_indicies)
    
        number_of_timepoints = root.run1._v_attrs.number_of_timepoints

        time_indicies = range(number_of_timepoints)
        
        self.array = numpy.zeros((len(time_indicies), instances))

        for t in time_indicies:
            self.array[t] = numpy.random.normal(1, 1, instances)

        print self.array
        print self.array.shape
        self.setData(self.array[0])

        h5.close()
        

    def setTimeIndex(self, timeIndex):
        self.setData(self.array[timeIndex])

        
    def setData(self, data=None):
        if data is None:
            self.data = numpy.random.normal(1, 1, 1000)
        else:
            self.data = data
        self.onDraw() 


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
        
        resampleButton = QPushButton('Resample')
        self.connect(resampleButton, SIGNAL('clicked()'), self.setData)

        # Layout with box sizers
        h = QHBoxLayout()
        for w in [self.showGridCheckBox,
                  self.logScaleCheckBox, self.logBaseComboBox,
                  binsSliderLabel, self.binsSlider,
#                  resampleButton
                  ]:
            h.addWidget(w)
            h.setAlignment(w, Qt.AlignVCenter)

        timeSliderLabel = QLabel('Time:')
        self.timeSlider = QSlider(Qt.Horizontal)
        self.timeSlider.setTracking(True)
        self.timeSlider.setTickPosition(QSlider.TicksBelow)
        self.connect(self.timeSlider, SIGNAL('valueChanged(int)'), self.setTimeIndex)
        self.timeSlider.setRange(0, 100)
        self.timeSlider.setValue(0)
        
        h2 = QHBoxLayout()
        h2.addWidget(timeSliderLabel)
        h2.addWidget(self.timeSlider)
        
        v = QVBoxLayout(self.centralWidget)
        v.addWidget(self.canvas)
        v.addWidget(self.mpl_toolbar)
        v.addLayout(h2)
        v.addLayout(h)
        
        self.setCentralWidget(self.centralWidget)


    def onDraw(self):
        """ Redraws the figure. """
        
        self.axes.clear()
        
        self.axes.grid(self.showGridCheckBox.isChecked())
        
        self.axes.set_yscale('log' if self.logScaleCheckBox.isChecked() else 'linear', basey=float(self.logBaseComboBox.currentText()))

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
    w = HistogramMainWindow()
    w.show()
    qApp.exec_()


if __name__ == "__main__":
    main()
