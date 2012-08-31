from pyface.workbench.api import Perspective, PerspectiveItem
    
class ExperimentsPerspective(Perspective):
    id = 'infobiotics.dashboard.plugins.experiments.ui_plugin.ExperimentsPerspective'
    name = 'Experiments'
    show_editor_area = True 
    contents = [
        PerspectiveItem(
            id='infobiotics.dashboard.plugins.experiments.ui_plugin.ExperimentQueueView', 
            position='bottom',
        ),
    ]


from envisage.api import Plugin, ServiceOffer, ExtensionPoint
from traits.api import List
from experiment_queue import ExperimentQueue
from pyface.workbench.api import TraitsUIView

class ExperimentsUIPlugin(Plugin):

    # experiments queue for view
    service_offers = List(contributes_to='envisage.service_offers')
    def _service_offers_default(self):
        return [
            ServiceOffer(
                protocol='infobiotics.dashboard.plugins.experiments.experiment_queue.ExperimentQueue',
                factory=self._create_experiment_queue_service,
            ),
        ]
    def _create_experiment_queue_service(self):
        from experiment_queue import ExperimentQueue
        return ExperimentQueue()

#    experiments = ExtensionPoint(
#        List(Instance('infobiotics.dashboard.plugin.experiments.experiment.Experiment')),
##        List(Instance('infobiotics.dashboard.plugin.experiments.i_experiment.IExperiment')), #TODO
#        id='infobiotics.dashboard.plugins.experiments.ui_plugin.experiments',
#        desc='''
#        
#        This extension point allows you to contribute experiments to the 
#        'Experiments' UI plugin, to take advantage of progress monitoring, etc.
#        
#        '''
#    )

    # 'IPlugin' interface
    id = 'infobiotics.dashboard.plugins.experiments.experiments_ui_plugin' # The plugin's unique identifier
    name = 'Experiments' # The plugin's name (suitable for displaying to the user)

    # Contributions to extension points made by this plugin
    action_sets = List(contributes_to='envisage.ui.workbench.action_sets')
    def _action_sets_default(self):
        return []

    perspectives = List(contributes_to='envisage.ui.workbench.perspectives')
    def _perspectives_default(self):
        return [ExperimentsPerspective]

    views = List(contributes_to='envisage.ui.workbench.views')
    def _views_default(self):
        return [self._create_experiment_queue_view]
    def _create_experiment_queue_view(self, **traits):
        # from EnvisagePlugins/examples/workbench/Lorenz/acme/lorenz/lorenz_ui_plugin.py
        return TraitsUIView(
            obj=self.application.get_service('infobiotics.dashboard.plugins.experiments.experiment_queue.ExperimentQueue'),
            id='infobiotics.dashboard.plugins.experiments.ui_plugin.ExperimentQueueView',
            name='Experiment queue',
            category='Experiments',
            position='bottom',
            width=0.1,
            **traits
        )

    preferences_pages = List(contributes_to='envisage.ui.workbench.preferences_pages')
    def _preferences_pages_default(self):
        return []

    def start(self):
        pass    

    def stop(self):
        pass
