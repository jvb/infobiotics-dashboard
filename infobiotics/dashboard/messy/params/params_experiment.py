from __future__ import division
import platform
if platform.system() == 'Windows':
    import wexpect as expect #TODO test with and include wexpect in sys.path
else:
    import pexpect as expect
import os
import sys
from threading import Thread
from enthought.traits.api import HasTraits, File, ListStr, Event, Str, on_trait_change, implements
from infobiotics.dashboard.interfaces import IExperiment
from infobiotics.dashboard.params.api import Params 

#from infobiotics.shared.traits_imports import *
#import os
#from infobiotics.dashboard.plugins.experiments.params_experiment_handler import ParamsExperimentHandler
#from infobiotics.dashboard.shared.unified_logging import unified_logging
#logger = unified_logging.get_logger('params_experiment')

class ParamsExperiment(Params):
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
    implements(IExperiment)
    
    _params_program = File(exists=True, desc='path to the executable that accepts the experiments params file.')
    args = ListStr
    pattern_list = ListStr
    error_pattern_list = ListStr([
        '^[eE]rror:.*', # mcss 'error: unknown parameter how_progress'
        '^[eE]rror[^:].+\nline [0-9]+: \([0-9]+ \[Error\]\) .*', # Fran & LibSBML 'error reading sbml input file\nline 1: (00002 [Error]) File unreadable.' 
        '^[eE]rror[^:].*', # Fran 'error ...'
        '^.+: command not found', # bash
        '^I/O warning : failed to load external entity ".+"', # libxml++
    ])
    error_string = Str
    starting = Event
    started = Event
    timed_out = Event
    finished = Event

#    @on_trait_change('started')
#    def forward_program_output_to_stdout(self):
##    def _started_fired(self):
#        ''' An example of responding to an Event. '''
#        self.child.logfile_read = sys.stdout

    def perform(self): 
        ''' Spawns an expect process and handles it in a separate thread. '''
#        if not self.has_valid_parameters():
#            return False

        self._spawn() 
#        Thread(target=self._spawn).start()

    def has_valid_parameters(self): 
        raise NotImplementedError
#        self.error = '' #TODO see Invalid...demo

    def _spawn(self):
        ''' Start the program and try to match output.
        
        Spawns the program (starting it in self.cwd), 
        compiles list of patterns for expect_list, 
        adds EOF to list,
        calls 'started' hook,
        loops calling the 'pattern_matched' hook with the index of the pattern
        and the match until EOF whereupon it calls the 'finished' hook.
         
        '''
        starting = True

        # spawn process
        self.child = expect.spawn(self._params_program, [self._params_file] + self.args[:], cwd=self._cwd) # _cwd defined in Params
        # note that the expect module doesn't like list traits so we copy them using [:] 

#        # useful for debugging
#        self.child.logfile_read = sys.stdout

        self.started = True

        # compile pattern list for expect_list
        compiled_pattern_list = self.child.compile_pattern_list(self.pattern_list + self.error_pattern_list)
        
        # append EOF to compiled pattern list
        compiled_pattern_list.append(expect.EOF)
        eof_index = compiled_pattern_list.index(expect.EOF)
        
        # append TIMEOUT to compiled pattern list
        compiled_pattern_list.append(expect.TIMEOUT)
        timeout_index = compiled_pattern_list.index(expect.TIMEOUT)
        
        # expect loop
        while True:
            pattern_index = self.child.expect_list(compiled_pattern_list)
            if pattern_index == eof_index:
                # process has finished, perhaps prematurely
                break
            elif pattern_index == timeout_index:
                self.timed_out = True
            else:
                self.pattern_matched(pattern_index, self.child.match.group())

        self.finished = True

    #TODO _output_pattern_matched
    def pattern_matched(self, pattern_index, match):
        ''' Update traits in response to matching error patterns.
        
        Subclasses should call this method after processing their own patterns,
        e.g.:
            if pattern_index == 0:
                # do something
            elif pattern_index == 1:
                # do something else
            else:
                # pattern_index not defined by this class, pass to superclass
                ParamsExpect.pattern_matched(self, pattern_index, match)
                # or
#                super(McssExpect, self).pattern_matched(pattern_index, match)
                
        '''
        self.error_string = match.split('rror')[1].strip(':') if 'rror' in match else match


    # changed to _params_file
#    #FIXME prefer 'path' as trait name? -> affects ParamsExperimentEditor
#    #TODO Experiment.file = ... # load or save file on change?
#    file = File(desc='the name of the .params file containing this experiments parameters, updated on save() and load(), to be passed to program.')
#    def _file_changed(self, file): #TODO
#        pass
##        print '%s.file changed' % self.__class__.__name__
    
#    _cwd_item = Item('_cwd', label='Current working directory', visible_when='object._has_unresolved_paths')
#    _has_unresolved_paths = Bool(False)
#    # relative paths of File parameters are resolved from the path of the loaded parameters file
#    # which will be None if not loaded in which case the user must be prompted.
#    _cwd = Directory(desc='')
#    def __cwd_changed(self, _cwd):
#        pass
##        print _cwd
##        os.chdir(self._cwd)
#        #TODO use for keeping cwd across multiple experiments, change to it when editor becomes active, use instead of os.getcwd()
##        print self.preferences, self
##        self.preferences.set('%s._cwd' % self.parameters_name, _cwd)
##        self.preferences.flush()
##        print self.preferences.get('%s._cwd' % self.parameters_name)
##    #FIXME add a current_working_directroy Directory trait to all experiments and expose in Views!

