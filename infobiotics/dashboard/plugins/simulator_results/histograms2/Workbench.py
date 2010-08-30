# This file is part of the Infobiotics Workbench. See LICENSE for copyright.
# $Id: __init__.py 286 2009-08-25 17:51:05Z jvb $
# $HeadURL: https://psiren.cs.nott.ac.uk/repos/infobiotics/gui-current/trunk/src/metamodel/__init__.py $
# $Author: jvb $
# $Revision: 286 $
# $Date: 2009-08-25 18:51:05 +0100 (Tue, 25 Aug 2009) $


from SimulationWidgets import *
from SimulationDatasets import Simulation, amountsFromIndices
from actions import addActions, createAction
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from HistogramWidget import HistogramWidget


organisationName = 'Infobiotics'
applicationName = 'Infobiotics Workbench'


class Workbench(QMainWindow):
    
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.setupUi()
        self.setWindowTitle(applicationName)
        
        self.restoreSettings()

        self.updateUi()
        
#        self.connect(self.mdiArea, SIGNAL('subWindowActivated(QMdiSubWindow*)'), self.subWindowActivated)
#        
#    def subWindowActivated(self, subWindow): #TODO
#        if subWindow is not No:
#            print subWindow.windowTitle()
#        
        
    # settings    
        
    def closeEvent(self, event):
        # save settings
        self.settings.setValue("state", QVariant(self.saveState()))
        self.settings.setValue("geometry", QVariant(self.saveGeometry()))
        
        QMainWindow.closeEvent(self, event)


    def restoreSettings(self):
        self.settings = QSettings(organisationName, applicationName)
        
        state = self.settings.value("state").toByteArray()
        if len(state) != 0:
            self.restoreState(state)
        
        geometry = self.settings.value("geometry").toByteArray()
        if len(geometry) != 0:
            self.restoreGeometry(geometry)
        else:
            self.resize(800, 600)
            from functions import centreWindow
            centreWindow(self)
            

    # UI
    
    def setupUi(self):
        self.createStatusBar()

        self.createActions()
        self.createMenus()
        self.createToolBars()

        self.createDockWidgets()

        self.mdiArea = QMdiArea(self)
        self.setCentralWidget(self.mdiArea)
        

    def createStatusBar(self):
        self.statusBar().showMessage('Ready', 2000)
        
        
    def createActions(self):
        self.openSimulationAction = createAction(self, '&Open Simulation...', slot=self.openSimulation)
        self.closeSimulationAction = createAction(self, '&Close Simulation', slot=self.closeSimulation)
        self.exitAction = createAction(self, 'E&xit', slot=self.close)
        
        self.plotHistogramAction = createAction(self, '&Histogram', slot=self.plotHistogram)
        self.plotSurfaceAction = createAction(self, '&Surface', slot=self.plotSurface)
        self.plotTimeseriesAction = createAction(self, '&Timeseries', slot=self.plotTimeseries)
        
            
    def createMenus(self):
        self.fileMenu = QMenu('&File', self)
        addActions(self.fileMenu, [self.openSimulationAction, self.closeSimulationAction, None, self.exitAction])
        self.menuBar().addMenu(self.fileMenu)

        self.plotMenu = QMenu('&Plot', self)
        addActions(self.plotMenu, [self.plotTimeseriesAction, self.plotHistogramAction, self.plotSurfaceAction])
        self.menuBar().addMenu(self.plotMenu)

#        self.windowMenu = QMenu('&Window', self)
#        self.menuBar().addMenu(self.windowMenu)
#        self.openPerspectiveMenu = QMenu('&Open Perspective', self)
#        self.showViewMenu = QMenu('Show &View', self)
#        self.windowMenu.addMenu(self.openPerspectiveMenu)
#        self.windowMenu.addMenu(self.showViewMenu)

        self.helpMenu = QMenu('&Help', self) 
        addActions(self.helpMenu, [createAction(self, 'About &Qt', slot=QApplication.aboutQt)])
        self.menuBar().addMenu(self.helpMenu)

        
    def createToolBars(self):
        self.fileToolBar = QToolBar('File')
        self.fileToolBar.setObjectName('fileToolBar')
        addActions(self.fileToolBar, [self.openSimulationAction, self.closeSimulationAction])
        
        self.plotToolBar = QToolBar('Plot')
        self.plotToolBar.setObjectName('plotToolBar')
        addActions(self.plotToolBar, [self.plotTimeseriesAction, self.plotHistogramAction, self.plotSurfaceAction])

        self.addToolBar(self.fileToolBar)
#        self.addToolBarBreak()
        self.addToolBar(self.plotToolBar)


    def createDockWidgets(self):
