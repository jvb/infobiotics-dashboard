import platform
if platform.system() == 'Windows':
    import wexpect as expect #TODO test with and include wexpect in sys.path
else:
    import pexpect as expect
from enthought.traits.api import ListStr, Str, Event, Property, Bool
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
    _params_program = ParamsRelativeFile(exists=True, executable=True)
    _params_program_kwargs = ListStr
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
    
#    @on_trait_change('started')
#    def forward_program_output_to_stdout(self):
##    def _started_fired(self):
#        ''' An example of responding to an Event. '''
#        self.child.logfile_read = sys.stdout

    def perform(self, thread=False):
        ''' Spawns an expect process and handles it in a separate thread. '''
        def _spawn():
            ''' Start the program and try to match output.
            
            Spawns the program (starting it in self.cwd), 
            compiles list of patterns for expect_list, 
            adds EOF to list,
            calls 'started' hook,
            loops calling the '_output_pattern_matched' hook with the index of the pattern
            and the match until EOF whereupon it calls the 'finished' hook.
             
            '''
            starting = True
    
            if self._params_program == '':
                print "warning self._params_program == ''"
            if self._params_file == '':
                print "warning self._params_file == ''"
    
            # spawn process
            self.child = expect.spawn(self._params_program, [self._params_file] + self._params_program_kwargs[:], cwd=self._cwd) # _cwd defined in Params
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
                            print self.child.before
                    # process has finished, perhaps prematurely
                    break
                elif pattern_index == timeout_index:
                    self.timed_out = True
                else:
                    self._output_pattern_matched(pattern_index, self.child.match.group())
                    patterns_matched += 1
    
            self.finished = True

        if thread:
            Thread(target=_spawn).start()
        else:
            _spawn()
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
