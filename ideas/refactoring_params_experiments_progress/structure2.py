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




# Imports ---


import os.path

from enthought.traits.api import \
    HasTraits, Interface, implements, File, Directory, Bool, Str, List, \
    Callable, Property, property_depends_on, Range, Button, on_trait_change, \
    Instance
    
from enthought.traits.ui.api import \
    Controller, ModelView, View, Item, Action, RangeEditor




# Traits ---

#class Percentage(Range):
#    
#    def __init__(self, value=None, **metadata):
#        super(Percentage, self).__init__(low=1.0, high=100.0, exclude_low=False, exclude_high=False, **metadata)




# Actions --- #TODO move into Params/Experiment

load_action = Action(name='Load', action='load', 
    tooltip='Load parameters from a file'
) 

save_action = Action(name='Save', action='save', 
    tooltip='Save the current parameters to a file'
)

params_actions = [load_action, save_action]

perform_action = Action(name='Perform', action='perform', 
    tooltip='Perform the experiment with the current parameters',
    enabled_when='object.has_valid_parameters()', #XXX calls has_valid_parameters which each UI change
)

experiment_actions = [load_action, save_action, perform_action] 

shared_actions = ['Undo','Revert','OK', 'Cancel']




# Views ---


class ParamsView(View): # can be used to edit parameters without performing the experiment (why would you want to do that?)
    
    buttons = shared_actions + params_actions
    resizable = True
    id = 'ParamsView'
    

class ExperimentView(ParamsView):

    buttons = shared_actions + experiment_actions
    id = 'ExperimentView'




# Mixins ---


class CancelExperimentMixin(object):
    ''' Mixin '''
    cancel = Button
    
    @on_trait_change('cancel')
    def cancelled(self):
        pass



# Params ---


class Params(HasTraits): 
    
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

#    def __init__(self, file=None, *args, **traits):
#        super(Params, self).__init__(*args, **traits)
#        self.load(file)

    title = Property(Str)
    
    @property_depends_on('_params_file')
    def _get_title(self):
        if len(self._params_file) > 0:
            path = self._params_file
        else:
            path = self._params_program
        dirname, basename = os.path.split(path)
        if dirname == '':
            return basename
        else:
            return '%s (%s)' % (basename, dirname)


class ParamsHandler(Controller):
    
    def load(self, info): 
        file=None
        info.object.load(file)
    
    def save(self, info):
        file=None
        info.object.save(file)

    traits_view = ParamsView(
        Item('_cwd', label='Working directory', tooltip='Relative paths will be relative to this directory.'),
    )

    def object_title_changed(self, info):
        info.ui.title = info.object.title


# Experiment ---


class Experiment(Params):
    
    _params_program = File(exists=True)
    
    def perform(self): 
        pass
        print self.__class__.__name__, 'perform'

    _error_pattern_list = List(Str)
    
    def _pattern_matched(self, pattern_index, match): 
        pass

#    def __init__(self, file=None, *args, **traits):
#        super(Experiment, self).__init__(file, *args, **traits)
    

class ExperimentHandler(ParamsHandler):
    
    _progress_handler = Callable # a class inheriting from IExperimentProgressHandler
    
    def perform(self, info):
        ''' Perform the experiment. '''
        self._show_progress()
        info.object.perform()

    def _show_progress(self):
        self._progress_handler(model=self.model).edit_traits(kind='nonmodal')

    traits_view = ExperimentView(
        Item('_cwd', label='Working directory', tooltip='Relative paths will be relative to this directory.'),
    )


class ExperimentProgressHandler(ModelView): # --> Mixin?
    
#    progress = Property(Percentage) 
#    progress = Property(Range(0.0, 100.0))
    progress = Range(0.0, 100.0)
    status = Property(Str)

    def _get_progress(self):
        raise NotImplementedError
    
    def _get_status(self):
        raise NotImplentedError
    
    traits_view = View(
        'model.title',
        'progress',
        'status',
    )




# mcss ---


class McssExperiment(Experiment):
    
    _params_program = 'mcss'


class McssExperimentProgressHandler(ExperimentProgressHandler):
    
    @property_depends_on('model.runs, model.max_time, time_in_run, run')
    def _get_progress(self):
        return 100.0

    def _get_status(self):
        return ''


class McssExperimentHandler(ExperimentHandler):

    _progress_handler = McssExperimentProgressHandler

    traits_view = ExperimentView(
        Item('_cwd', label='Working directory', tooltip='Relative paths will be relative to this directory.'),
    )
    

class McssExperimentDashboardProgressHandler(McssExperimentProgressHandler, CancelExperimentMixin):
    pass
    

class McssExperimentDashboardHandler(McssExperimentHandler):

    _progress_handler = McssExperimentDashboardProgressHandler

    def _show_progress(self):
        pass
#        super(McssExperimentDashboardHandler, self)._show_progress()




# pmodelchecker ---
    
    
class PModelCheckerExperiment(Experiment): 

    _params_program = 'pmodelchecker'
    _parameters_name = 'pmodelchecker'


class PModelCheckerExperimentHandler(ExperimentHandler):
    pass



# MC2 --


