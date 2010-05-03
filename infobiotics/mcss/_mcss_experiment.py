# This file is part of the Infobiotics Dashboard. See LICENSE for copyright.
# $Id: experiment.py 413 2010-01-26 14:45:50Z jvb $
# $HeadURL: https://psiren.cs.nott.ac.uk/repos/infobiotics/dashboard/trunk/infobiotics/dashboard/plugins/mcss/experiment.py $
# $Author: jvb $
# $Revision: 413 $
# $Date: 2010-01-26 14:45:50 +0000 (Tue, 26 Jan 2010) $

from __future__ import with_statement # not required in Python >=2.6
from infobiotics.common._ets_imports import *
from infobiotics.dashboard.plugins.experiments.params_experiment import *
from mcss_experiment_handler import McssExperimentHandler
import signal
import sys

from infobiotics.dashboard.shared.unified_logging import unified_logging
logger = unified_logging.get_logger('mcss_experiment')

class McssExperiment(ParamsExperiment):

    program = File('/usr/bin/mcss')#, filter=['mcss'], exists=True) #TODO load from preferences using 'name' in ParamsExperiment
#    parameters_name = 'mcss'
    parameter_set_name = 'SimulationParameters'
    handler = McssExperimentHandler

    def _model_file_changed(self, model_file):
        ''' updates model_format so that duplicate_initial_amounts is visible for SBML files even when their extension is XML. '''
        if self.model_file.lower().endswith('.sbml'):
            self.model_format = 'SBML'
        else:
            self.model_format = 'P system XML'
    
    model_file = File('model.lpp', filter=['All model files (*.lpp *.sbml)', 'Lattice population P system files (*.lpp)', 'P system XML files (*.xml)', 'Systems Biology Markup Language files (*.sbml)', 'All files (*)'], desc='the model file to simulate')
    model_format = Trait(
        'P system XML',
        {'P system XML' : 'xml',
         'SBML': 'sbml',
#         'Lattice population P system' : 'lpp',
        },
        desc='the model specification format'
    )
    duplicate_initial_amounts = Bool(False, desc='whether to duplicate initial amounts for all templates in the SBML model')
    just_psystem = Bool(False, desc='whether to just initialise the P system and not perform the simulation')
    max_time = FloatGreaterThanZero(desc='the maximum time to run simulation')
    log_interval = FloatGreaterThanZero(desc='the time interval between which to log data') 
    runs = Long(1, desc='the number of simulation runs to perform')
    data_file = File('simulation.h5', desc='the file to save simulation data to')
    seed = Long(0, desc='the random number seed (0=randomly generated)')
    compress = Bool(True, desc='whether to compress HDF5 output')
    compression_level = Range(0, 9, 9, desc='the HDF5 compression level (0-9; 9=best)')
    simulation_algorithm = Enum(['dmq','dm','ldm','dmgd','dmcp'], desc='the stochastic simulation algorithm to use')

    log_type = Enum(['levels','reactions'], desc='the type of data logging to perform')
    log_memory = Bool(False, desc='whether to log output to memory')
    log_propensities = Bool(False, desc='whether to log reaction propensities')
    log_volumes = Bool(False, desc='whether to log compartment volumes')
    log_steady_state = Bool(True, desc='whether to log up to max_time if steady state reached')
    log_degraded = Bool(False, desc='whether to log levels of degraded species')
    dump = Bool(False, desc='whether to dump model to binary format')
   
    periodic_x = Bool(False, desc='whether the x dimension of the lattice has a periodic boundary condition')
    periodic_y = Bool(False, desc='whether the y dimension of the lattice has a periodic boundary condition')
    periodic_z = Bool(False, desc='whether the z dimension of the lattice has a periodic boundary condition')
    division_direction = Enum(['x','y','z'], desc='the direction of cell division (x,y,z)')
    keep_divisions = Bool(False, desc='whether to keep dividing cells')
    growth_type = Enum(['none','linear','exponential','function'], desc='the volume growth type')
    
    # not in parameter_names
    show_progress = Bool(False, desc='whether to output the current time to screen at each log interval')

    def parameter_names(self):
        return [
            'model_file', 'model_format', 'duplicate_initial_amounts', 
            'just_psystem', 'max_time', 'log_interval', 'runs', 'data_file', 
            'seed', 'compress', 'compression_level', 'show_progress', 
            'simulation_algorithm', 'log_type', 'log_memory', 
            'log_propensities', 'log_volumes', 'log_steady_state', 
            'log_degraded', 'dump', 'periodic_x', 'periodic_y', 'periodic_z',
            'division_direction', 'keep_divisions', 'growth_type' 
        ]
    
    def has_valid_parameters(self): #TODO
        return True

    def perform(self):
        if not self.save(self.file):
            return False #TODO prompt to save if dirty or self.file == ''
