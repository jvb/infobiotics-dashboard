from infobiotics.shared.api import \
    Params, File, ListStr, Str, Event, expect, Thread, Property, Bool

class Experiment(Params):
    
    _params_program = File(exists=True, executable=True)
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
        if not self.has_valid_parameters():
            return False

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
            while True:
                pattern_index = self.child.expect_list(compiled_pattern_list)
                if pattern_index == eof_index:
                    # process has finished, perhaps prematurely
                    break
                elif pattern_index == timeout_index:
                    self.timed_out = True
                else:
                    self._output_pattern_matched(pattern_index, self.child.match.group())
    
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


if __name__ == '__main__':
    execfile('../mcss/mcss_experiment.py')
    