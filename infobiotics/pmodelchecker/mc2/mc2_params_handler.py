from infobiotics.common.api import ParamsView
from enthought.traits.api import (
    Int, Range, Property, Instance, on_trait_change, Button,
)
from infobiotics.pmodelchecker.api import (
    PModelCheckerParamsHandler, 
)
from mc2_params_group import mc2_params_group
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
    
    def init(self, info):
        super(MC2ParamsHandler, self).init(info)
        if info.initialized:
            self._update_mcss_experiment()
    
    _mcss_experiment = Instance('McssExperiment', ())
    
    @on_trait_change('_mcss_experiment, model.model_specification, model.number_samples, model.simulations_file_hdf5')
    def _update_mcss_experiment(self):
        self._mcss_experiment._cwd=self.model._cwd
        self._mcss_experiment.model_file = self.model.model_specification
        self._mcss_experiment.data_file = self.model.simulations_file_hdf5
        self._mcss_experiment.runs = self.model.number_samples
        # replace parameter_names function in _mcss_experiment with function that returns reduced list of parameter names
        def parameter_names():
            return [
                # set by MC2Experiment.TODO
                'model_file',
                # set by McssExperiment._model_file_changed()
                'model_format',
                # edited by user
                'duplicate_initial_amounts',
                'max_time',
                'log_interval',
                'compress',
                'compression_level',
                'simulation_algorithm',
                'seed',
                'periodic_x',
                'periodic_y',
                'periodic_z',
                'division_direction',
                'keep_divisions',
                'growth_type',
                'log_type',
                'log_propensities',
                'log_volumes',
                'log_steady_state',
                'log_degraded',
                # not edited by user
                'just_psystem',
            ]
        self._mcss_experiment.parameter_names = parameter_names

    def _mcss_params_file_changed(self, mcss_params_file):
        self._mcss_experiment = McssExperiment(mcss_params_file)

    edit_mcss_experiment = Button(label='Edit')
    
    def _edit_mcss_experiment_fired(self): #TODO
        from infobiotics.common.api import ParamsView
        view = ParamsView(
            mc2_mcss_experiment_group,
        )
        self._mcss_experiment.edit(view=view)


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
    