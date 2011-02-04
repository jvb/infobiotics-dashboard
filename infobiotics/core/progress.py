from enthought.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'qt4'
from enthought.traits.api import *
from enthought.traits.ui.api import *
import sys
if sys.platform.startswith('win'):
    import winpexpect
import pexpect
from progressbar import ProgressBar, Percentage, Bar, RotatingMarker, ETA


class Experiment(HasTraits):
    
    _command = Str('python process.py')
    
    def _starting(self):
        if self._interaction_mode not in ('script', 'terminal'):
            self._handler._starting()
        else:
            print 'Experiment._starting'
            self._progress_bar = ProgressBar(
                widgets=[
                    self._command,
                    ' ',
                    Percentage(),
                    ' ',
                    Bar(marker=RotatingMarker()),
                    ' ',
                    ETA()
                ],
                maxval=100,
            )
            self._progress_bar_started = False

    
    def _finished(self):
        if self._interaction_mode not in ('script', 'terminal'):
            self._handler._finished()
        else:
            print 'Experiment._finished'
    
    _handler = Instance('ExperimentHandler')
    
    def __handler_default(self):
        return ExperimentHandler(model=self)

    _interaction_mode = Enum(['script', 'terminal', 'gui'])
    
    def _interaction_mode_default(self):
        import sys
        if sys.stdout.isatty():
            return 'terminal'
        else:
            return 'script'

#    def __interaction_mode_changed(self, name, old, new):
#        print name, old, new

    def configure(self, **traits):
        '''Starts event loop.'''
        interaction_mode = self._interaction_mode
        self._interaction_mode = 'gui'
        self._handler.configure_traits(**traits)
        self._interaction_mode = interaction_mode

    def edit(self, **traits):
        '''Doesn't start event loop.'''
        # doesn't change self.interaction mode to 'gui' because it will already be that if configure previously called and if not then this will return straight away anyway 
        self._handler.edit_traits(**traits)

    def perform(self):
        
        self._child = pexpect.spawn('python process.py')
        
        self._stdout_pattern_list = [
            '[0-9]+'
        ]
        stdout_pattern_range = range(0, len(self._stdout_pattern_list))
        
        self._stderr_pattern_list = [
            '[Ee]rror.+'
        ]
        stderr_pattern_range = range(len(self._stdout_pattern_list), len(self._stdout_pattern_list) + len(self._stderr_pattern_list))
        
        # compile pattern list for expect_list
        compiled_pattern_list = self._child.compile_pattern_list(self._stdout_pattern_list + self._stderr_pattern_list)
        
        # append EOF to compiled pattern list        
        compiled_pattern_list.append(pexpect.EOF)
        eof_index = compiled_pattern_list.index(pexpect.EOF)
        
        # append TIMEOUT to compiled pattern list
        compiled_pattern_list.append(pexpect.TIMEOUT)
        timeout_index = compiled_pattern_list.index(pexpect.TIMEOUT)        
        
        self._starting()

        import re, os

        # expect loop
        patterns_matched = 0
        stdout_patterns_matched = 0
        stderr_patterns_matched = 0
        while True:
#            break
            pattern_index = self._child.expect_list(compiled_pattern_list, searchwindowsize=100, timeout=1)
            if pattern_index == eof_index:
#                if patterns_matched == 0:
#                    if self.child.before != '':
#                        print self.child.before
#                        # scour before for error messages
#                        for line in self.child.before.split(os.linesep):
#                            for i, pattern in enumerate(self._stderr_pattern_list):
#                                if re.match(pattern, line) is not None:
#                                    self._stderr_pattern_matched(len(self._stdout_pattern_list) + i, line)
#                                    break # out of inner for loop
#                            else:
#                                continue # don't break out of outer loop yet
##                            for i, pattern in enumerate(self._stdout_pattern_list):
##                                if re.match(pattern, line) is not None:
##                                    self._stdout_pattern_matched(i, line)
##                                    break # out of inner for loop
##                            else:
##                                continue # don't break out of outer loop yet
#                            break # out of outer for loop
#                        else:
##                            self._stdout_pattern_matched(-1, self.child.before)
#                            print '-1', self.child.before
#                    else:
##                        self.finished_without_output = True #TODO
#                        print 'finished without output'
#                    break # out of while loop
                print 'finished'
                break
                # process has finished, perhaps prematurely, but can't tell so call it a success
            elif pattern_index == timeout_index:
#                self.timed_out = True #TODO
                print 'timed out'
                break
            elif pattern_index in stdout_pattern_range:
                match = self._child.match.group()
                self._stdout_pattern_matched(pattern_index, match)
                stdout_patterns_matched += 1
            elif pattern_index in stderr_pattern_range:
                match = self._child.match.group()
                self._stderr_pattern_matched(pattern_index - len(self._stdout_pattern_list), match)
                stderr_patterns_matched += 1
            else:
                print 'got here'
        
        self._finished()
        
        if stdout_patterns_matched + stderr_patterns_matched == 0:
            print 'finished without output'