#        self.setDocumentMode(True)
        self.setDockNestingEnabled(True)
        
        # Simulations
        self.simulationsDockWidget = QDockWidget('Simulations', self)
        self.simulationsDockWidget.setObjectName('simulationsDockWidget')
        self.simulationsListWidget = QListWidget()
        self.simulationsDockWidget.setWidget(self.simulationsListWidget)
        self.simulationsListWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.connect(self.simulationsListWidget, SIGNAL('currentItemChanged(QListWidgetItem*, QListWidgetItem*)'), self.simulationListWidgetCurrentItemChanged)
        self.connect(self.simulationsListWidget, SIGNAL('currentItemChanged(QListWidgetItem*, QListWidgetItem*)'), self.updateUi)
        self.connect(self.simulationsListWidget, SIGNAL('itemDoubleClicked(QListWidgetItem*)'), self.newEditor)

        self.speciesDockWidget = QDockWidget('Species')
        self.speciesDockWidget.setObjectName('speciesDockWidget')
        
        self.compartmentsDockWidget = QDockWidget('Compartments')
        self.compartmentsDockWidget.setObjectName('compartmentsDockWidget')
        
        self.runsDockWidget = QDockWidget('Runs')
        self.runsDockWidget.setObjectName('runsDockWidget')
        
        self.addDockWidget(Qt.DockWidgetArea(Qt.TopDockWidgetArea), self.simulationsDockWidget)
        self.addDockWidget(Qt.DockWidgetArea(Qt.RightDockWidgetArea), self.speciesDockWidget)
        self.splitDockWidget(self.speciesDockWidget, self.runsDockWidget, Qt.Vertical)
        self.splitDockWidget(self.speciesDockWidget, self.compartmentsDockWidget, Qt.Horizontal)

        self.dockWidgets = [self.speciesDockWidget,
                            self.compartmentsDockWidget,
                            self.runsDockWidget]
        
        for dockWidget in self.dockWidgets:
            dockWidget.setWidget(QListWidget())


    # slots

    def updateUi(self):
        if self.simulationsListWidget.currentItem() is None:
            self.closeSimulationAction.setEnabled(False)
            self.plotHistogramAction.setEnabled(False)
            self.plotSurfaceAction.setEnabled(False)
            self.plotTimeseriesAction.setEnabled(False)
            self.compartmentsDockWidget.setEnabled(False)
            self.speciesDockWidget.setEnabled(False)
            self.runsDockWidget.setEnabled(False)
        else:
            self.closeSimulationAction.setEnabled(True)
            self.plotHistogramAction.setEnabled(True)
            self.plotSurfaceAction.setEnabled(True)
            self.plotTimeseriesAction.setEnabled(True)
            self.compartmentsDockWidget.setEnabled(True)
            self.speciesDockWidget.setEnabled(True)
            self.runsDockWidget.setEnabled(True)

            
    def closeSimulation(self):
        simulationItem = self.simulationsListWidget.takeItem(self.simulationsListWidget.currentRow())
        for dockWidget in self.dockWidgets:
            dockWidget.setWidget(QListWidget())
        del simulationItem
        
                
    def openSimulation(self, fileName=None):
        if fileName is None:
            fileName = unicode(QFileDialog.getOpenFileName(self,
                'Select a simulation file to open',
                '/home/jvb/phd/models',
                'HDF5 files (*.h5 *.hd5 *.hdf5)'))
        if fileName != '':
            item = SimulationListWidgetItem(fileName)
            self.simulationsListWidget.addItem(item)
            self.simulationsListWidget.setCurrentItem(item)
            self.statusBar().showMessage('Opened %s' % fileName, 2000)
            

    def simulationListWidgetCurrentItemChanged(self, current, previous):
        if current is not None:
            self.setSpeciesWidget(current.speciesWidget())
            self.setCompartmentsWidget(current.compartmentsWidget())
            self.setRunsWidget(current.runsWidget())

    def setCompartmentsWidget(self, widget):
        self.compartmentsDockWidget.setWidget(widget)

    def setSpeciesWidget(self, widget):
        self.speciesDockWidget.setWidget(widget)
        
    def setRunsWidget(self, widget):
        self.runsDockWidget.setWidget(widget)
        
        
    def checkedIndices(self):
        currentSimulationListWidgetItem = self.simulationsListWidget.currentItem()
        if currentSimulationListWidgetItem is None:
            print 'self.simulationsListWidget.currentItem() == None'
            return None
        else:
            checkedSpeciesItems = currentSimulationListWidgetItem.speciesWidget().checkedItems()
            if len(checkedSpeciesItems) > 0:
                listOfSpeciesIndices = [item.amountsIndex for item in checkedSpeciesItems]
            else:
                title = 'No checked species'
                text = 'Please check some species before continuing.'
                QMessageBox.critical(self, title, text) 
                return None
            
            checkedCompartmentItems = currentSimulationListWidgetItem.compartmentsWidget().checkedItems()
            if len(checkedCompartmentItems) > 0:
                listOfCompartmentIndices = [item.amountsIndex for item in checkedCompartmentItems] 
            else:
                title = 'No checked compartments'
                text = 'Please check some compartments before continuing.'
                QMessageBox.critical(self, title, text)
                return None 
            
            checkedRunItems = currentSimulationListWidgetItem.runsWidget().checkedItems()
            if len(checkedRunItems) > 0:
                listOfRunIndices = [item.amountsIndex for item in checkedRunItems] 
            else:
                title = 'No checked runs'
                text = 'Please check some runs before continuing.'
                QMessageBox.critical(self, title, text)
                return None 
            
            return listOfSpeciesIndices, listOfCompartmentIndices, listOfRunIndices


    def plotHistogram(self):
        checkedIndices = self.checkedIndices()
        if checkedIndices is not None:
            listOfSpeciesIndices, listOfCompartmentIndices, listOfRunIndices = checkedIndices

            simulation = self.simulationsListWidget.currentItem().simulation
            listOfTimepointIndices = simulation.listOfTimepointIndicesOfNonTruncatedRuns()[:-1] 
            
            # extract amounts for all checked species, compartments and runs, and their indices
            tup = amountsFromIndices(simulation.fileName,
                                     listOfSpeciesIndices,
                                     listOfCompartmentIndices,
                                     listOfTimepointIndices,
                                     listOfRunIndices)

            # unpack tup
            amounts, listOfSpeciesIndices, listOfCompartmentIndices, listOfTimepointIndices, listOfRunIndices = tup
            
            #TODO use the actual timepoints
            timepoints = listOfTimepointIndices 
            
            # create histograms
            for i, speciesIndex in enumerate(listOfSpeciesIndices):
                species = simulation.dictionaryOfSpecies[speciesIndex]
                title = 'Histogram of %s in %s' % (species.species_name, simulation.fileName.split('/')[-1])
                widget = HistogramWidget(title, amounts[i, ..., 0], timepoints, parent=self)
                subWindow = self.mdiArea.addSubWindow(widget)
                subWindow.setWindowTitle(title)
                subWindow.show()
                
            
            self.mdiArea.tileSubWindows()
            
    
    def plotSurface(self):
        checkedIndices = self.checkedIndices()
        if checkedIndices is not None:
            self.newEditor()
    
    def plotTimeseries(self):
        checkedIndices = self.checkedIndices()
        if checkedIndices is not None:
            self.newEditor()

    def newEditor(self):
        currentSimulationListWidgetItem = self.simulationsListWidget.currentItem()
        if currentSimulationListWidgetItem is None:
            print 'self.simulationsListWidget.currentItem() == None'
            return None
        else:
