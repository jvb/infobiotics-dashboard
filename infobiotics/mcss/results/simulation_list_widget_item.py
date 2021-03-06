from PyQt4.QtGui import QListWidgetItem
from species import Species
from compartment import Compartment
from run import Run
from simulation import Simulation

class SimulationListWidgetItem(QListWidgetItem):

    def __init__(self, data, parent=None):
        self.data = data

        if isinstance(data, Species):
            text = data.name
            self.amounts_index = data.index
            
        elif isinstance(data, Compartment):
            text = data.compartment_name_and_xy_coords()
            self.amounts_index = data.index

        elif isinstance(data, Run):
            text = "%s" % (data._run_number)
            self.amounts_index = data._run_number - 1

#        elif isinstance(data, Simulation):
#            text = "%s %s" % (data.model_input_file, data.simulation_start_time)
#            self.amounts_index = None

        else:
            raise TypeError("type of data is not recognised")

        QListWidgetItem.__init__(self, text, parent, QListWidgetItem.UserType) # QObject::startTimer: QTimer can only be used with threads started with QThread
        
        if isinstance(self.amounts_index, int):
            self.setToolTip('%d' % self.amounts_index)
