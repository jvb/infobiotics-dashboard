from __future__ import with_statement
from enthought.traits.api import Int, Instance, on_trait_change, Button, Bool
from infobiotics.pmodelchecker.pmodelchecker_params_handler import PModelCheckerParamsHandler
from mc2_params_group import mc2_params_group
from mc2_mcss_experiment import MC2McssExperiment
from infobiotics.commons.files import can_read_file
import tables
from mc2_preferences import MC2ParamsPreferencesPage

class MC2ParamsHandler(PModelCheckerParamsHandler):

    preferences_page = MC2ParamsPreferencesPage()

    def _params_group_default(self):
        return mc2_params_group
    
    id = 'MC2ParamsHandler'
    
    help_urls = [
        ('Tutorial', 'http://www.infobiotics.org/infobiotics-workbench/tutorial/modelCheckingMC2.html'),
        ('MC2 webpage', 'http://www.brc.dcs.gla.ac.uk/software/mc2/'),
    ]
    
    default_temporal_formula = 'P=?[ (Time=1000)U([molecule] >= T ^ [molecule] < T + constant)'
    
    _mc2_mcss_experiment = Instance(MC2McssExperiment)
    
    def object_mcss_params_file_changed(self, info):
        if can_read_file(self.model.mcss_params_file_):
            self._mc2_mcss_experiment = MC2McssExperiment(self.model.mcss_params_file_, _mc2_experiment=self.model)
    
    def __mc2_mcss_experiment_default(self):
        return MC2McssExperiment(_mc2_experiment=self.model)

    edit_mc2_mcss_experiment = Button(label='Edit')
    
    def _edit_mc2_mcss_experiment_fired(self):
        self._mc2_mcss_experiment.edit()
    
    @on_trait_change('model:simulations_file_hdf5, model:simulations_generatedHDF5')
    def update_number_of_runs_read(self, info):
        ''' Tries to extract 'number_of_runs' from 'simulations_file_hdf5'. '''
        self.number_of_runs_read = False
        if self.model.simulations_generatedHDF5 and can_read_file(self.model.simulations_file_hdf5_): # fail fast
            with tables.openFile(self.model.simulations_file_hdf5_, 'r') as f:
                try:
                    if not f.root._v_attrs.__contains__('mcss_version'):
                        raise ValueError('%s is not an mcss simulation' % self.model.simulations_file_hdf5_)
                    self.max_number_samples = int(f.root._v_attrs.number_of_runs)
                    if self.max_number_samples > 1:
                        self.number_of_runs_read = True
                except ValueError, e:
                    print e

    number_of_runs_read = Bool
    max_number_samples = Int(1) # used by RangeEditor in mc2_params_group
    number_samples_when_simulation_file_supplied = Int(desc='the number of simulations to use when approximation is applied')
    
    def _number_samples_when_simulation_file_supplied_changed(self):
        self.model.number_samples = self.number_samples_when_simulation_file_supplied

    
if __name__ == '__main__':
    execfile('mc2_params.py')
    
