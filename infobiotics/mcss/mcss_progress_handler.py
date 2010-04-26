from infobiotics.shared.api import (
    ExperimentProgressHandler, Property, percentage, property_depends_on,
    ProgressEditor, View, Item
)

class McssProgressHandler(ExperimentProgressHandler):
    
    progress = Property(percentage)
    
    @property_depends_on('model.time_in_run, model.runs, model.max_time')#model.run
    def _get_progress(self):
        percent = int((((self.model.time_in_run) + ((self.model.run - 1) * self.model.max_time)) / (self.model.max_time * self.model.runs)) * 100) 
        return percent

    def _get_status(self):
        return 'todo'

    traits_view = View(
        Item('progress', 
            editor=ProgressEditor(
                title='title',
                min=0,
                max=100,
                message='message',
                can_cancel=True,
            #    can_ok=False,
                show_time=True,
                show_percent=True,
            ),
        ),
    )