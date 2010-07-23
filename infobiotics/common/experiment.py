import sys
if sys.platform.startswith('win'):

    # for py2exe frozen executables:
    
    # ModuleFinder can't handle runtime changes to __path__, but win32com uses them
    import pywintypes
    import pythoncom
    import win32api
    try:
    # if this doesn't work, try import modulefinder
        import py2exe.mf as modulefinder
        import win32com
        for p in win32com.__path__[1:]:
            modulefinder.AddPackagePath("win32com", p)
        for extra in ["win32com.shell"]: #,"win32com.mapi"
            __import__(extra)
            m = sys.modules[extra]
            for p in m.__path__[1:]:
                modulefinder.AddPackagePath(extra, p)
    except ImportError:
        # no build path setup, no worries.
        pass
    
    import infobiotics.thirdparty.winpexpect as expect
else:
    import pexpect as expect
#    import infobiotics.thirdparty.pexpect as expect
from enthought.traits.api import ListStr, Str, Event, Property, Bool, on_trait_change
from threading import Thread
from infobiotics.common.api import Params, ParamsRelativeFile

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
    _output_pattern_list = ListStr
    _error_pattern_list = ListStr([
        '^[eE]rror:.*', # mcss 'error: unknown parameter how_progress'
        '^[eE]rror[^:].+\nline [0-9]+: \([0-9]+ \[Error\]\) .*', # Fran & LibSBML 'error reading sbml input file\nline 1: (00002 [Error]) File unreadable.' 
        '^[eE]rror[^:].*', # Fran 'error ...'
        '^.+: command not found', # bash
        '^I/O warning : failed to load external entity ".+"', # libxml++
    ])
    _error_string = Str

    starting = Event
    started = Event
    timed_out = Event
    finished = Event
    finished_without_output = Event

#    @on_trait_change('started')
#    def forward_program_output_to_stdout(self):
#        self.child.logfile_read = sys.stdout

#    @on_trait_change('started')
#    def print_experiment_command_line(self):
#        # debugging #TODO silence
#        print 'executable =', self.executable
#        print 'params file =', self._params_file
#        print 'overridden parameters =', self.executable_kwargs
#        print 'directory =', self.directory
    
#    @profile
    def _spawn(self):
        ''' Start the program and try to match output.
        
        Spawns the program (starting it in self.cwd), 
        compiles list of patterns for expect_list, 
        adds EOF to list,
        calls 'started' hook,
        loops calling the '_output_pattern_matched' hook with the index of the pattern
        and the match until EOF whereupon it calls the 'finished' hook.
         
        '''
        self.starting = True
        
#        try:
#    
#            # spawn process
#            if sys.platform.startswith('win'):
#                self.child = expect.winspawn(self.executable, [self._params_file] + self.executable_kwargs[:], cwd=self.directory)
#            else:    
#                self.child = expect.spawn(self.executable, [self._params_file] + self.executable_kwargs[:], cwd=self.directory)
#            # note that the expect module doesn't like list traits so we copy them using [:] 
#            # and directory is defined in Params
#    
#            # compile pattern list for expect_list
#            compiled_pattern_list = self.child.compile_pattern_list(self._output_pattern_list + self._error_pattern_list)
#            
#            # append EOF to compiled pattern list
#            compiled_pattern_list.append(expect.EOF)
#            eof_index = compiled_pattern_list.index(expect.EOF)
#            
#            # append TIMEOUT to compiled pattern list
#            compiled_pattern_list.append(expect.TIMEOUT)
#            timeout_index = compiled_pattern_list.index(expect.TIMEOUT)
#            
#            self.started = True
#
#            # expect loop
#            patterns_matched = 0
#            while True:
#                pattern_index = self.child.expect_list(compiled_pattern_list, searchwindowsize=100)
#                if pattern_index == eof_index:
#                    if patterns_matched == 0:
#                        if self.child.before != '':
#                            self.finished_without_output = True
#                    # process has finished, perhaps prematurely
#                    break
#                elif pattern_index == timeout_index:
#                    self.timed_out = True
#                else:
#                    self._output_pattern_matched(pattern_index, self.child.match.group())
#                    patterns_matched += 1
##            print patterns_matched
#    
#        except Exception, e:
#            print e
        import subprocess
        if subprocess.mswindows: # http://www.gossamer-threads.com/lists/python/python/783937#783937
            su = subprocess.STARTUPINFO() 
            su.dwFlags |= subprocess.STARTF_USESHOWWINDOW 
            su.wShowWindow = subprocess.SW_HIDE 
            p = subprocess.Popen([self.executable, self._params_file] + self.executable_kwargs[:], startupinfo=su, cwd=self.directory) # directory defined in Params
        else:
            p = subprocess.Popen([self.executable, self._params_file] + self.executable_kwargs[:], 
                cwd=self.directory, # directory defined in Params
#                # debugging
#                stdout=subprocess.PIPE,
#                stderr=subprocess.PIPE,#STDOUT,
            ) 
        self.started = True
        p.wait()

        # trigger ExperimentHandler.show_results()
        self.finished = True

    def _finished_fired(self):
        del self.temp_params_file #TODO test this
        
#    def _finished_without_output_fired(self):
#        print '_finished_without_output_fired', self.child.before

    def perform(self, thread=False):
        ''' Spawns an expect process and handles it in a separate thread. '''
        
#        print 'got here also' #TODO remove this and others
        
        #TODO check if dirty/saved first

        # save to temporary file in the same directory
        
        import tempfile
        self.temp_params_file = tempfile.NamedTemporaryFile(dir=self.directory)
            
        self.save(self.temp_params_file.name)
    #    import os.path
    #    if not os.path.exists(os.path.abspath(os.path.join(translate_experiment.directory, translate_experiment.PRISM_model))):
    #        del temp_file
    #        raise Exception('%s was not created.' % self.PRISM_model)        
        
        if thread:
            Thread(target=self._spawn).start()
        else:
            self._spawn()
            #TODO call serial progress function from here
        return True

    def _output_pattern_matched(self, pattern_index, match):
        ''' Update traits in response to matching error patterns.
        
        Subclasses should call this method after processing their own patterns,
        e.g.:
            if pattern_index == 0:
                # do something
            elif pattern_index == 1:
                # do something else
            else:
                super(McssExperiment, self)._output_pattern_matched(pattern_index, match)
                
        '''
        self._error_string = match.split('rror')[1].strip(':') if 'rror' in match else match

    def __error_string_changed(self, _error_string):
        print _error_string, '(from Experiment.__error_string_changed)'


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
