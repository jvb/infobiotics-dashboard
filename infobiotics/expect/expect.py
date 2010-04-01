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

class Expect(HasTraits):
    ''' Wraps common pattern of expect usage with traits (including events).
    
    The main advantage of Expect is that it appears as a pseudo-terminal to C 
    programs stdio methods, which therefore treat it as 'line-buffered' in 
    contrast to 'buffered' when using subprocess.Popen(stdout=subprocess.PIPE),
    meaning program output is seen immediately rather than when the buffer is 
    full.
    
    '''
    program = File
    program_args_list = ListStr
    pattern_list = ListStr
    
    cwd = Directory(os.getcwd())
#    def _cwd_default(self):
#        return os.getcwd()

    starting = Event
    started = Event
    timed_out = Event
    finished = Event
    
    @on_trait_change('started')
    def forward_program_output_to_stdout(self): 
#    def _started_fired(self):
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
        self.child = expect.spawn(self.program, self.program_args_list[:], cwd=self.cwd)
        # note that the expect module doesn't like list traits so we copy them using [:] 

        self.started = True

        # compile pattern list for expect_list
        compiled_pattern_list = self.child.compile_pattern_list(self.pattern_list[:])
        
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
        ''' pattern matched hook. '''
        raise NotImplementedError('All subclasses should at least override this method.')
    

if __name__ == '__main__':
    pattern_list = [
        'initialization',
        'parameter optimization [0-9]+/[0-9]+',
        '[0-9]+ [0-9]+[.][0-9]+ .+\n',
        'simulate final model',
    ]
    e = Expect(program='./expect_tester', program_args_list=['./poptimizer.stdout'], pattern_list=pattern_list)
    e.start()
    e.configure_traits()
    if hasattr(e, 'child'): 
        e.child.terminate(True)