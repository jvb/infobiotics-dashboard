from infobiotics.shared.api import \
    ExperimentProgressHandler, Property, Range, property_depends_on

class McssProgressHandler(ExperimentProgressHandler):
    
    progress = Property(Range(0.0, 100.0, 0))
    
    @property_depends_on('model.time_in_run, model.runs, model.max_time')#model.run
    def _get_progress(self):
        percentage = float((((self.model.time_in_run) + ((self.model.run - 1) * self.model.max_time)) / (self.model.max_time * self.model.runs)) * 100) 
#        print '%s/%s %s/%s'%(self.model.time_in_run, self.model.max_time, self.model.run, self.model.runs), percentage
        return percentage

    def _get_status(self):
        return 'todo'