#            editor = Editor(currentSimulationListWidgetItem.simulation)
#            self.mdiArea.addSubWindow(editor)
#            editor.show()
#            return editor 

            widget = QTextEdit('test', self)
#            widget.setAttribute(Qt.WA_DeleteOnClose)
            widget.setReadOnly(True)
            self.mdiArea.addSubWindow(widget).show()



class SimulationListWidgetItem(QListWidgetItem):

    def __init__(self, fileName, parent=None):
        self.simulation = Simulation.fromH5File(fileName)
        self.speciesListWidget = SpeciesListWidget(self.simulation.listOfSpecies) 
        self.compartmentsListWidget = CompartmentsListWidget(self.simulation.listOfInitialCompartments())
        
        # sort compartments
        self.compartmentsListWidget.sortItems()
        self.compartmentsListWidget.setSortingEnabled(True)
        
        
        self.runsListWidget = RunsListWidget(self.simulation.listOfRuns)
        text = '%s (%s)' % (self.simulation.fileName, self.simulation.model_input_file)
        QListWidgetItem.__init__(self, text, parent)

    def speciesWidget(self):
        return self.speciesListWidget

    def compartmentsWidget(self):
        return self.compartmentsListWidget

    def runsWidget(self):
        return self.runsListWidget



class Editor(QMdiSubWindow):
    '''
    For histograms, surfaces and timeseries (so far).
    '''
    
    def __init__(self, simulation):
        QMdiSubWindow.__init__(self)
        self.setAttribute(Qt.WA_DeleteOnClose)
        
        self.setWidget(QTextEdit(self))

        self.simulation = simulation
        







if __name__ == '__main__':
    app = QApplication([])
    w = Workbench()
    w.show()
#    w.openSimulation('/media/backup/weasel/models/circularPattern_05.h5')
#    w.openSimulation('/home/jvb/phd/eclipse/infobiotics/2sat/SP_UnRegModel.h5')
#    w.openSimulation('/home/jvb/phd/eclipse/infobiotics/2sat/SP_PARModel.h5')
#    w.openSimulation('/home/jvb/phd/eclipse/infobiotics/2sat/SP_NARModel.h5')
    exit(qApp.exec_())