#        elif stdout_patterns_matched > 1:
#            print 1
#        elif stderr_patterns_matched > 1:
#            print 2
            
        self._child.close()
        if self._child.exitstatus is not None:
            print 'exitstatus == %s' % self._child.exitstatus
        if self._child.signalstatus is not None:
            print 'signalstatus == %s' % self._child.signalstatus
        print 'status == %s' % self._child.status
        print
        
        
    def _stdout_pattern_matched(self, pattern_index, match):
        if self._interaction_mode not in ('script', 'terminal'):
            self._handler._stdout_pattern_matched(pattern_index, match)
        else:
            if pattern_index == 0:
                print match
            else:
                raise ValueError('Experiment._stdout_pattern_matched called with unrecognised pattern_index %s' % pattern_index)
            
    def _stderr_pattern_matched(self, pattern_index, match):
        if self._interaction_mode not in ('script', 'terminal'):
            self._handler._stderr_pattern_matched(pattern_index, match)
        else:
            if pattern_index == 0:
                print match
            else:
                raise ValueError('Experiment._stderr_pattern_matched called with unrecognised pattern_index %s' % pattern_index)
        

class ExperimentHandler(Controller):

    def _starting(self):
        print 'ExperimentHandler._starting'

    def _finished(self):
        print 'ExperimentHandler._finished'
            
    def _stdout_pattern_matched(self, pattern_index, match):
        if pattern_index == 0:
            print match, 'ExperimentHandler'
        else:
            raise ValueError('ExperimentHandler._stdout_pattern_matched called with unrecognised pattern_index %s' % pattern_index)

    def _stderr_pattern_matched(self, pattern_index, match):
        if pattern_index == 0:
            print match, 'ExperimentHandler'
        else:
            raise ValueError('ExperimentHandler._stderr_pattern_matched called with unrecognised pattern_index %s' % pattern_index)


class DashboardExperimentHandler(ExperimentHandler):

    def _starting(self):
        print 'DashboardExperimentHandler._starting'

    def _finished(self):
        print 'DashboardExperimentHandler._finished'

    def _stdout_pattern_matched(self, pattern_index, match):
        if pattern_index == 0:
            print match, 'DashboardExperimentHandler'
        else:
            raise ValueError('DashboardExperimentHandler._stdout_pattern_matched called with unrecognised pattern_index %s' % pattern_index)

    def _stderr_pattern_matched(self, pattern_index, match):
        if pattern_index == 0:
            print match, 'DashboardExperimentHandler'
        else:
            raise ValueError('DashboardExperimentHandler._stderr_pattern_matched called with unrecognised pattern_index %s' % pattern_index)


class DashboardExperiment(Experiment):
    
    def __handler_default(self):
        return DashboardExperimentHandler(model=self)

#    def _starting(self):
#        print 'DashboardExperiment.starting'
#
#    def _finished(self):
#        print 'DashboardExperiment.finished'

    def _starting(self):
        if self._interaction_mode not in ('script', 'terminal'):
            self._handler._starting()
        else:
            print 'DashboardExperiment._starting'
            self._progress_bar = ProgressBar(
                widgets=[
                    self._command,
                    ' ',
                    Percentage(),
                    ' ',
                    Bar(marker=RotatingMarker()),
                    ' ',
                    ETA()
                ],
                maxval=100,
            )
            self._progress_bar_started = False
    
    def _finished(self):
        if self._interaction_mode not in ('script', 'terminal'):
            self._handler._finished()
        else:
            print 'DashboardExperiment._finished'


def Experiment_perform():
    experiment = Experiment()
    experiment.perform()
    
def DashboardExperiment_perform():
    experiment = DashboardExperiment()
    experiment.perform()
    
def Experiment_gui_perform():
    experiment = Experiment()
    experiment._interaction_mode = 'gui'
    experiment.perform()
    
def DashboardExperiment_gui_perform():
    experiment = DashboardExperiment()
    experiment._interaction_mode = 'gui'
    experiment.perform()

def Experiment_configure():
    experiment = Experiment()
    experiment.configure()
    
def DashboardExperiment_configure():
    experiment = DashboardExperiment()
    experiment.configure()
     

if __name__ == '__main__':
#    Experiment_perform()
#    DashboardExperiment_perform()
#    Experiment_gui_perform()
    DashboardExperiment_gui_perform()
#    Experiment_configure()
#    DashboardExperiment_configure()
    exit(0)
