'''
An experiment is 'performed', 
a process is started, 
the process is polled,
its output is displayed. 


'''

import subprocess
import sys
import os
os.environ['ETS_TOOLKIT']='qt4'
from enthought.traits.api import *
from enthought.traits.ui.api import *
from enthought.traits.ui.menu import *
from enthought.pyface.timer.timer import Timer


# Handles perform_action button click    
class ParamsExperimentHandler(Handler):
    
    perform_action = Action(name='Perform', action='perform')
    def perform(self, info):
        info.object.perform()

    traits_view = View(
        buttons=[perform_action],
        title='ParamsExperimentHandler',
    )

#TODO should each perform spawn a new process and progress meter?
    
# starts a process and creates a progress meter
class ParamsExperiment(HasTraits):

    def start(self):
#        args = ['less', 'view_output_fired.py']
#        args = ['./count_to_ten.py']
        args = ['python', './count_to_one_hundred.py']
        return subprocess.Popen(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        # raises OSError if not executable

    def perform(self):
        self.progress = ExperimentProgressItem(
            start_function=self.start,
        )
        result = self.progress.edit_traits(kind='nonmodal')
#        self.progress.start = True
        

#TODO use process.stdout as file instead of temporary file

#TODO exp1 == exp2 using parameter_names



class ExperimentProgressItem(HasTraits):
    process = Instance(subprocess.Popen)
    timer = Instance(Timer)
    start_function = Callable(lambda self: True)
    start = Button
    cancel = Button
    cancelled = Bool(False)
    view_output = Bool(True)
    stdout = Str
    stderr = Str
    
    lines_sizehint = Int(3)
    
    view = View(
        'lines_sizehint',
        Item('start', enabled_when='object.started == False'),
        HGroup('view_output'),
        VSplit(
            Item('stdout',
                editor=TextEditor(), 
                style='custom',
                show_label=False,
                visible_when='len(object.stdout)>0',
            ),
            Item('stderr',
                editor=TextEditor(), 
                style='custom',
                show_label=False,
                visible_when='len(object.stderr)>0',
            ),
            visible_when='object.view_output == True',
        ),
#        resizable=True,
#        scrollable=True,
        title='ExperimentProgressItem',
    )
    
    def _start_fired(self):
        try:
            self.process = self.start_function()
            self.timer = Timer(10, self._poll_process)
        except OSError, e:
            sys.stderr.write('%s\n' % e)

    def _poll_process(self):
        returncode = self.process.poll()
        if returncode is None:
            # process still running
            
            # check if user has cancelled
#            if self.progress_meter.cancelled: 
            if self.cancelled: 
                # ask process to terminate
                if sys.platform == 'win32':
                    self.process.terminate()
                else:
                    # mcss should exit gracefully on Linux with SIGINT
                    os.kill(self.process.pid, signal.SIGINT) # == self.process.send_signal(signal.SIGINT) 
                return
                    
#            # ask process to print the current simulation time and run number
#            if sys.platform != 'win32':
#                os.kill(self.process.pid, signal.SIGUSR1) #TEST
            
            # read last line on stdout within sizehint
            lines = self.process.stdout.readlines(self.lines_sizehint)
            # needs sizehint or we wait to get the whole buffer and progress bar doesn't work
            if lines is not None:
                if len(lines) > 0:    
                    self._process_lines(lines)
                else:
                    print 'len(lines) == 0'

#            # read last line on stdout within sizehint
#            lines = self.process.stdout.readlines(self.lines_sizehint)
#            # needs sizehint or we wait to get the whole buffer and progress bar doesn't work
#            if lines is not None:
#                if len(lines) > 0:    
#                    self._process_lines(lines)
#                else:
#                    print 'len(lines) == 0'

        else:
            # process has finished

            # auto-close progress_meter by updating its progress to max
#            self.progress_meter.update(self.max_time if self.runs == 1 else self.runs)
            
            # stop the polling timer
            self.timer.Stop()

#            logger.debug(returncode)

            if returncode != 0:
                print 'there was an error'
                # 2 for syntax
                # 1 for other

                lines = self.process.stderr.readlines()
                if lines is not None:
                    pass
#                    logger.error('perform(): mcss returned %s and %s' % (returncode, lines))
                    self.stderr = ''.join(lines)
                
                #TODO message box if using gui - might not need to check because progress dialog doesn't appear without configure_traits! - can this be guaranteed?

                if returncode == 1:
                    pass
                    
                if returncode == 127:
                    # missing shared library (on Linux only?)
                    print 'shared library error:', 'try "export LD_LIBRARY_PATH=/path/to/libecsb.so.0"'
            
            else:
                pass
                print 'finished successfully'
                #TODO messagebox inviting user to view results

  
    def _cancel_fired(self):
        self.cancelled = True
    
    def _process_lines(self, lines):
        try:
            pass
#            (current_time, current_run) = lines[-1].strip().split(' ')
#            # update progress after converting current_time from str output to int *via* float
#            value = int(float(current_time) if self.runs == 1 else int(float(current_run)))
#            self.progress_meter.update(value)
            
            self.stdout = ''.join(lines)
            
        except ValueError, e:
            pass
#            logger.error(e)
            print e

  
  
if __name__ == '__main__':
    experiment = ParamsExperiment()
    handler = ParamsExperimentHandler()
    handler.configure_traits(context={'object':experiment})