class MC2Experiment(PModelCheckerExperiment):

    _parameter_set_name = 'mc2'
    model_checker = 'MC2'

    
class MC2ExperimentProgressHandler(ExperimentProgressHandler):

    @property_depends_on('pass')
    def _get_progress(self):
        pass

    def _get_status(self):
        pass


class MC2ExperimentHandler(PModelCheckerExperimentHandler):

    _progress_handler = MC2ExperimentProgressHandler 

    traits_view = ExperimentView(
        Item('_cwd', label='Working directory', tooltip='Relative paths will be relative to this directory.'),
    )


class MC2ExperimentDashboardProgressHandler(MC2ExperimentProgressHandler, CancelExperimentMixin):
    pass


class MC2ExperimentDashboardHandler(MC2ExperimentHandler):

    _progress_handler = MC2ExperimentDashboardProgressHandler

    def _show_progress(self):
        pass



# PRISM --


class PRISMExperiment(PModelCheckerExperiment):
    
    _parameter_set_name = 'prism'
    model_checker = 'PRISM'


class PRISMExperimentProgressHandler(ExperimentProgressHandler):

    @property_depends_on('pass')
    def _get_progress(self):
        pass

    def _get_status(self):
        pass


class PRISMExperimentHandler(PModelCheckerExperimentHandler):
    
    _progress_handler = PRISMExperimentProgressHandler

    traits_view = ExperimentView(
        Item('_cwd', label='Working directory', tooltip='Relative paths will be relative to this directory.'),
    )
    

class PRISMExperimentDashboardProgressHandler(PRISMExperimentProgressHandler, CancelExperimentMixin):
    pass
    
    
class PRISMExperimentDashboardHandler(PRISMExperimentHandler):

    _progress_handler = PRISMExperimentDashboardProgressHandler

    def _show_progress(self):
        pass




# poptimizer ---


class POptimizerExperiment(Experiment):

    _params_program = 'poptimizer'
    _parameters_name = 'poptimizer'
    _parameter_set_name = 'poptimizer'
    
    
class POptimizerExperimentProgressHandler(ExperimentProgressHandler):

    @property_depends_on('pass')
    def _get_progress(self):
        pass

    def _get_status(self):
        pass


class POptimizerExperimentHandler(ExperimentHandler):
    
    _progress_handler = POptimizerExperimentProgressHandler
    
    traits_view = ExperimentView(
        Item('_cwd', label='Working directory', tooltip='Relative paths will be relative to this directory.'),
        Item(label='testing override traits_view'),
    )


class POptimizerExperimentDashboardProgressHandler(POptimizerExperimentProgressHandler, CancelExperimentMixin):
    pass


class POptimizerExperimentDashboardHandler(POptimizerExperimentHandler):

    _progress_handler = POptimizerExperimentDashboardProgressHandler

    def _show_progress(self):
        print 'got here'




def mcss(*args, **traits):
    if len(args) < 1 or args[0] is None:
        raise ValueError
    if isinstance(args[0], str):
        file = args[0]
        mcss_experiment = McssExperiment(file)
#    mcss_experiment_handler = McssExperimentHandler(model=mcss_experiment)
#    mcss_experiment_handler.configure_traits()
    mcss_experiment.perform()




if __name__ == '__main__':

#    mcss_experiment = McssExperiment()
#    mcss_experiment.configure_traits()
#    mcss_experiment_handler = McssExperimentHandler(model=mcss_experiment)
#    mcss_experiment_handler = McssExperimentProgressHandler(model=mcss_experiment).configure_traits()
#    mcss_experiment_handler = McssExperimentDashboardProgressHandler(model=mcss_experiment)
#    mcss_experiment_handler._show_progress()
#    mcss_experiment_handler.configure_traits()
#    mcss('abc')


    pmodelchecker_experiment = PModelCheckerExperiment()
#    pmodelchecker_experiment.configure_traits()
    pmodelchecker_experiment_handler = PModelCheckerExperimentHandler(model=pmodelchecker_experiment)
#    pmodelchecker_experiment_handler = PModelCheckerExperimentProgressHandler(model=pmodelchecker_experiment).configure_traits()
#    pmodelchecker_experiment_handler = PModelCheckerExperimentDashboardProgressHandler(model=pmodelchecker_experiment)
#    pmodelchecker_experiment_handler._show_progress()
    pmodelchecker_experiment_handler.configure_traits()
#    pmodelchecker('abc')


#    poptimizer_experiment = POptimizerExperiment()

#    poptimizer_experiment.configure_traits()
#    poptimizer_experiment.configure_traits(view=ParamsView())
#    poptimizer_experiment.configure_traits(view=ExperimentView())

#    poptimizer_experiment_handler = POptimizerExperimentHandler(model=poptimizer_experiment)
#    poptimizer_experiment_handler._show_progress()
#    poptimizer_experiment_handler.configure_traits()

#    poptimizer_experiment_handler = POptimizerExperimentDashboardHandler(model=poptimizer_experiment)
#    poptimizer_experiment_handler._show_progress() # prints 'got here'
#    poptimizer_experiment_handler.configure_traits()
