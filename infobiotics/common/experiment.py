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
from enthought.traits.api import ListStr, Str, Event, Property, Bool
from threading import Thread
from infobiotics.common.api import Params, ParamsRelativeFile

'''
from which import which, WhichError
import os
import winpexpect as expect


# mcss-specific

executable = 'mcss'
_params_file = 'module1.params'
executable_kwargs = ['sho', 'runs=2', 'max_time=100']
directory = os.getcwd()
_output_pattern_list = [
    '[0-9]+ [0-9]+', # 'time_in_run, run'
]


# Experiment

_error_pattern_list = [
#    '^I/O warning : failed to load external entity ".+"', # libxml++
    "^[eE]rror: couldn't parse command line parameter .*$", 
#    '^[eE]rror: unknown parameter .*', 
#    '^[eE]rror: value .*', 
#    '^[eE]rror[^:].+\nline [0-9]+: \([0-9]+ \[Error\]\) .*', # Fran & LibSBML 'error reading sbml input file\nline 1: (00002 [Error]) File unreadable.' 
#    '^[eE]rror[^:].*', # Fran 'error ...'
#    '^[eE]rror:.*', # mcss 'error: unknown parameter how_progress' or 'error: value'
#    '^.+: command not found', # bash
]

try:
    command = which(executable)
    print 'using', command
except WhichError:
    exit("Error: Cannot locate '%s' on environment PATH." % executable)    

child = expect.winspawn(command, [_params_file] + executable_kwargs[:], cwd=directory)

compiled_pattern_list = child.compile_pattern_list(_output_pattern_list + _error_pattern_list)
        
compiled_pattern_list.append(expect.EOF)
eof_index = compiled_pattern_list.index(expect.EOF)

compiled_pattern_list.append(expect.TIMEOUT)
timeout_index = compiled_pattern_list.index(expect.TIMEOUT)

patterns_matched = 0

while True:

    pattern_index = child.expect_list(compiled_pattern_list)
    
    if pattern_index == eof_index:
        if patterns_matched == 0:
            if child.before != '':
                finished_without_output = True
                print child.before
        # process has finished, perhaps prematurely
        break
        
    elif pattern_index == timeout_index:
        timed_out = True
        
    else:
        match = child.match.group() # only gets the *first* match for the line
        
        # McssExperiment
        if pattern_index == 0: # '1 20.5'
            time_in_run, run = match.split(' ')
            print float(time_in_run), int(run)
        # Experiment
#        '^[eE]rror:.*', # mcss 'error: unknown parameter how_progress'
#        '^[eE]rror[^:].+\nline [0-9]+: \([0-9]+ \[Error\]\) .*', # Fran & LibSBML 'error reading sbml input file\nline 1: (00002 [Error]) File unreadable.' 
#        '^[eE]rror[^:].*', # Fran 'error ...'
#        '^.+: command not found', # bash
#        '^I/O warning : failed to load external entity ".+"', # libxml++
        #elif pattern_index == 1 + len(_output_pattern_list):
        #    print match
        #elif pattern_index == 2 + len(_output_pattern_list):
        #    print match
        #elif pattern_index == 3 + len(_output_pattern_list):
        #    print match
        #elif pattern_index == 4 + len(_output_pattern_list):
        #    print match
        #elif pattern_index == 5 + len(_output_pattern_list):
        #    print match
        elif len(_output_pattern_list) <= pattern_index < len(_output_pattern_list) + len(_error_pattern_list):
            pass
#            print 'child.match.string = ', child.match.string
#            print 'child.match.re.pattern = ', child.match.re.pattern
            print 'child.before =', child.before
            print 'match = ', match
            print 'child.after =', child.after
            print


        patterns_matched += 1

print 'child.before =', child.before
print 'child.after =', child.after
#print patterns_matched
'''

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
##    def _started_fired(self):
#        ''' An example of responding to an Event. '''
#        self.child.logfile_read = sys.stdout

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

        #FIXME are these still relevant now that executable is found in preferences or PATH?
        if self.executable == '':
            print "warning self.executable == ''"
        if self._params_file == '':
            print "warning self._params_file == ''"
#            print self.executable, self._params_file, self.executable_kwargs, self.directory

        # spawn process
        if sys.platform.startswith('win'):
            self.child = expect.winspawn(self.executable, [self._params_file] + self.executable_kwargs[:], cwd=self.directory) # directory defined in Params
        else:    
            self.child = expect.spawn(self.executable, [self._params_file] + self.executable_kwargs[:], cwd=self.directory) # directory defined in Params
        # note that the expect module doesn't like list traits so we copy them using [:] 

        # useful for debugging
#            self.child.logfile_read = sys.stdout #TODO comment out in release

        self.started = True

        # compile pattern list for expect_list
        compiled_pattern_list = self.child.compile_pattern_list(self._output_pattern_list + self._error_pattern_list)
        
        # append EOF to compiled pattern list
        compiled_pattern_list.append(expect.EOF)
        eof_index = compiled_pattern_list.index(expect.EOF)
        
        # append TIMEOUT to compiled pattern list
        compiled_pattern_list.append(expect.TIMEOUT)
        timeout_index = compiled_pattern_list.index(expect.TIMEOUT)
        
        # expect loop
        patterns_matched = 0
        while True:
            pattern_index = self.child.expect_list(compiled_pattern_list)
            if pattern_index == eof_index:
                if patterns_matched == 0:
                    if self.child.before != '':
                        self.finished_without_output = True
                # process has finished, perhaps prematurely
                break
            elif pattern_index == timeout_index:
                self.timed_out = True
            else:
                self._output_pattern_matched(pattern_index, self.child.match.group())
                patterns_matched += 1
        self.finished = True
#        print patterns_matched

    def _finished_without_output_fired(self):
        print '_finished_without_output_fired', self.child.before

#    def _finished_fired(self):
#        print 'finished'

    def perform(self, thread=False):
        ''' Spawns an expect process and handles it in a separate thread. '''
##    def __params_program_default(self): #TODO get_preference(name, contigency_function)
##            from infobiotics.thirdparty.which import which, WhichError
##            try:
##                _params_program = which(self._params_program_name)
##            except WhichError:
##                _params_program = None
##            if _params_program is None:
##                # we can't find it so print error message and exit #FIXME what does this do in the interpreter? 
##                import sys
##                sys.stderr.write(
##                    "error: '%s' could not be located on PATH. " \
##                    "Either change PATH to include '%s' " \
##                    "or amend '%s' with its correct location.\n" % (
##                        self._params_program_name, 
##                        self._params_program_name, 
##                        get_default_preferences().filename,
##                    )
##                )
##                sys.exit(1)
#
#        import os
#        if not os.path.isfile(self.executable):
#            if self._interactive:
#                #TODO message box explaining that executable does not exist or is not executable and that another should be specified using the preferences dialog
#                while True:
#                    if not self.handler.edit_preferences(self.handler.info): # self.executable will be updated if True returned
#                        return False
#                    elif os.path.isfile(self.executable):
#                        break
#            else:
#                import sys
#                sys.stderr.write("'%s' does not exist. Please specify an alternative %s executable either by using McssExperiment(executable=/full/path/to/executable, ...) or by editing the 'executable' entry in section [%s] of the preferences file '%s'.\n" % (self.executable, self.executable_name, self.executable_name, self.preferences_helper.preferences.filename))
#                return False
#
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
                # pattern_index not defined by this class, pass to superclass
                ParamsExpect._output_pattern_matched(self, pattern_index, match)
                # or
#                super(McssExpect, self)._output_pattern_matched(pattern_index, match)
                
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
