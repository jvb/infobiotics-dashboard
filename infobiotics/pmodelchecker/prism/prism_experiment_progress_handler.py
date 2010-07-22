from infobiotics.common.api import ExperimentProgressHandler
from enthought.traits.api import on_trait_change

class PRISMExperimentProgressHandler(ExperimentProgressHandler):
    
#    max = 100 # defaults to zero
#    show_time = True

    def _message_default(self):
        if self.model.task == 'Approximate':
            return 'Approximating %s' % self.model.current_property
        elif self.model.task == 'Verify':
            return 'Verifying %s' % self.model.current_property
        elif self.model.task == 'Build':
            return 'Building PRISM model'
        elif self.model.task == 'Translate':
            return 'Translating PRISM model'
            
    #FIXME PRISM doesn't seem to send its output to stdout!    

#    @on_trait_change('model.current_property')
#    def update_message(self):
#        self.message = self._message_default()
#            
#    @on_trait_change('model.property_progress, model.max_properties, model.property_index')
#    def update_progress(self, name, old, new):
#        subtotal = self.model.property_progress + (100 * self.model.property_index)
#        total = 100 * self.model.max_properties
#        self.progress = int((subtotal / total) * 100)
    
        
if __name__ == '__main__':
    execfile('prism_experiment.py')
    