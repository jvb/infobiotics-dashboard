from enthought.traits.api import ListStr, Str, Event, Property, Bool, on_trait_change
from infobiotics.core.params import Params
import sys 
import os
import tempfile
from threading import Thread

from infobiotics.thirdparty import which
import sys
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
    
from infobiotics.commons.api import logging
log = logging.getLogger(name='Experiment', level=logging.ERROR, format="%(message)s [%(levelname)s]")
log.setLevel(logging.ERROR)
log.setLevel(logging.WARN)
log.setLevel(logging.DEBUG)

class Experiment(Params):
    ''' Abstract base class of all Infobiotics Dashboard experiments.
    
    ParamsExperiments are performed by external programs with parameters from
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

    ParamsExperiment implements usable load(), save() and reset() methods from 
    the IParamsExperiment interface. has_valid_parameters() and 
    parameter_names() are left to subclasses to implement: in ParamsExperiment 
    they each raise a NotImplementedError when called, as does perform() from 
    the Experiment superclass.    
    
    '''
    executable_kwargs = ListStr
    _output_pattern_list = ListStr
    _error_pattern_list = ListStr([
        '^[eE]rror:.*', # mcss 'error: unknown parameter how_progress'
        '^[eE]rror[^:].+\nline [0-9]+: \([0-9]+ \[Error\]\) .*', # Fran & LibSBML 'error reading sbml input file\nline 1: (00002 [Error]) File unreadable.' 
        '^[eE]rror[^:].*', # Fran 'error ...'
        '^.+: command not found', # bash
        '^I/O warning : failed to load external entity ".+"', # libxml++
    ])
    _error_string = Str

    starting = Event # used to reset finished_successfully
    def _starting_fired(self):
        self.finished_successfully = False
    started = Event
    timed_out = Event
    finished = Event
    finished_successfully = Bool
    finished_without_output = Event #TODO

    def perform(self, thread=False):#TODO make thread True by default?
        ''' Spawns an expect process and handles it in a separate thread. '''
        # save to temporary file in the same directory
        kwargs = dict(
            prefix=self._params_file.split('.params')[0],
            suffix='.params',
            dir=self.directory,
        ) 
        if sys.platform.startswith('win'): 
            print os.path.splitunc(self._params_file_) #TODO use for paths
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
        if sys.platform.startswith('win'): self.temp_params_file.close() # see comment http://bit.ly/gUSEh0
        self.save(self.temp_params_file.name, force=True, update_object=False)
        #TODO maybe repeat this pattern in PModelCheckerParams.translate_model_specification when model_specification == ''
        if not thread or self._interaction_mode == 'terminal':
            self._perform() # always do this in terminal mode
            #TODO call serial progress function from here
        else:
            Thread(target=self._perform).start()
#        print 'executed'
        return True

    def _perform(self):
        '''Might be running in a thread.'''
        self.starting = True
        self.__expect()
        self.finished = True

    def _finished_fired(self):
        if self.finished_successfully:
            log.debug('succeeded')
        else:
            log.debug('failed')
        if sys.platform.startswith('win'):
            os.remove(self.temp_params_file.name) #TODO test
        else:
            del self.temp_params_file

