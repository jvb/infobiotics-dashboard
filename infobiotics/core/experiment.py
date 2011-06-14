from enthought.traits.api import ListStr, Str, Event, Property, Bool, on_trait_change, Instance
from infobiotics.commons.traits.percentage import Percentage
from infobiotics.core.params import Params
import sys 
import os
import tempfile
import re
from enthought.pyface.timer.api import do_later
from PyQt4.QtCore import QThread
from PyQt4.QtGui import QWidget
from enthought.pyface.api import error as error, GUI

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
logger = logging.getLogger(name=__name__, format="%(message)s [%(levelname)s]")

class Experiment(Params):
    ''' Abstract base class of all Infobiotics Dashboard experiments.
    
    Experiments are performed by external programs with parameters from
    files with the extension '.params' (hence forth called 'params files'). 
    Params files are XML in nature with 'parameters', 'parameterSet' 
    and 'parameter' elements. Only one 'parameters' element is present and 
    its name attribute is supposed to correlate to the program that parsers the
    file. Generally only one 'parameterSet' element is present in each params 
    file and its name attribute is supposed to correlate to a type of 
    experiment that the program performs. For example in a PModelChecker 
    experiment <parameters name="pmodelchecker"> and 
    <parameterSet name="PRISM"> or <parameterSet name="MC2">. Each 'parameter'
    element has 'name' and 'value' attributes that are used by the experiment
    performing program to parameterise and perform an experiment.
    
    ...    
    '''
    executable_kwargs = ListStr

    def perform(self, thread=False, expecting_no_output=False):
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
        if not thread:# or self._interaction_mode in ('terminal', 'script'):
            self._perform(expecting_no_output)
        else:
            class Thread(QThread):
                def __init__(self, experiment):
                    QThread.__init__(self)
                    self.experiment = experiment
                def run(self):
                    print self.isRunning()
                    print 'self.currentThreadId', int(self.currentThreadId())
                    print 'perform'
                    self.experiment._perform()
                    print self.isFinished()
#                    print 'self.exec_'
#                    self.exec_() # vital
                    print 'quit'
                    self.quit()
            self._thread = Thread(self)
            if True:#self._interaction_mode in ('terminal', 'script'):
                print 'start'
                self._thread.start() # not gui
                print 'QThread.currentThreadId', int(QThread.currentThreadId())
                print '_thread.exec_'
                self._thread.exec_()
            else:
                print 'do_later'
                do_later(self._thread.start) # vital
#                do_later(QThread.yieldCurrentThread) # vital

        # restore default SIGINT handler that raises KeyboardInterrupt 
        if self._interaction_mode in ('terminal', 'script'):
            signal.signal(signal.SIGINT, signal.default_int_handler)

        if not thread:
            return True

    def _perform(self, expecting_no_output=False):
        ''' Start the program and try to match output.
        
        Spawns the program (starting it in self.cwd),
        compiles list of patterns for expect_list,
        adds EOF to list,
        calls 'started' hook,
        loops calling the '_output_pattern_matched' hook with the index of the pattern
        and the match until EOF whereupon it calls the 'finished' hook.
         
        **Might be running in thread.**
         
        '''
        print 'got here'
        if sys.platform.startswith('win'):
            self._child = winpexpect.winspawn(self.executable, [self.temp_params_file.name] + self.executable_kwargs[:], cwd=self.directory)
        else:
            self._child = pexpect.spawn(self.executable, [self.temp_params_file.name] + self.executable_kwargs[:], cwd=self.directory)
        # note that spawn doesn't like list traits so we copy them using [:] 
        # and directory is defined in Params
        print self._child
        
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
        
        self.success = False
        self.error = '' # public error
        self._errors = '' # private errors
        self.started = True # Event
        self.running = True
        self._was_cancelled = False
        stdout_patterns_matched = 0
        stderr_patterns_matched = 0
        
#        print 'reading lines'
#        print self._child.readlines()
#        print 'finished'
#        return
        # expect loop
        while True:
            pattern_index = self._child.expect_list(
                compiled_pattern_list,
                searchwindowsize=2000, # at least 2000 is required to catch some pmodelchecker output
                timeout=300,
            )
            if pattern_index == eof_index:
                if stdout_patterns_matched + stderr_patterns_matched == 0:
                    if self._child.before != '':
#                        self._errors = self._child.before
                        # scour before for error messages
                        for line in self._child.before.split(os.linesep):
                            for i, pattern in enumerate(self._stderr_pattern_list):
                                match = re.match(pattern, line) 
                                if match is not None:
                                    self._stderr_pattern_matched(len(self._stdout_pattern_list) + i, match)
                                    break # out of inner for loop
                            else:
                                continue # don't break out of outer loop yet
                            for i, pattern in enumerate(self._stdout_pattern_list):
                                match = re.match(pattern, line)
                                print pattern, match.group()
                                if match is not None:
                                    self._stdout_pattern_matched(i, match)
                                    self._stderr_pattern_matched(i, match)
                                    break # out of inner for loop
                            else:
                                continue # don't break out of outer loop yet
                            break # out of outer for loop
                        else:
#                            self._stdout_pattern_matched(-1, self._child.before)
                            print 'Unmatched pattern in %s output: "%s"' % (self.executable_name, self._child.before) 
