from __future__ import with_statement
from infobiotics.common.api import ParamsView
from enthought.traits.api import (
    Int, Range, Property, Instance, on_trait_change, Button,
)
from infobiotics.pmodelchecker.api import (
    PModelCheckerParamsHandler, 
)
#from infobiotics.pmodelchecker.mc2.api import MC2Params
from mc2_params_group import mc2_params_group
from mc2_mcss_experiment import MC2McssExperiment
from mc2_mcss_experiment_group import mc2_mcss_experiment_group
from infobiotics.mcss.api import McssExperiment
from commons.api import can_read, can_write
import tables

class MC2ParamsHandler(PModelCheckerParamsHandler):

    def _params_group_default(self):
        return mc2_params_group
    
    id = 'MC2ParamsHandler'
    
    help_urls = [
        ('MC2 webpage','http://www.brc.dcs.gla.ac.uk/software/mc2/'),
    ]
    
    _mc2_mcss_experiment = Instance(MC2McssExperiment)
    
    def __mc2_mcss_experiment_default(self):
        return MC2McssExperiment(_mc2_experiment=self.model)

    edit_mc2_mcss_experiment = Button(label='Edit')
    
    def _edit_mc2_mcss_experiment_fired(self):
        self._mc2_mcss_experiment.handler.edit_traits()
    
    def object_simulations_file_hdf5_changed(self, info):
        ''' Tries to extract 'number_of_runs' from 'simulations_file_hdf5'. '''
        if can_read(self.model.simulations_file_hdf5) and self.simulations_generatedHDF5:
            with tables.openFile(self.simulations_file_hdf5, 'r') as f:
                if not f.root._v_attrs.__contains__('mcss_version'):
                    raise ValueError('%s is not an mcss simulation' % self.model.simulations_file_hdf5)
                self.number_of_runs = int(f.root._v_attrs.number_of_runs)
                
                #TODO use to make number_of_samples a range from 1 to 'number_of_runs'
    
    _number_of_runs = Int(1)
    _max_number_samples = Property(depends_on='_number_of_runs')
    _min_number_samples = Int(1)
    _number_samples_for_mc2_when_simulation_file_supplied = Range('_min_number_samples', '_max_number_samples', desc='the number of simulations to use when approximation is applied')
    #TODO show/hide number_samples in favour of _number_samples_for_mc2_when_simulation_file_supplied in mc2_group
    
    def _get__max_number_samples(self):
        return self._number_of_runs

    
if __name__ == '__main__':
    execfile('mc2_params.py')
    