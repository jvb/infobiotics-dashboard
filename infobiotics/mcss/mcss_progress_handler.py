from infobiotics.shared.api import \
    ExperimentProgressHandler, Property, percentage, property_depends_on

class McssProgressHandler(ExperimentProgressHandler):
    
    progress = Property(percentage)
    
    @property_depends_on('model.time_in_run, model.runs, model.max_time')#model.run
    def _get_progress(self):
        percent = float((((self.model.time_in_run) + ((self.model.run - 1) * self.model.max_time)) / (self.model.max_time * self.model.runs)) * 100) 
        return percent

    def _get_status(self):
        return 'todo'