#        directory, file = os.path.split(self.file)

        self.progress_meter = self.create_progress_meter(
            title=self.name, # done in Experiment.create_progress_meter()
            text='text',
            max=int(self.max_time if self.runs == 1 else self.runs),
        )
#        print self.progress_meter
        
        if self.is_part_of_application():
            # using TraitsUI within Envisage

            self.progress_meter.start_function = self.start

            experiment_queue = self.application.get_service('infobiotics.dashboard.plugins.experiments.experiment_queue.ExperimentQueue')
            self.progress_meter.hide_function = experiment_queue.hide_function
            
            experiment_queue.experiment_progress_items.append(self.progress_meter)
            
            self.progress_meter.start = True
            
        elif self.is_interactive():
            # using TraitsUI outside Envisage
            self.start()
            self.progress_meter.open()
        else:
            # perform() was called by a script and we can use stdout to report 
            # progress. 
            pass
            raise NotImplementedError('McssExperiment.perform(): self.is_interactive() == False')

    
    def start(self, this=None):
        # create process that runs without blocking interface
        if sys.platform == 'win32':
            args = [self.program, self.file, 'show_progress=true'],
        else:
#            args = [self.program, self.file, 'show_progress=true'] #TODO fix SIGUSR1
            args = [self.program, self.file]
        import subprocess
        self.process = subprocess.Popen(
            args,
            # redirect stdout and stderror from shell to 
            # self.process.stdout and self.process.stderr file-like objects
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            # set subprocess's working directory to os.path.dirname(self.file) 
            cwd=self._cwd, # essential for file parameters with relative paths
#            shell=True,
        )        

        # use intelligent sizehint for self.process.stdout.readlines(sizehint)
#        self.lines_sizehint = int((self.max_time/self.log_interval)/(self.runs/10))
        if self.runs > self.max_time:
            self.lines_sizehint = int(self.runs)
        else:
            self.lines_sizehint = int(self.max_time)
#        self.lines_sizehint = 1000
        
        # choose a polling_interval that is not too long or too short
        polling_interval = 10 # milliseconds
        
        # start a timer to poll the process on its progress
        from enthought.pyface.timer.timer import Timer
        self.timer = Timer(polling_interval, self._poll_process)

        return True
        
    
    def _poll_process(self):
        returncode = self.process.poll()
        if returncode is None:
            # process still running
            
            # check if user has cancelled
            if self.progress_meter.cancelled: 
                # ask process to terminate
                if sys.platform == 'win32':#!= 'linux2': #TODO?
                    self.process.terminate() # == self.process.send_signal(signal.SIGTERM)
                else:
                    # mcss should exit gracefully on Linux with SIGINT
                    os.kill(self.process.pid, signal.SIGINT) # == self.process.send_signal(signal.SIGINT) 
                return
                    
            # ask process to print the current simulation time and run number
            if sys.platform != 'win32':
                os.kill(self.process.pid, signal.SIGUSR1) #TEST
            
            # read last line on stdout within sizehint
            lines = self.process.stdout.readlines(self.lines_sizehint)
            # needs sizehint or we wait to get the whole buffer and progress bar doesn't work
            if lines is not None and len(lines) > 0:
                try:
                    (current_time, current_run) = lines[-1].strip().split(' ')
                    # update progress after converting current_time from str output to int *via* float
                    value = int(float(current_time) if self.runs == 1 else int(float(current_run)))
                    self.progress_meter.update(value)
                except ValueError, e:
                    logger.error(e)
        else:
            # process has finished

            # auto-close progress_meter by updating its progress to max
            self.progress_meter.update(self.max_time if self.runs == 1 else self.runs)
            
            # stop the polling timer
            self.timer.Stop()

            logger.debug(returncode)

            if returncode != 0:
                # there was an error
                # 2 for syntax
                # 1 for other

                lines = self.process.stderr.readlines()
                if lines is not None:
                    logger.error('perform(): mcss returned %s and %s' % (returncode, lines))
                
                #TODO message box if using gui - might not need to check because progress dialog doesn't appear without configure_traits! - can this be guaranteed?

                if returncode == 1:
                    pass
                    
                if returncode == 127:
                    # missing shared library (on Linux only?)
                    print 'shared library error:', 'try "export LD_LIBRARY_PATH=/path/to/libecsb.so.0"'
            
            else:
                # finished successfully
                pass
                #TODO messagebox inviting user to view results
  

if __name__ == '__main__':
    self = McssExperiment()
#    print self.parameter_file_string()
#    os.chdir('/home/jvb/phd/eclipse/infobiotics/dashboard/')
#    self.load('/home/jvb/phd/eclipse/infobiotics/dashboard/examples/pmodelchecker/Const/constitutiveExpressionModel.params')
#    self.configure_traits()
    self.configure()
#    self.edit()
#    self.print_parameters()

