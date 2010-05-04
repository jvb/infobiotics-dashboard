from infobiotics.mcss.api import McssExperiment, McssExperimentHandler
from infobiotics.pmodelchecker.mc2.api import MC2Params, mc2_mcss_experiment_group
from enthought.traits.api import Instance, DelegatesTo, Any, Str
from enthought.traits.ui.api import View, Group

class MC2McssExperimentHandler(McssExperimentHandler):
    
    traits_view = View(
        Group(
            mc2_mcss_experiment_group,
            show_border=True,
        ),
        buttons=['OK','Cancel'],
        resizable=True,
        id = 'MC2McssExperimentHandler'
    )

    def init(self, info):
        info.ui.title = self.title
        self.sync_trait('model_format_', info.object, alias='model_format', mutual=False) # doesn't sync mutually even if mutual=True, this just makes it explicit
        self.sync_trait('simulation_algorithm_', info.object, alias='simulation_algorithm', mutual=False) # ditto

class MC2McssExperiment(McssExperiment):
    
    _preferences_path = Str('pmodelchecker.mc2._mc2_mcss_experiment')
    
    def _handler_default(self):
        return MC2McssExperimentHandler(model=self)
    
    _mc2_experiment = Any#Instance(MC2Params) # otherwise when MC2Params(): TraitError: The '_mc2_experiment' trait of a MC2McssExperiment instance must be a MC2Params or None, but a value of MC2Params(model_specification='', model_checker='MC2', temporal_formulas='', number_samples=10000, results_file='', simulations_generatedHDF5=False, simulations_file_hdf5='', simulations_generatedMC2=False, simulations_file_MC2='', mcss_params_file='') <class '__main__.MC2Params'> was specified.
    
    _cwd = DelegatesTo('_mc2_experiment', prefix='_cwd', listenable=False)
    model_file = DelegatesTo('_mc2_experiment', prefix='model_specification')
    data_file = DelegatesTo('_mc2_experiment', prefix='simulations_file_hdf5')
    runs = DelegatesTo('_mc2_experiment', prefix='number_samples')

    def parameter_names(self): #TODO make parameter_names a Property(List)?
        return [
            'model_file',
            'model_format', # set by McssExperiment._model_file_changed()
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


if __name__ == '__main__':
#    MC2McssExperiment().configure()
    MC2Params().configure()
