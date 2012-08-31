from enthought.traits.api import Interface, Int, Range, Str 
#from enthought.traits.api import HasTraits, Enum, Bool, Button, Callable  

class IProgressMeter(Interface):
    ''' A progress meter that can be customised and subclassed for 
    non-interactive, interactive and within application uses.
    
    Implements the logic of start, pause, continue, cancel, retry and finished.
    
    From ProgressItem:
        A progress bar with customisable interactions.
        
        ...
    
        When min and max are both zero (the default) the progress percentage is not
        shown, instead the progress bar bounces back and forth. 
    
        ProgressItem can be customised and used in two ways, by direct 
        instantiation or by subclassing to override more fundamental aspects of the
        default behaviour.
    
        Instantiation:
            ProgressItem(
                title='title', 
                text='text', 
                min=0, 
                max=10, 
                start_condition='object.progress == object.min', 
                hide_function=lambda this: self.experiments.remove(this)
            )
    
        Subclassing:
            class ExperimentProgressItem(ProgressItem):
                title = 'title'
                text = 'text'
                def _cancel_function_default(self):
                    return ...
                    
    '''
    min = Int(0, desc='an integer specifying the minimum amount of progress (used to calculate the progress percentage).')
    max = Int(0, desc='an integer specifying the maximum amount of progress (used to calculate the progress percentage).')
    value = Range('min','max', desc='an integer between "min" and "max"  (used to calculate the progress percentage).')
    
    title = Str(desc='the title of the task.')
    text = Str(desc='textual information about the task, hidden if empty.')
#    state = Enum('started', 'paused', 'cancelled', 'finished')
#    
#    started = Bool(False)
#    paused = Bool(True) # starts paused
#    cancelled = Bool(False)
#    finished = Bool(False)
#        
#    hidden = Bool(False)
#
#    start = Button(desc='whether to start the task.')
#    pause = Button(desc='whether to pause the started task.')
#    continue_ = Button(desc='whether to continue the paused task.')
#    cancel = Button(desc='whether to cancel the started task.')
#    retry = Button(desc='whether to retry the cancelled task.')
#    hide = Button(desc='whether to hide updates to this progress meter.')
#
#    # eval'able strings that can be used directly by a TraitsUI Handler 
#    start_condition = Str('object.start_function is not None', desc='an expression that can be evaluated to enable the Start button')
#    pause_condition = Str('object.pause_function is not None and (object.min < object.value < object.max) and object.paused == False and object.cancelled == False', desc='an expression that can be evaluated to enable the Pause button')
#    continue_condition = Str('object.continue_function is not None and (object.min < object.value < object.max) and object.paused == True and object.cancelled == False', desc='an expression that can be evaluated to enable the Continue button')
#    cancel_condition = Str('object.cancel_function is not None and (object.min < object.value < object.max) and object.cancelled == False', desc='an expression that can be evaluated to enable the Cancel button')
#    retry_condition = Str('object.start_function is not None and object.cancelled == True', desc='an expression that can be evaluated to enable the Retry button')
#    hide_condition = Str('object.hide_function is not None and object.hidden == False', desc='an expression that can be evaluated to enable the Hide button')
#
#    # lambda self: True ensures paused, cancelled and hidden are set correctly
#    # when self._button_fired(True) and eval(button_condition, {'object':self})
#    # is True if functions have not been replaced. #TODO is that correct?
#    #TODO Do we want paused = True when pause = True and there is no pause_function?
#    start_function = Callable(lambda self: True, desc="a function called with this ProgressMeter instance when 'start' is True that must return True or False")
#    pause_function = Callable(lambda self: True, desc="a function called with this ProgressMeter instance when 'pause' is True that must return True or False")
#    continue_function = Callable(lambda self: True, desc="a function called with this ProgressMeter instance when 'continue' is True that must return True or False")
#    cancel_function = Callable(lambda self: True, desc="a function called with this ProgressMeter instance when 'cancel' is True that must return True or False")
#    retry_function = Callable(lambda self: True, desc="a function called with this ProgressMeter instance when 'retry' is True that must return True or False")
#    hide_function = Callable(lambda self: True, desc="a function called with this ProgressMeter instance when 'hide' is True that must return True or False")
#    finished_function = Callable(lambda self: True, desc="a function called with this ProgessMeter instance when 'progress' == 100%")
#    
#    def _start_fired(self, event):
#        ''' Calls self.start_function and sets self.paused to the result. '''
#        if event and eval(self.start_condition, {'object':self}):
#            self.update(self.min)
#            self.started = self.start_function(self)
#            print self.started
#            self.paused = not self.started
#                
#    def _pause_fired(self, event):
#        ''' Calls self.pause_function and sets self.paused to the result. '''
#        if event and eval(self.pause_condition, {'object':self}):
#            self.paused = self.pause_function(self)
#                
#    def _continue__fired(self, event):
#        ''' Calls self.continue_function and sets self.paused to the opposite 
#        of the result. '''
#        if event and eval(self.continue_condition, {'object':self}):
#            self.paused = not self.continue_function(self)
#                
#    def _cancel_fired(self, event):
#        ''' Calls self.cancel_function and sets self.cancelled to the result. 
#        '''
#        if event and eval(self.cancel_condition, {'object':self}):
#            self.cancelled = self.cancel_function(self)
#            self.started = False
#            self.paused = not self.started
#        
#    def _retry_fired(self, event):
#        ''' Calls self.retry_function and sets self.cancelled and self.finished
#        to True if it returns True. '''
#        if event and eval(self.retry_condition, {'object':self}):
#            if self.retry_function(self): 
#                self.cancelled = False
#                self.start = True # restart by calling start function again
#            
#    def _hide_fired(self, event):
#        ''' Calls self.hide_function and sets self.hidden to True if it returns
#        True. '''
#        if event and eval(self.hide_condition, {'object':self}):
#            if self.hide_function(self):
#                self.hidden = True
#    
#    def _finished_changed(self, finished):
#        ''' Calls self.finished_function if finished is True. '''
#        if finished and self.finished_function is not None:
#            self.finished_function(self)
    
    def update(self, value):
        ''' Set progress function. '''
