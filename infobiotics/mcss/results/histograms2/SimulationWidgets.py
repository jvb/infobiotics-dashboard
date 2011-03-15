# This file is part of the Infobiotics Workbench. See LICENSE for copyright.
# $Id: __init__.py 286 2009-08-25 17:51:05Z jvb $
# $HeadURL: https://psiren.cs.nott.ac.uk/repos/infobiotics/gui-current/trunk/src/metamodel/__init__.py $
# $Author: jvb $
# $Revision: 286 $
# $Date: 2009-08-25 18:51:05 +0100 (Tue, 25 Aug 2009) $


from SimulationDatasets import Simulation, Species, Run, Compartment 
from EnhancedListWidget import EnhancedListWidget
from PyQt4.QtGui import QListWidgetItem, QTreeWidget, QTreeWidgetItem
from PyQt4.QtCore import Qt, QStringList, QString
#from enthought.traits.api import HasTraits, Str, Int
#
#
#class Compartment(HasTraits):
#    
#    name = Str('compartment')
#    id = Int
#    index = Int



#class SimulationListWidgetItem(QListWidgetItem):
#
#    def __init__(self, data, parent=None):
#        QListWidgetItem.__init__(self, parent)
#        self.data = data
#        if isinstance(data, Species):
#            text = data.name
#            self.amounts_index = data.index
#        elif isinstance(data, Compartment):
#            text = data.compartment_name_and_xy_coords() #TODO fudge
#            self.amounts_index = data.index
#        elif isinstance(data, Run):
#            text = "%s" % (data.run_number)
#            self.amounts_index = data.run_number #? should probably be an index
#            self.setToolTip(unicode(data.number_of_timepoints))
##            print self.toolTip()
#        elif isinstance(data, Simulation):
#            text = "%s %s" % (data.model_input_file, data.simulation_start_time)
#            self.amounts_index = None
#        else:
#            text = None
#            raise TypeError("type of data is not recognised")
#        QListWidgetItem.__init__(self, text, parent)
        


class SpeciesListWidgetItem(QListWidgetItem):
    
    def __init__(self, species, parent=None):
        QListWidgetItem.__init__(self,
                                 species.species_name,
                                 parent)
        
        self.setCheckState(Qt.Unchecked)
        
        self.species = species
        
        self.amountsIndex = self.species.species_index
        
        
        
class SpeciesListWidget(EnhancedListWidget):
    
    def __init__(self, listOfSpecies, parent=None):
        EnhancedListWidget.__init__(self, parent)
        
        self.listOfSpecies = listOfSpecies
        
        for species in self.listOfSpecies:
            self.addItem(SpeciesListWidgetItem(species))
        
        if self.count() == 1:
            self.item(0).setCheckState(Qt.Checked)
            


class RunsListWidgetItem(QListWidgetItem):
    
    def __init__(self, run, parent=None):
        QListWidgetItem.__init__(self,
                                 QString(unicode(run.runNumber)), parent)                                 
        
        self.setCheckState(Qt.Unchecked)
        
        self.run = run
        
        self.amountsIndex = self.run.runIndex

    

class RunsListWidget(EnhancedListWidget):
    
    def __init__(self, listOfRuns, parent=None):
        EnhancedListWidget.__init__(self, parent)
        
        self.listOfRuns = listOfRuns
        
        for run in self.listOfRuns:
            self.addItem(RunsListWidgetItem(run))
            
        if self.count() == 1:
            self.item(0).setCheckState(Qt.Checked)            
        
        
            
class CompartmentsListWidgetItem(QListWidgetItem):
    
    def __init__(self, compartment, parent=None):
        QListWidgetItem.__init__(self,
                                 compartment.nameAndCoordinates(),
                                 parent)

        self.setCheckState(Qt.Unchecked)
        
        self.compartment = compartment
        
        self.amountsIndex = compartment.compartment_index


class CompartmentsListWidget(EnhancedListWidget):

    def __init__(self, listOfCompartments=[], parent=None):
        EnhancedListWidget.__init__(self, parent)
        
        self.setWindowTitle('Compartments')

        self.listOfCompartments = listOfCompartments
        
        for compartment in self.listOfCompartments:
            self.addItem(CompartmentsListWidgetItem(compartment))
        
        if self.count() == 1:
            self.item(0).setCheckState(Qt.Checked)


class CompartmentsTreeWidget(QTreeWidget):
    
    def __init__(self, listOfCompartments=[], parent=None):
        QTreeWidget.__init__(self, parent)

        self.setWindowTitle('Compartments')
        self.setRootIsDecorated(False)
        self.setHeaderLabels([
                              '',
                              'Name',
                              'X',
                              'Y'
                              ])
        
        self.listOfCompartments = listOfCompartments
    
        for compartment in self.listOfCompartments:
            self.addTopLevelItem(CompartmentsTreeWidgetItem(compartment)) # not strictly true, but how does Fran represent sub-compartments?

        for columnIndex in range(self.columnCount()):
            self.resizeColumnToContents(columnIndex)

    
class CompartmentsTreeWidgetItem(QTreeWidgetItem):
    
    def __init__(self, compartment, parent=None):
        if parent is None:
            QTreeWidgetItem.__init__(self,
                                     QStringList([
                                     unicode(''),
                                     unicode(compartment.compartment_name),
                                     unicode(compartment.compartment_x_position),
                                     unicode(compartment.compartment_y_position)
                                     ])
                                     )
        else:
            QTreeWidgetItem.__init__(self,
                                     parent,
                                     [
                                     compartment.compartment_name,
                                     compartment.compartment_x_position,
                                     compartment.compartment_y_position
                                     ] 
                                     )
            
        
        self.setCheckState(0, Qt.Unchecked)
        
        self.compartment = compartment
        
        self.amountsIndex = compartment.compartment_index







if __name__ == '__main__':
    from PyQt4.QtGui import QApplication
    app = QApplication([])
    
#    w = CompartmentsListWidget()
#    for i in range(0,10):
#        w.addItem(CompartmentsListWidgetItem('compartment %s' % i))

    listOfCompartments = [Compartment(i, i, 'compartment%s' % i, i, i, i, 0, i, None, None) for i in range(10)]
    for compartment in listOfCompartments:
        print compartment
    w = CompartmentsTreeWidget(listOfCompartments)
    w.setGeometry(640, 480, 640, 480)

    w.show()
    
    app.exec_()