#    def __subprocess(self):
#                
#        def cancel(process):
#            import signal
#            os.kill(process.pid, signal.SIGINT)
#            #http://docs.python.org/library/os.html#os.kill
#            #http://docs.python.org/library/signal.html#signal.CTRL_C_EVENT
#        self.cancel = cancel
#            
#        def last_non_empty_line(liststr):
#            for line in reversed(liststr):
#                if len(line) > 0:
#                    return line
#            return None
#        
#        args = [self.executable, self.temp_params_file.name] + self.executable_kwargs[:]
#        arg_string = ' '.join(args)
#        kwargs = dict(
#            cwd=self.directory,
#            stdout=subprocess.PIPE, # capture stdout
#            stderr=subprocess.PIPE, # capture stderr
#        )
#        if subprocess.mswindows:
#            # prevent empty terminal window opening (http://bit.ly/hNQUlQ)
#            su = subprocess.STARTUPINFO() 
#            su.dwFlags |= subprocess.STARTF_USESHOWWINDOW 
#            su.wShowWindow = subprocess.SW_HIDE 
#            kwargs.update(startupinfo=su)
#        p = subprocess.Popen(args, **kwargs)
##        import time
##        time.sleep(0.005)
##        cancel(p)
##        #p.terminate()
##        ##p.kill() # kill        
#        self.started = True
#        self.error_log_file_name = 'mcss-error.log'
#        error_log = None
#        stdout_output, stderr_output = p.communicate()
#        if p.returncode == 0: # returncode is set by communicate() 
#            self.finished_successfully = True # trigger ExperimentHandler.show_results()
#        else:
#            error_log = open(self.error_log_file_name, 'w')
#            if p.returncode == 1:
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
#                            error = '%s exited with return code %s' % (arg_string, p.returncode)
#            elif p.returncode == -2:
#                error = '%s was cancelled by the user before data could be written.' % arg_string
#            elif p.returncode == -9:
#                error = '%s was terminated by the user.' % arg_string
#            elif p.returncode == -11:
#                error = '%s caused a segmentation fault and was terminated by the operating system.' % arg_string
#            elif p.returncode == -15:
#                error = '%s was terminated by the dashboard.' % arg_string
#            elif p.returncode == 127:
#                error = 'shared library error'
#            else:
#                error = '%s exited with returncode %s' % (arg_string, p.returncode)
##            self.log.error(error)
#            error_log.write(error)
#            error_log.close()

    def __expect(self):
        ''' Start the program and try to match output.
        
        Spawns the program (starting it in self.cwd), 
        compiles list of patterns for expect_list, 
        adds EOF to list,
        calls 'started' hook,
        loops calling the '_output_pattern_matched' hook with the index of the pattern
        and the match until EOF whereupon it calls the 'finished' hook.
         
        '''
        if sys.platform.startswith('win'):
            self.child = winpexpect.winspawn(self.executable, [self.temp_params_file.name] + self.executable_kwargs[:], cwd=self.directory)
        else:
            self.child = pexpect.spawn(self.executable, [self.temp_params_file.name] + self.executable_kwargs[:], cwd=self.directory)
        # note that spawn doesn't like list traits so we copy them using [:] 
        # and directory is defined in Params

        # compile pattern list for expect_list
        compiled_pattern_list = self.child.compile_pattern_list(self._output_pattern_list + self._error_pattern_list)
        
        # append EOF to compiled pattern list
        compiled_pattern_list.append(pexpect.EOF)
        eof_index = compiled_pattern_list.index(pexpect.EOF)
        
        # append TIMEOUT to compiled pattern list
        compiled_pattern_list.append(pexpect.TIMEOUT)
        timeout_index = compiled_pattern_list.index(pexpect.TIMEOUT)
        
        self.started = True

        # expect loop
        import re
        patterns_matched = 0
        eof = True
        while eof:
            pattern_index = self.child.expect_list(compiled_pattern_list, searchwindowsize=100)
            if pattern_index == eof_index:
                if patterns_matched == 0:
                    if self.child.before != '':
                        # scour before for error messages
                        for line in self.child.before.split(os.linesep):
                            for i, pattern in enumerate(self._error_pattern_list):
                                if re.match(pattern, line) is not None:
                                    self._output_pattern_matched(len(self._output_pattern_list) + i, line)
                                    break # out of inner for loop
                            else:
                                continue # don't break out of outer loop yet
                            break # out of outer for loop
                        else:
                            self._output_pattern_matched(-1, self.child.before)
                    else:
                        self.finished_without_output = True #TODO
                    break # out of while loop
                eof = False
                # process has finished, perhaps prematurely, but can't tell so call it a success
            elif pattern_index == timeout_index:
                log.debug('timed out')
                self.timed_out = True #TODO
            else:
                self._output_pattern_matched(pattern_index, self.child.match.group())
                patterns_matched += 1
        else: # while loop finished without a break
            self.finished_successfully = True
        
    def _output_pattern_matched(self, pattern_index, match):
        '''Update traits in response to matching error patterns.
        
        Subclasses should call this method after processing their own patterns, e.g.:
            if pattern_index == 0:
                # do something
            elif pattern_index == 1:
                # do something else
            else:
                Experiment._output_pattern_matched(self, pattern_index, match)

        '''
        self._error_string = match.strip()
        if self._interaction_mode == 'terminal':
            print self._error_string
        elif self._interaction_mode == 'script':
            self.log.error(self._error_string)
        else:
            print 'got here'
    
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
