from progress_meter import ProgressMeter
from traits.api import Int

class NonInteractiveProgressMeter(ProgressMeter):

    progress_percentage = Int(0)

    def _progress_percentage_changed(self):
         if self.progress_percentage % 10 == 0:
             if not self.hidden:
                 print '%s: %s @ %s%% ' % (self.title, self.state, self.progress_percentage)

    def update(self, value):
        old_value = self.value
        super(NonInteractiveProgressMeter, self).update(value)
        new_value = self.value
        if new_value > old_value:
            self.progress_percentage = int(float(self.value) /  float((self.max - self.min) / float(100)))
    
    
if __name__ == '__main__':

    def start(self):
        return True

    progress_meter = NonInteractiveProgressMeter(
        min=0, max=50,
#        start_function=start,
        title='mcss',
        text='../xxx.params',        
    )
    progress_meter.start = True
    progress_meter.print_state()
    progress_meter.update(1)
    progress_meter.pause = True
    progress_meter.print_state()
    progress_meter.cancel = True
    progress_meter.print_state()
    progress_meter.retry = True
    progress_meter.print_state()
    
#    import time
#    for i in range(100):
#        time.sleep(0.02)
#        progress_meter.update(i)
    