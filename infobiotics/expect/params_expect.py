'''
Reusable classes for pexpect/wexpect interaction with Infobiotics components. 

See http://pexpect.sourceforge.net/pexpect.html#spawn-expect for pexpect API.

To log interactions to sys streams: 
    import sys
    child.logfile_read = sys.stdout # send child stdout to sys stdout
    #child.logfile_send = sys.stderr # sends my stdin to sys stderr

To read stdout directly
    for line in child.readlines(1):
        print line.replace('\n','')

stderr is mixed in with stdout, must use patterns to infer errors.

expect_list uses compiled regex and is therefore a bit faster.

'''

from __future__ import division
import platform
if platform.system() == 'Windows':
    import wexpect as expect #TODO test with and include wexpect in sys.path
else:
    import pexpect as expect
import os
import sys
from threading import Thread
from enthought.traits.api import HasTraits, File, ListStr, Directory, Event, Str, on_trait_change
from enthought.traits.ui.api import View, Group, Item


error_string_group = Group(
    Item('error_string',
        show_label=False,
        style='readonly',
        emphasized=True,
    ),
    visible_when='len(object.error_string) > 0',
    label='Error(s)',
)


class ParamsExpect(HasTraits): #TODO Controller/ModelView
    ''' Reimplements Expect to apply to params programs.
    
    '''
    params_program = File(exists=True)
    params_file = File(exists=True)
    args = ListStr
    cwd = Directory(os.getcwd())
#    def _cwd_default(self):
#        return os.getcwd()
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

    @on_trait_change('params_file')
    def update_cwd_from_params_file(self, params_file):
        ''' Update cwd and params_file from params_file. '''
        if os.path.isabs(params_file) and os.path.isfile(params_file):
             self.cwd, self.params_file = os.path.split(params_file)
    
    @on_trait_change('started')
    def forward_program_output_to_stdout(self):
#    def _started_fired(self):
        ''' An example of responding to an Event. '''
        self.child.logfile_read = sys.stdout

    def start(self):
        Thread(target=self.spawn).start() 
            
    def spawn(self):
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
        self.child = expect.spawn(self.params_program, [self.params_file] + self.args[:], cwd=self.cwd)
        # note that the expect module doesn't like list traits so we copy them using [:] 

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
                # process has finished
                break
            elif pattern_index == timeout_index:
                self.timed_out = True
            else:
                self.pattern_matched(pattern_index, self.child.match.group())

        self.finished = True

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
                super(McssExpect, self).pattern_matched(pattern_index, match)
                
        '''
        self.error_string = match.split('rror')[1].strip(':') if 'rror' in match else match

    traits_view = View(
        error_string_group,
        width=300,
        resizable=True,
    )