#                    elif not expecting_no_output:
#                        self._errors += '\nFinished without output.'
                    break # out of while loop
                break
                # process has finished, perhaps prematurely, but can't tell so call it a success
            elif pattern_index == timeout_index:
                self._errors += '\nTimed out.'
                break
            elif pattern_index in stdout_pattern_range:
                self._stdout_pattern_matched(pattern_index, self._child.match)
                stdout_patterns_matched += 1
            elif pattern_index in stderr_pattern_range:
                self._stderr_pattern_matched(pattern_index - len(self._stdout_pattern_list), self._child.match)
                stderr_patterns_matched += 1

        # gather information before finishing
                
        self._finished_without_output = True if stdout_patterns_matched + stderr_patterns_matched == 0 else False
            
        self._child.close() # close file descriptors and store exitstatus and signalstatus        
        if self._child.exitstatus is None:
            self.error = self._interpret_exitcode(self._child.signalstatus)
        else:#elif self._child.exitstatus != 0: # it might appear to have finished normally but we could have found some errors
            self.error = self._interpret_exitcode(self._child.exitstatus)
            
#        self.success = True if self._child.exitstatus == 0 and not self._was_cancelled else False
        self.success = True if self.error == '' and not self._was_cancelled else False
        do_later(setattr, self, 'finished', True) # trigger self._finished_fired in the main thread
        
#        do_later(quit, self._thread) 

    def _error_changed(self):
        if self.error != '':
            if self._interaction_mode == 'script':
                logger.error(self.error)
            elif self._interaction_mode == 'terminal':
                logger.error(self.error)
            elif self._interaction_mode == 'gui':
#                logger.error(error)
#                pass
                GUI.invoke_later(error, self._parent_widget, self.error, 'Experiment failed') # error here is enthought.pyface.api.error
                self._handler.status = self.error #TODO remove?

    def _interpret_exitcode(self, exitcode):
        error = ''
        if exitcode == 2:
            error = '%s was cancelled by the user before data could be written.' % self.executable_name
        elif exitcode == 9:
#            error = '%s was terminated by the user.' % self.executable_name
            pass
        elif self._child.signalstatus == 11:
            error = '%s caused a segmentation fault and was terminated by the operating system.' % self.executable_name
        elif exitcode == 15:
            error = '%s was terminated by this program.' % self.executable_name
        elif exitcode == 127:
            error = '%s triggered a shared library error.' % self.executable_name
        elif exitcode != 0:
            error = '%s exited with returncode %s' % (self.executable_name, exitcode)
        error += self._errors
#        error += '\n(exitcode = %s)' % exitcode
        return error

    error = Str
    success = Bool
    started = Event
    finished = Event

    _parent_widget = Property(Instance(QWidget))

    def _get__parent_widget(self):
#        return None
        return self._handler.info.ui.control

    def _started_fired(self):
        print 'started'
        self._progress_percentage = 0
        if self._interaction_mode == 'gui':
            self._handler._starting()
        else:
            self._progress_bar = ProgressBar(
                fd=sys.stdout,
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

    def cancel(self):
        self._was_cancelled = self._child.terminate(force=True)
    
    def _finished_fired(self):
        '''Sets self.running to False in the main thread'''
        self.running = False
        if self._interaction_mode in ('script', 'terminal'):
            if self.success and not self._finished_without_output:
                self._progress_bar.finish()
            if getattr(self, '_progress_bar_started', False): #FIXME AttributeError: 'McssExperiment' object has no attribute '_progress_bar_started'
                print
        else:#elif self._interaction_mode == 'gui':
            do_later(self._handler._finished, self.success) # do_later is essential to stop crash due to threads
#            if self.success:
#                if not hasattr(self, '_imported_results_modules') or not self._imported_results_modules: # have we done the long import yet?
#                    #TODO auto close message loading (if first time, otherwise it will be fast)
#                    from enthought.traits.ui.message import auto_close_message
##                    GUI.invoke_later(auto_close_message(message='Loading results', time=1))#, parent=self.info.ui.control))
#                    do_later(auto_close_message(message='Loading results', time=1))#, parent=self.info.ui.control))
#                    self._imported_results_modules = True
        
        if sys.platform.startswith('win'):
            os.remove(self.temp_params_file.name) # deletes file on Windows
        del self.temp_params_file # deletes file except on Windows because we set delete=False for other reasons, see perform
        
        self._reset_progress_traits()
        
    def _reset_progress_traits(self):
        self._progress_percentage = 0


    _stdout_pattern_list = ListStr
    _stderr_pattern_list = ListStr([
        '^[eE]rror:.*', # mcss 'error: unknown parameter how_progress'
        '^[eE]rror[^:].+\nline [0-9]+: \([0-9]+ \[Error\]\) .*', # Fran & LibSBML 'error reading sbml input file\nline 1: (00002 [Error]) File unreadable.' 
        '^[eE]rror[^:].*', # Fran 'error ...'
        '^.+: command not found', # bash
        '^I/O warning : failed to load external entity ".+"', # libxml++
        '^Parsing of file (?P<file>.*) according to BNF failed in line: (?P<line>[0-9]*)',
        '^Exception in thread "main" java',
#        'Exception in thread "main" java',
##        ''' Error: parameters with same name and different ranges: 
##0:10:3000:10:100''',
    ])
    
    def _stdout_pattern_matched(self, pattern_index, match):
        raise ValueError('Experiment._stdout_pattern_matched called with unrecognised pattern_index %s' % pattern_index)


    _errors = Str(desc='the error the executable exited with')
            
    def _stderr_pattern_matched(self, pattern_index, match):
#        print 'got here'
        pattern = match.group()
        self._errors += '\n%s' % pattern.strip()
#        if pattern_index == 5:
#            d = match.groupdict()
#            print 'file="%s" line=%s' % (d['file'], d['line'])


    _progress_percentage = Percentage
    
    @on_trait_change('_progress_percentage')    
    def _update_progress_bar(self):
#    def __progress_percentage_changed(self, value): # doesn't work, maybe because of threads...
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
