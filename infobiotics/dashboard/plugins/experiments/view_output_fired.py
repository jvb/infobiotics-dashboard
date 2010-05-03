'''
An experiment is 'performed', 
a process is started, 
the process is polled,
its output is displayed. 


'''

import subprocess
import os
os.environ['ETS_TOOLKIT']='qt4'
from enthought.traits.api import *
from enthought.traits.ui.api import *
from enthought.traits.ui.menu import *
import tempfile


# Handles perform_action button click    
class ParamsExperimentHandler(Handler):
    
    perform_action = Action(name='Perform', action='perform')
    def perform(self, info):
        info.object.perform()

    traits_view = View(
        buttons=[perform_action],
        title='ParamsExperimentHandler',
    )

#TODO should each perform spawn a new process and progress meter?
    
# starts a process and creates a progress meter
class ParamsExperiment(HasTraits):

    def start(self, stdout_path):
        args = ['less', 'view_output_fired.py']
        args = ['./count_to_ten.py']
        self.process = subprocess.Popen(
            args,
            # redirect stdout and stderror from shell to 
            # self.process.stdout and self.process.stderr file-like objects
#            stdout=subprocess.PIPE,
            stdout=open(stdout_path,'w'),
#            stderr=subprocess.PIPE,
            # set subprocess's working directory to os.path.dirname(self.file) 
#            cwd=self._cwd, # essential for file parameters with relative paths
#            shell=True,
        )
        print self.process.stdout
        return True

    def perform(self):
        self.progress = ExperimentProgressItem(
            start_function=self.start,
            experiment=self,
        )
        result = self.progress.edit_traits(kind='modal')

#TODO use process.stdout as file instead of temporary file

#TODO exp1 == exp2 using parameter_names

# shows the progress of the process
class ExperimentProgressItem(HasTraits):

    experiment = ParamsExperiment

    stdout_path = File
    def _stdout_path_default(self):
        self.stdout_file = tempfile.NamedTemporaryFile()
        return self.stdout_file.name

    start_function = Callable(lambda self: True)
    started = Bool(False)
    start = Button
    def _start_fired(self):
        started = self.start_function(self.stdout_path)

    view_output = Button
    def _view_output_fired(self):
#        with open(self.stdout_path) as stdout:
        with self.stdout_file as stdout:
            self.stdout_str = ''.join(stdout.readlines())

    stdout_str = Str
            
    view = View(
        Item('start', enabled_when='object.started == False'),
        'view_output',
        Item('stdout_path'),
        Item('stdout_str', editor=TextEditor(), style='custom'),
#        resizable=True,
        scrollable=True,
        title='ExperimentProgressItem',
    )
    
if __name__ == '__main__':
    experiment = ParamsExperiment()
    handler = ParamsExperimentHandler()
    handler.configure_traits(context={'object':experiment})