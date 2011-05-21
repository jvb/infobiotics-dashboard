from enthought.traits.api import ListStr, Str, Event, Property, Bool, on_trait_change
from infobiotics.commons.traits.percentage import Percentage
from infobiotics.core.params import Params
import sys 
import os
import tempfile
from enthought.pyface.timer.api import do_later

if sys.platform.startswith('win'):    
    # for py2exe frozen executables
    # ModuleFinder can't handle runtime changes to __path__, but win32com uses them
    import pywintypes
    import pythoncom
    import win32api
    try:
        import py2exe.mf as modulefinder # if this doesn't work, try import modulefinder
        import win32com
        for p in win32com.__path__[1:]:
            modulefinder.AddPackagePath("win32com", p)
        for extra in ["win32com.shell"]: #,"win32com.mapi"
            __import__(extra)
            m = sys.modules[extra]
            for p in m.__path__[1:]:
                modulefinder.AddPackagePath(extra, p)
    except ImportError:
        pass # no build path setup, no worries.

    import winpexpect
#    import wexpect # deprecated
import pexpect # provided by pexpect or winpexpect PyPI packages
from progressbar import ProgressBar, Percentage as Percent, Bar, RotatingMarker, ETA
    
from infobiotics.commons.api import logging
log = logging.getLogger(name='Experiment', level=logging.ERROR, format="%(message)s [%(levelname)s]")

class Experiment(Params):
#    ''' Abstract base class of all Infobiotics Dashboard experiments.
#    
#    ParamsExperiments are performed by external programs with parameters from
#    files with the extension '.params' (hence forth called 'params files'). 
#    Params files are XML in nature with 'parameters', 'parameterSet' 
#    and 'parameter' elements. Only one 'parameters' element is present and 
#    its name attribute is supposed to correlate to the program that parsers the
#    file. Generally only one 'parameterSet' element is present in each params 
#    file and its name attribute is supposed to correlate to a type of 
#    experiment that the program performs. For example in a PModelChecker 
#    experiment <parameters name="pmodelchecker"> and 
#    <parameterSet name="PRISM"> or <parameterSet name="MC2">. Each 'parameter'
#    element has 'name' and 'value' attributes that are used by the experiment
#    performing program to parameterise and perform an experiment.    
#
#    ParamsExperiment implements usable load(), save() and reset() methods from 
#    the IParamsExperiment interface. has_valid_parameters() and 
#    parameter_names() are left to subclasses to implement: in ParamsExperiment 
#    they each raise a NotImplementedError when called, as does perform() from 
#    the Experiment superclass.    
#    
#    '''
    executable_kwargs = ListStr

    def perform(self, thread=False):
        ''' Spawns an expect process and handles it in a separate thread. '''
        # save to temporary file in the same directory
        kwargs = dict(
            prefix=self._params_file.split('.params')[0],
            suffix='.params',
            dir=self.directory,
        ) 
        if sys.platform.startswith('win'): 
#            print os.path.splitunc(self._params_file_) #TODO use for paths
            kwargs.update(delete=False)
#        '''
#        tempfile.NamedTemporaryFile([mode='w+b'[, bufsize=-1[, suffix=''[, prefix='tmp'[, dir=None[, delete=True]]]]]])
#            This function operates exactly as TemporaryFile() does, except that the 
#            file is guaranteed to have a visible name in the file system (on Unix, the
#            directory entry is not unlinked). That name can be retrieved from the name 
#            member of the file object. Whether the name can be used to open the file a 
#            second time, while the named temporary file is still open, varies across 
#            platforms (it can be so used on Unix; it cannot on Windows NT or later). 
#            If delete is true (the default), the file is deleted as soon as it is 
#            closed.        
#        '''
        self.temp_params_file = tempfile.NamedTemporaryFile(**kwargs) # must be an instance variable (self...) otherwise it will not be usable by self._perform and will be deleted at the end of the method
        if sys.platform.startswith('win'): 
            self.temp_params_file.close() # see comment http://bit.ly/gUSEh0
        self.save(self.temp_params_file.name, force=True, update_object=False)

        # catch SIGINT signals (Ctrl-C)
        if self._interaction_mode in ('terminal', 'script'):
            def terminate(signum, frame):
                '''Signal handler that terminates child processes elegantly.'''
                if self._child.isalive():
                    self._child.terminate(force=True)
            import signal
            signal.signal(signal.SIGINT, terminate)   
        
        # actually perform the experiment
        if not thread or self._interaction_mode in ('terminal', 'script'):
            self._perform()
        else:
            do_later(self._perform) # run in thread

        # restore default SIGINT handler that raises KeyboardInterrupt 
        if self._interaction_mode in ('terminal', 'script'):
            signal.signal(signal.SIGINT, signal.default_int_handler)


    def _perform(self):
        ''' Start the program and try to match output.
        
        Spawns the program (starting it in self.cwd),
        compiles list of patterns for expect_list,
        adds EOF to list,
        calls 'started' hook,
        loops calling the '_output_pattern_matched' hook with the index of the pattern
        and the match until EOF whereupon it calls the 'finished' hook.
         
        **Might be running in thread.**
         
        '''
        self.success = False
        if sys.platform.startswith('win'):
            self._child = winpexpect.winspawn(self.executable, [self.temp_params_file.name] + self.executable_kwargs[:], cwd=self.directory)
        else:
            self._child = pexpect.spawn(self.executable, [self.temp_params_file.name] + self.executable_kwargs[:], cwd=self.directory)
        # note that spawn doesn't like list traits so we copy them using [:] 
        # and directory is defined in Params
        
        stdout_pattern_range = range(0, len(self._stdout_pattern_list))
        
        stderr_pattern_range = range(len(self._stdout_pattern_list), len(self._stdout_pattern_list) + len(self._stderr_pattern_list))
        
        # compile pattern list for expect_list
        compiled_pattern_list = self._child.compile_pattern_list(self._stdout_pattern_list + self._stderr_pattern_list)
        
        # append EOF to compiled pattern list        
        compiled_pattern_list.append(pexpect.EOF)
        eof_index = compiled_pattern_list.index(pexpect.EOF)
        
        # append TIMEOUT to compiled pattern list
        compiled_pattern_list.append(pexpect.TIMEOUT)
        timeout_index = compiled_pattern_list.index(pexpect.TIMEOUT)        
        
        self._starting()
        self.running = True

        import re, os

        # expect loop
