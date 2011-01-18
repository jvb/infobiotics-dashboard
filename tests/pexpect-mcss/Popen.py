def cancel(process):
    import signal
    os.kill(process.pid, signal.SIGINT)
    #http://docs.python.org/library/os.html#os.kill
    #http://docs.python.org/library/signal.html#signal.CTRL_C_EVENT
    
def last_non_empty_line(liststr):
    for line in reversed(liststr):
        if len(line) > 0:
            return line
    return None

import subprocess, os
#p = subprocess.Popen(os.path.join(os.path.dirname(__file__), 'segfault'))
#print p.communicate()
#print p.returncode
#exit()

from infobiotics.mcss.api import McssExperiment
experiment = McssExperiment()
params_file_name = '/home/jvb/src/mcss-0.0.41/examples/models/module1.params'
experiment.load(params_file_name)
args = [experiment.executable, experiment._params_file]#params_file_name
args += ['show_progress=true']
#args += ['show_progress=true', 'runs=10000']
args += ['model_file=wrong'] # incorrent parameters
#args = [os.path.join(os.path.dirname(__file__), 'segfault')] # segfault
kwargs = dict(
    cwd=experiment.directory,
    stdout=subprocess.PIPE, # capture stdout
    stderr=subprocess.PIPE, # capture stderr
)
arg_string = ' '.join(args)
error_log_file_name = 'mcss-error.log'
error_log = None
p = subprocess.Popen(args, **kwargs)

#import time
#time.sleep(0.005)
#cancel(p)
##p.terminate()
###p.kill() # kill

stdout_output, stderr_output = p.communicate()
if p.returncode == 0: # returncode is set by communicate() 
    pass
else:
    error_log = open(error_log_file_name, 'w')
    if p.returncode == 1:
        # get last non-empty line of stdout or None
        if len(stderr_output) > 0:#stderr_output != '':
            stdout_output_error = last_non_empty_line(stdout_output.split(os.linesep))
            stderr_output_error = last_non_empty_line(stderr_output.split(os.linesep))
            if stdout_output_error is not None:
                if stderr_output_error is not None:
                    error = os.linesep.join((stdout_output_error, stderr_output_error))
                else:
                    error = stdout_output_error
            else:
                if stderr_output_error is not None:
                    error = stderr_output_error
                else:
                    error = '%s exited with return code %s' % (arg_string, p.returncode)
    elif p.returncode == -2:
        error = '%s was cancelled by the user before data could be written.' % arg_string
    elif p.returncode == -9:
        error = '%s was terminated by the user.' % arg_string
    elif p.returncode == -11:
        error = '%s caused a segmentation fault and was terminated by the operating system.' % arg_string
    elif p.returncode == -15:
        error = '%s was terminated by the dashboard.' % arg_string
    else:
        error = '%s exited with returncode %s' % (arg_string, p.returncode)
    error_log.write(error)
    error_log.close()
if error_log is not None:
    for line in open(error_log_file_name, 'r'):
        print line,
