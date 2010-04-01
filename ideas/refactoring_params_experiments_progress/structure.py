'''
Skeletal definitions of interfaces, abstract classes, classes and mixins used 
by Infobiotics programs.

Class names have the general form:
[IM][Specific]General[Context][Function][Handler]
I = Interface
M = Mixin
Specific ~ Mcss
General ~ Experiment
Context ~ Dashboard
Function ~ Progress
Handler = Handler
e.g. IMcssExperimentDashboardProgressHandler

'''
import enthought.traits.has_traits
enthought.traits.has_traits.CHECK_INTERFACES = 2

from enthought.traits.api import \
    HasTraits, Interface, implements, File, Directory, Bool, Str, List, \
    Callable, Property, property_depends_on, Range, Button, on_trait_change, \
    Instance
from enthought.traits.ui.api import \
    Controller, ModelView, View, Item, Action


load_action = Action(name='Load', action='load', 
    tooltip='Load parameters from a file'
) 

save_action = Action(name='Save', action='save', 
    tooltip='Save the current parameters to a file'
)

#load_save_actions = [load_action, save_action]
params_actions = [load_action, save_action]

perform_action = Action(name='Perform', action='perform', 
    tooltip='Perform the experiment with the current parameters',
    enabled_when='object.has_valid_parameters()', #XXX calls has_valid_parameters which each UI change
)

#load_save_perform_actions = [load_action, save_action, perform_action] 
experiment_actions = [load_action, save_action, perform_action] 



class ParamsView(View):
    
    buttons = ['Undo','Revert','OK', 'Cancel'] + params_actions
    resizable = True
    id = 'ParamsView'
    

class ExperimentView(ParamsView):

    buttons = ['Undo','Revert','OK', 'Cancel'] + experiment_actions
    id = 'ExperimentView'


class Percentage(Range):
    
    def __init__(self, value=None, **metadata):
        super(Percentage, self).__init__(low=1.0, high=100.0, exclude_low=False, exclude_high=False, **metadata)


class IParams(Interface):
    
    _parameters_name = Str(desc='the name attribute of the parameter tag in the params XML file')
    _parameter_set_name = Str(desc='the name attribute of the parameterSet tag in the params XML file')
    _params_file = File(exists=True)
    _cwd = Directory(exists=True)
    _dirty = Bool

    def load(self, file=None):
        ''' Load parameters from a file. '''
    
    def save(self, file=None):
        ''' Save parameters to a file. '''

    def parameter_names(self):
        ''' Returns the list of '''


class Params(HasTraits): 
    implements(IParams)
    
    _parameters_name = Str(desc='the name attribute of the parameter tag in the params XML file')
    _parameter_set_name = Str(desc='the name attribute of the parameterSet tag in the params XML file')
    _params_file = File(exists=True)
    _cwd = Directory(exists=True)
    _dirty = Bool
    
    def parameter_names(self): 
        raise NotImplementedError
    
    def load(self, file=None): 
        if file is None:
            raise ValueError
        pass
    
    def save(self, file=None): 
        if file is None:
            raise ValueError
        pass

class IParamsHandler(Interface):
    
    def load(self, info):
        ''' Load parameters from a file. '''
    
    def save(self, info):
        ''' Save parameters to a file. '''
        

class ParamsHandler(Controller):
    implements(IParamsHandler)
    
    def load(self, info): 
        file=None
        info.object.load(file)
    
    def save(self, info):
        file=None
        info.object.save(file)

    view = ParamsView(
        Item('_cwd', label='Working directory', tooltip='Relative paths will be relative to this directory.'),
    )


class IExperiment(IParams):
    _params_program = File(exists=True)
    
    def perform(self):
        ''' Perform the experiment. '''


class Experiment(Params):
    implements(IExperiment) 
    
    _params_program = File(exists=True)
    
    def perform(self): 
        pass

    _error_pattern_list = List(Str)
    
    def _pattern_matched(self, pattern_index, match): 
        pass


class McssExperiment(Experiment):
    
    _params_program = 'mcss'
    
    
class PModelCheckerExperiment(Experiment): 

    _params_program = 'pmodelchecker'
    _parameters_name = 'pmodelchecker'


class MC2Experiment(PModelCheckerExperiment):

    _parameter_set_name = 'mc2'
    model_checker = 'MC2'


class PRISMExperiment(PModelCheckerExperiment):
    
    _parameter_set_name = 'prism'
    model_checker = 'PRISM'


class POptimizerExperiment(Experiment):

    _params_program = 'poptimizer'
    _parameters_name = 'poptimizer'
    _parameter_set_name = 'poptimizer'