#        patterns_matched = 0
        stdout_patterns_matched = 0
        stderr_patterns_matched = 0
        
        self._error_string = ''
        
        while True:
            pattern_index = self._child.expect_list(
                compiled_pattern_list,
                searchwindowsize=2000, # at least 2000 is required to catch some pmodelchecker output
                timeout=60,
            )
            if pattern_index == eof_index:
                if stdout_patterns_matched + stderr_patterns_matched == 0:
                    if self._child.before != '':
#                        self._error_string = self._child.before
                        # scour before for error messages
                        for line in self._child.before.split(os.linesep):
                            for i, pattern in enumerate(self._stderr_pattern_list):
                                if re.match(pattern, line) is not None:
                                    self._stderr_pattern_matched(len(self._stdout_pattern_list) + i, line)
                                    break # out of inner for loop
                            else:
                                continue # don't break out of outer loop yet
#                            for i, pattern in enumerate(self._stdout_pattern_list):
#                                if re.match(pattern, line) is not None:
#                                    self._stdout_pattern_matched(i, line)
#                                    break # out of inner for loop
#                            else:
#                                continue # don't break out of outer loop yet
                            break # out of outer for loop
                        else:
#                            self._stdout_pattern_matched(-1, self._child.before)
                            print '-1', self._child.before
                    else:
#                        self.finished_without_output = True #TODO
#                        print 'finished without output'
                        pass
                    break # out of while loop
                break
                # process has finished, perhaps prematurely, but can't tell so call it a success
            elif pattern_index == timeout_index:
#                self.timed_out = True #TODO
                print 'timed out'
                break
            elif pattern_index in stdout_pattern_range:
                match = self._child.match.group()
                self._stdout_pattern_matched(pattern_index, match)
#                do_later(self._stdout_pattern_matched, pattern_index, match)
                stdout_patterns_matched += 1
            elif pattern_index in stderr_pattern_range:
                match = self._child.match.group()
                self._stderr_pattern_matched(pattern_index - len(self._stdout_pattern_list), match)
#                do_later(self._stderr_pattern_matched, pattern_index - len(self._stdout_pattern_list), match)
                stderr_patterns_matched += 1

        # gather information before finishing
                
        self._finished_without_output = True if stdout_patterns_matched + stderr_patterns_matched == 0 else False
            
        self._child.close() # close file descriptors and store exitstatus and signalstatus
#        if self._child.exitstatus is not None:
#            print 'exitstatus == %s' % self._child.exitstatus
#        if self._child.signalstatus is not None:
#            print 'signalstatus == %s' % self._child.signalstatus
#        print 'status == %s' % self._child.status

