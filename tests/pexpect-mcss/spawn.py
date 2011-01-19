import pexpect as expect
print expect.__version__
import os
import sys
from infobiotics.mcss.api import McssExperiment
params_file_name = '/home/jvb/src/mcss-0.0.41/examples/models/module1.params'
directory = os.path.dirname(params_file_name) 
executable = '/usr/bin/mcss'
executable_kwargs = ['show_progress=true', 'runs=1000']
#experiment = McssExperiment()
#experiment.load(params_file_name)
#args = [experiment.executable, experiment._params_file] + executable_kwargs

_output_pattern_list = [
    '[0-9]+ [0-9]+', # 'time_in_run, run'
] 

def _output_pattern_matched(pattern_index, match):
    if pattern_index == 0: # '1 20.5'
        time_in_run, run = match.split(' ')
        print int(run),
        print float(time_in_run)
        if int(run) > 2:
            child.terminate(force=True) # cancel
    else:
        print match.groups()
#        super(McssExperiment, self)._output_pattern_matched(pattern_index, match)
        
try:
    # spawn process
    if sys.platform.startswith('win'):
        child = expect.winspawn(executable, [params_file_name] + executable_kwargs[:], cwd=directory)
    else:
        child = expect.spawn(executable, [params_file_name] + executable_kwargs[:], cwd=directory)
    # note that the expect module doesn't like list traits so we copy them using [:] 
    # and directory is defined in Params
    
    # compile pattern list for expect_list
    compiled_pattern_list = child.compile_pattern_list(_output_pattern_list)# + _error_pattern_list)
    
    # append EOF to compiled pattern list
    compiled_pattern_list.append(expect.EOF)
    eof_index = compiled_pattern_list.index(expect.EOF)
    
    # append TIMEOUT to compiled pattern list
    compiled_pattern_list.append(expect.TIMEOUT)
    timeout_index = compiled_pattern_list.index(expect.TIMEOUT)
    
    #self.started = True
    
    # expect loop
    patterns_matched = 0
    while True:
        #TODO can we abort if process finished?
        pattern_index = child.expect_list(compiled_pattern_list, searchwindowsize=100)
        if pattern_index == eof_index:
            if patterns_matched == 0:
                if child.before != '':
                    print child.before#finished_without_output = True
            # process has finished, perhaps prematurely
            break
        elif pattern_index == timeout_index:
            print 'timed out'#self.timed_out = True
        else:
            _output_pattern_matched(pattern_index, child.match.group())
            patterns_matched += 1
#        print patterns_matched

except Exception, e:
    print e    