class IExperimentHandler(IParamsHandler):

    _progress_handler = Callable # a class inheriting from IExperimentProgressHandler
    
    def perform(self, info):
        ''' Perform the experiment. '''


class ExperimentHandler(ParamsHandler):
    implements(IExperimentHandler)
    
    _progress_handler = Callable # a class inheriting from IExperimentProgressHandler
    
    def perform(self, info):
        self._show_progress()
        info.object.perform()

    def _show_progress(self):
        self._progress_handler(model=self.model).edit_traits(kind='nonmodal')

    traits_view = ExperimentView(
        Item('_cwd', label='Working directory', tooltip='Relative paths will be relative to this directory.'),
    )


class IExperimentProgressHandler(Interface):
    
    progress = Property(Percentage) 
    status = Property(Str)

    def _get_progress(self):
        ''''''
    def _get_status(self):
        ''''''

class ExperimentProgressHandler(ModelView):
    implements(IExperimentProgressHandler)
    
    progress = Property(Percentage) 
    status = Property(Str)

    def _get_progress(self):
        raise NotImplementedError
    
    def _get_status(self):
        raise NotImplentedError
    
    params_experiment_progress_view = View(
        'model.title',
        'progress',
        'model.status',
    )


class McssExperimentProgressHandler(ExperimentProgressHandler):
    
    @property_depends_on('model.runs, model.max_time, time_in_run, run')
    def _get_progress(self):
        pass

    def _get_status(self):
        pass


class MC2ExperimentProgressHandler(ExperimentProgressHandler):

    @property_depends_on('pass')
    def _get_progress(self):
        pass

    def _get_status(self):
        pass


class PRISMExperimentProgressHandler(ExperimentProgressHandler):

    @property_depends_on('pass')
    def _get_progress(self):
        pass

    def _get_status(self):
        pass


class POptimizerExperimentProgressHandler(ExperimentProgressHandler):

    @property_depends_on('pass')
    def _get_progress(self):
        pass

    def _get_status(self):
        pass


class CancelProgressMixin(object):#Cancellation/Cancellable
    ''' Mixin '''
    cancel = Button
    
    @on_trait_change('cancel')
    def cancelled(self):
        pass

    
class McssExperimentDashboardProgressHandler(McssExperimentProgressHandler, CancelProgressMixin):
    pass


class MC2ExperimentDashboardProgressHandler(MC2ExperimentProgressHandler, CancelProgressMixin):
    pass


class PRISMExperimentDashboardProgressHandler(PRISMExperimentProgressHandler, CancelProgressMixin):
    pass


class POptimizerExperimentDashboardProgressHandler(POptimizerExperimentProgressHandler, CancelProgressMixin):
    pass

    
class McssExperimentHandler(ExperimentHandler):

    _progress_handler = McssExperimentProgressHandler


class McssExperimentDashboardHandler(McssExperimentHandler):

    _progress_handler = McssExperimentDashboardProgressHandler

    def _show_progress(self):
        pass
#        super(McssExperimentDashboardHandler, self)._show_progress()


class PModelCheckerExperimentHandler(ExperimentHandler):
    pass


class MC2ExperimentHandler(PModelCheckerExperimentHandler):

    _progress_handler = MC2ExperimentProgressHandler 


class MC2ExperimentDashboardHandler(MC2ExperimentHandler):

    _progress_handler = MC2ExperimentDashboardProgressHandler

    def _show_progress(self):
        pass


class PRISMExperimentHandler(PModelCheckerExperimentHandler):
    
    _progress_handler = PRISMExperimentProgressHandler


class PRISMExperimentDashboardHandler(PRISMExperimentHandler):

    _progress_handler = PRISMExperimentDashboardProgressHandler

    def _show_progress(self):
        pass


class POptimizerExperimentHandler(ExperimentHandler):
    
    _progress_handler = POptimizerExperimentProgressHandler
    

class POptimizerExperimentDashboardHandler(POptimizerExperimentHandler):

    _progress_handler = POptimizerExperimentDashboardProgressHandler

    def _show_progress(self):
        pass

    traits_view = ExperimentView(
#        Item('_cwd', label='Working directory', tooltip='Relative paths will be relative to this directory.'),
        Item('testing')
    )


if __name__ == '__main__':
#    mcss_experiment = McssExperiment()
#    McssExperimentHandler(model=mcss_params_experiment).configure_traits()
#    McssExperimentProgress(model=mcss_params_experiment).configure_traits()
    poptimizer_experiment = POptimizerExperiment()
    poptimizer_experiment_dashboard_handler = POptimizerExperimentDashboardHandler(model=poptimizer_experiment)
    poptimizer_experiment_dashboard_handler.configure_traits()