#        if self._child.exitstatus == 0: # returncode is set by communicate() 
#            self.finished_successfully = True # trigger ExperimentHandler.show_results()
#        else:
#            error_log = open(self.error_log_file_name, 'w')
#            if self._child.exitstatus == 1:
#                # get last non-empty line of stdout or None
#                if len(stderr_output) > 0:#stderr_output != '':
#                    stdout_output_error = stdout_output.strip()#last_non_empty_line(stdout_output.split(os.linesep))
#                    stderr_output_error = stderr_output.strip()#last_non_empty_line(stderr_output.split(os.linesep))
#                    if stdout_output_error is not None:
#                        if stderr_output_error is not None:
#                            error = os.linesep.join((stdout_output_error, stderr_output_error))
#                        else:
#                            error = stdout_output_error
#                    else:
#                        if stderr_output_error is not None:
#                            error = stderr_output_error
#                        else:
#                            error = '%s exited with return code %s' % (arg_string, self._child.exitstatus)
#            elif self._child.exitstatus == -2:
#                error = '%s was cancelled by the user before data could be written.' % arg_string
#            elif self._child.exitstatus == -9:
#                error = '%s was terminated by the user.' % arg_string
#            elif self._child.exitstatus == -11:
#                error = '%s caused a segmentation fault and was terminated by the operating system.' % arg_string
#            elif self._child.exitstatus == -15:
#                error = '%s was terminated by the dashboard.' % arg_string
#            elif self._child.exitstatus == 127:
#                error = 'shared library error'
#            else:
#                error = '%s exited with returncode %s' % (arg_string, self._child.exitstatus)
##            self.log.error(error)
#            error_log.write(error)
#            error_log.close()

        error = ''
        if self._child.exitstatus is None:
            # exited with a signal
            error = '%s exited with signal: %s' % (self.executable_name, self._child.signalstatus)
        elif self._child.exitstatus != 0:
            error = '%s exited with exit code: %s' % (self.executable_name, self._child.exitstatus)
            error += self._child.before
        if error != '':
            if self._interaction_mode == 'script':
                log.error(error)
            elif self._interaction_mode == 'terminal':
                print error
            elif self._interaction_mode == 'gui':
                self._handler.status = self._child.before + match #TODO 
            
        self.success = True if self._child.exitstatus == 0 else False
        self.finished = True # setting an Event trait like 'finished' triggers change handlers in the main thread


    success = Bool

    finished = Event
    
    def _finished_changed(self):
        '''Sets self.running to False in the main thread'''
        self.running = False
        if self._interaction_mode in ('script', 'terminal'):
            if self.success and not self._finished_without_output:
                self._progress_bar.finish()
            if getattr(self, '_progress_bar_started', False): #FIXME AttributeError: 'McssExperiment' object has no attribute '_progress_bar_started'
                print
        elif self._interaction_mode == 'gui':
            self._handler._finished(self.success)
        
        del self.temp_params_file # deletes file except on Windows because we set delete=False for other reasons, see perform
        if sys.platform.startswith('win'):
            os.remove(self.temp_params_file.name) # deletes file on Windows
        
        self._reset_progress_traits()

    def _reset_progress_traits(self):
        self._progress_percentage = 0

    def cancel(self):
        self._child.terminate()



    _stdout_pattern_list = ListStr
    _stderr_pattern_list = ListStr([
        '^[eE]rror:.*', # mcss 'error: unknown parameter how_progress'
        '^[eE]rror[^:].+\nline [0-9]+: \([0-9]+ \[Error\]\) .*', # Fran & LibSBML 'error reading sbml input file\nline 1: (00002 [Error]) File unreadable.' 
        '^[eE]rror[^:].*', # Fran 'error ...'
        '^.+: command not found', # bash
        '^I/O warning : failed to load external entity ".+"', # libxml++
    ])
    
    def _stdout_pattern_matched(self, pattern_index, match):
        raise ValueError('Experiment._stdout_pattern_matched called with unrecognised pattern_index %s' % pattern_index)

    _error_string = Str(desc='the error the executable exited with')
            
    def _stderr_pattern_matched(self, pattern_index, match):
        self._error_string = match.strip()
        if self._interaction_mode == 'terminal':
            print self._error_string
        elif self._interaction_mode == 'script':
            log.error(self._error_string)
        elif self._interaction_mode == 'gui':
            log.error(self._error_string)

    def _starting(self):
#        print 'starting in %s' % self._interaction_mode
        self._progress_percentage = 0
        if self._interaction_mode not in ('script', 'terminal'):
            self._handler._starting()
        else:
            self._progress_bar = ProgressBar(
                widgets=[
                    self.executable_name, #' '.join((self.executable_name, os.path.split(self._params_file)[1])),
                    ' ',
                    Percent(),
                    ' ',
                    Bar(), #marker=RotatingMarker()),
                    ' ',
                    ETA()
                ],
                maxval=100,
            )
            self._progress_bar_started = False


    _progress_percentage = Percentage
    
    @on_trait_change('_progress_percentage')    
    def _update_progress_bar(self):
#    def __progress_percentage_changed(self, value): # doesn't work, maybe because of double underscore ...
        if self._interaction_mode in ('script', 'terminal'):
            if not self._progress_bar_started and self._progress_percentage > 0:
                self._progress_bar_started = True
                self._progress_bar.start()
            self._progress_bar.update(self._progress_percentage)
#        else:
#            self._handler.update_progress_dialog(self._progress_percentage)
        # done automatically
            
#from enthought.traits.ui.api import Group, Item
#
#error_string_group = Group(
#    Item('error_string',
#        show_label=False,
#        style='readonly',
#        emphasized=True,
#    ),
##    visible_when='len(object.error_string) > 0',
#    enabled_when='len(object.error_string) > 0',
#    label='Error(s)',
#)


def test():
#    from infobiotics.mcss.mcss_experiment import McssExperiment
#    McssExperiment().configure()
    from infobiotics.pmodelchecker.prism.prism_experiment import PRISMExperiment
    PRISMExperiment().configure()
     
if __name__ == '__main__':
    test()
