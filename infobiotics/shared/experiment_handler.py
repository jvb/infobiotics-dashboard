from infobiotics.shared.api import \
    Handler, Instance, \
    Experiment, ExperimentProgressHandler, \
    ExperimentView, Item, \
    Property, Str, property_depends_on

class ExperimentHandler(Handler):
#class ExperimentHandler(ParamsHandler):
    
    # Traits ---

    _progress_handler = Instance(ExperimentProgressHandler)

    experiment = Instance(Experiment)

    def _experiment_default(self):
        raise NotImplemetedError('Subclasses should override this method or'\
                                 "declare 'experiment = McssExperiment()'")

#    def _experiment_changed(self, experiment):
#        self.parameters = experiment.parameters
    
    
    # Handler-specific ---
    
    def trait_context(self):
        '''
        
        Adapted from Controller: https://svn.enthought.com/enthought/browser/Traits/trunk/enthought/traits/ui/handler.py
        
        '''
        context = super(ExperimentHandler, self).trait_context()
        context.update(
            {
                'experiment':self.experiment,
                'parameters': self.experiment.parameters,
                'handler': self,
                'object': self.experiment.parameters,
            }
        )
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


    title = Property(Str)

    @property_depends_on('experiment.parameters._params_file')
    def _get_title(self):
        path = self.experiment.parameters._params_file
        if len(path) > 0:
            dirname, basename = os.path.split(path)
            if dirname == '':
                return basename
            else:
                return '%s (%s)' % (basename, dirname)
        else:
            return self.experiment.parameters._parameters_name
            
    def init(self, info):
        info.ui.title = self.title 


#    # Class attributes --- 
#
#    traits_view = ExperimentView(
#        Item('_cwd', label='Working directory', tooltip='Relative paths will be relative to this directory.'),
#    )
    