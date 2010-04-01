from infobiotics.shared.api import \
    Handler, Instance, \
    Experiment, ExperimentProgressHandler, \
    ExperimentView, Item

class ExperimentHandler(Handler):
#class ExperimentHandler(ParamsHandler):
    
    # Traits ---

    _progress_handler = Instance(ExperimentProgressHandler)

    experiment = Instance(Experiment)

    def _experiment_default(self):
        raise NotImplemetedError('Subclasses should override this method or'\
                                 "declare 'experiment = McssExperiment()'")

    def _experiment_changed(self, experiment):
        self.parameters = experiment.parameters
    
    
    # Handler-specific ---
    
    def traits_context(self):
        '''
        
        Adapted from Controller: https://svn.enthought.com/enthought/browser/Traits/trunk/enthought/traits/ui/handler.py
        
        '''
        context = super(ExperimentHandler, self).traits_context()
        context.update({'experiment':self.experiment, 'parameters': self.experiment.parameters})
#        context.update({'experiment':self._experiment}) # if ExperimentHandler(ParamsHandler)
        return context


    # Action methods ---
    
    def load(self, info): 
        file=None
        pass
        info.parameters.load(file)
    
    def save(self, info):
        file=None
        pass
        info.parameters.save(file)
    
    def perform(self, info):
        ''' Perform the experiment. '''
        info.experiment.perform(thread=True)
        self._show_progress()


    # self traits methods ---
    
    def _show_progress(self):
        progress_handler = self._progress_handler(model=self.model) # remove model in favour of context?
        progress_handler.edit_traits(kind='live') # must be live to receive progress updates


    # parameters traits methods ---

    def parameters_title_changed(self, info):
        info.ui.title = info.parameters.title


#    # Class attributes --- 
#
#    traits_view = ExperimentView(
#        Item('_cwd', label='Working directory', tooltip='Relative paths will be relative to this directory.'),
#    )
    