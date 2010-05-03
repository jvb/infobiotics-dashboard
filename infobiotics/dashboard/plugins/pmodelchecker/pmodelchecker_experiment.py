# This file is part of the Infobiotics Dashboard. See LICENSE for copyright.
# $Id: pmodelchecker_experiment.py 414 2010-01-26 16:07:05Z jvb $
# $HeadURL: https://psiren.cs.nott.ac.uk/repos/infobiotics/dashboard/trunk/infobiotics/dashboard/plugins/pmodelchecker/pmodelchecker_experiment.py $
# $Author: jvb $
# $Revision: 414 $
# $Date: 2010-01-26 16:07:05 +0000 (Tue, 26 Jan 2010) $

from __future__ import with_statement # This isn't required in Python 2.6

import os; os.environ['ETS_TOOLKIT']='qt4'
from enthought.traits.api import *#\
#    File, Enum, Long, Str, Float, Directory, Bool, List, Button
from infobiotics.dashboard.plugins.experiments.params_experiment import *
#from infobiotics.dashboard.plugins.pmodelchecker.temporal_formulas import *
from temporal_formulas import *
from infobiotics.dashboard.shared.files import whereis    

from infobiotics.dashboard.shared.unified_logging import unified_logging
logger = unified_logging.get_logger('pmodelchecker_experiment')

from pmodelchecker_experiment_handler import PModelCheckerExperimentHandler

class PModelCheckerExperiment(ParamsExperiment):

#    def handler_default(self): # this doesn't work, we get a ParamsExperimentHandler instead.
#        logger.debug('handler_default')
#        from pmodelchecker_experiment_handler import PModelCheckerExperimentHandler
#        return PModelCheckerExperimentHandler()
#    handler = PModelCheckerExperimentHandler() # this works
    handler = PModelCheckerExperimentHandler #TODO
    
    def _program_default(self):
        #TODO load from preferences
        return '/usr/bin/pmodelchecker'
        
    parameters_name = 'pmodelchecker' # formerly 'Model_checker_parameters'

    def _parameters_set_name_default(self):
        raise NotImplementedError(
            'PModelCheckerExperiment is an abstract base class',
        )

    # PRISMExperiment and MC2Experiment
    model_specification = File(filter=['*.xml','*.lpp'], desc='the filename(.lpp) of the model to check') #TODO have multiple wildcards in one filter?
    model_checker = Enum(['PRISM','MC2'], desc='the name of model checker to use')
    number_samples = Long(desc='the number of simulations to used when approximation is applied')
#
#    # PRISMExperiment
#    PRISM_model = File('PRISM_model.sm', filter=['*.sm','*'],desc='the filename(.sm) of the intermediate PRISM model')
#    temporal_formulas = File(desc='') #TODO MC2-specific? desc
#    formula_parameters = Str(desc='') #TODO PRISM-specific? desc
#    model_parameters = Str('') #TODO desc
#    confidence = Float(0.1, desc='the confidence level used when approximating the answer to a formula')
#    precision = Float(1.0, desc='the precision used when approximating the answer to a formula')
#    results_file = File('results.txt', desc='') #TODO desc
#    states_file = File('states.psm', desc='')  #TODO desc
#    task = Enum(['Approximate','Translate','Build','Verify'], desc='')  #TODO desc
#    transitions_file = File(desc='')  #TODO desc
##    parameters_file = File(desc='a filename for the parameters of the PRISM model')

    # MC2Experiment
    simulations_generatedHDF5 = Bool(False, desc='whether the simulations have already been run')
    simulations_file_hdf5 = File(filter=['*.h5','*'], desc='the filename(.h5) of the simulation')
    simulations_generatedMC2 = Bool(False, desc='whether the TODO have already been run')
    simulations_file_MC2 = File(filter=['*.mc2','*'], desc='the filename(.mc2) of the simulation converted to MC2 format')
    mcss_params_file = File(filters=['*.params'], desc='TODO')

#    def parameters_names(self):
#        return [
#            'model_specification',
#            'model_checker',
#            'number_samples',
#            'formula_parameters',
#            'PRISM_model',
#            'temporal_formulas',
#            'model_parameters',
#            'confidence',
#            'precision',
#            'results_file',
#            'states_file',
#            'task',
#            'transitions_file',
#            'simulations_generatedHDF5',
#            'simulations_file_hdf5',
#            'simulations_generatedMC2',
#            'simulations_file_MC2',
#            'mcss_params_file',
#        ]

    def perform(self):
        
        super(PModelCheckerExperiment, self).perform()
        
        # if dirty save as temporary file
#        '''
#        if self.path can't be read prompt to save,
#        else save current parameters to a temporary file and *compare* to self.path
#            if different prompt to save 
#            else continue without prompt
#        TODO factor this into Experiment.perform()
#        '''
#
#        try:
#            open(self.path, 'r')
#            
#            path = self.path
#            from tempfile import NamedTemporaryFile
#            temporary_file = NamedTemporaryFile()
#            self.save(temporary_file.name)
#            self.path = path
#        except IOError:
#            self.save() # updates self.path
            
        #TODO don't ignore above
        self.save(self.file)

        cwd = os.path.dirname(self.file)
        filename = os.path.basename(self.file) # absolutely necessary
        
        program = os.path.basename(self.program) # 'pmodelchecker'
        
        print whereis(program) #TODO remove
        if whereis(program) is None:
            print program, 'not found, aborting'
            return
        
#        with open(os.path.join(cwd, filename), 'r') as fh: print fh.read(), '\n' 
        
        filename = os.path.join(cwd, filename)
    
        args = [program, filename]

#        print program, filename, cwd, os.path.join(cwd, filename)
#        exit()
        
#    try:
        import subprocess
        self.process = subprocess.Popen(args,
            #TODO reinstate 2 of these
#            stdout=subprocess.PIPE,
#            stderr=subprocess.PIPE,
#            stderr=subprocess.STDOUT,
            cwd=cwd,
        )
        
        # choose a polling_interval that is not too long or too short
        polling_interval = 100 # milliseconds
        
        # start a timer to poll the process on its progress
        from enthought.pyface.timer.timer import Timer
        self.timer = Timer(polling_interval, self._poll_process)                
        
#    except OSError, e:
#        sys.stderr.write(e)
#    except ValueError, e:
#        sys.stderr.write(e)
    
    def _poll_process(self):
        if not hasattr(self, 'process'):
            return
        if self.process is None:
            return
        process = self.process
        
        return_code = process.poll()
#        print 'return_code =', return_code
    
        if return_code is not None:
            # process has finished
    
            if process.stderr is not None:
                stderr = process.stderr.readlines()
                if stderr is not None and len(stderr) > 0:
                    sys.stderr.writelines(stderr)
                    if stderr[0].startswith('Exception in thread "main" java'):
                        print 'PRISM is not compatible with this version of Java, \ntry running outside of eclipse.'
#                        break
                    print len(stderr), '*'
            
            if process.stdout is not None:
                stdout = process.stdout.readlines()
                if stdout is not None and len(stdout) > 0:
                    sys.stdout.writelines(stdout)
                    print len(stdout), '*'
            
#            print '%s returned %s' % (program, return_code)
            print 'pmodelchecker returned %s' % return_code
            if return_code == -6:
                '''
                Generating simulations in MC2 format
                pmodelchecker: /usr/local/include/ecsb/Misc.h:49: T ECSB::fromStringTo(const std::string&) [with T = double]: Assertion `stream >> result' failed.
                pmodelchecker returned -6
                possible incorrect cwd or filename
                '''
#                print 'possible incorrect cwd: %s; or filename: %s' % (cwd, filename)
                print 'possible incorrect cwd or filename'
    #        if return_code == -11:
    #            print 'possible missing libraries, check LD_LIBRARY_PATH'
            
            self.timer.Stop()
            self.process = None        
    
        else:
            # process still running
    
    #        pass
            if process.stderr is not None:
                stderr = process.stderr.readlines()
                if stderr is not None and len(stderr) > 0:
                    sys.stderr.writelines(stderr)
                    if stderr[0].startswith('Exception in thread "main" java'):
                        print 'PRISM is not compatible with this version of Java, \ntry running outside of eclipse.'
                    print len(stderr), '*'
            
            if process.stdout is not None:
                stdout = process.stdout.readlines()
                if stdout is not None and len(stdout) > 0:
                    sys.stdout.writelines(stdout)
                    print len(stdout), '*'
    #        process.stderr.flush()
    #        process.stdout.flush()
    
#    def _poll_process(self):
#
#        returncode = self.process.poll()
#
#        if returncode is None:
#            # process still running
#
#            # don't read all the output in one go by specifying a sizehint
##            lines = self.process.stdout.readlines(self.lines_sizehint)
#            lines = self.process.stdout.readlines()
#            for line in lines:
#                print line
#            
#        else:
#            print returncode
#            
#            # process has finished
#
#            if returncode > 0:
#                # there was an error
#
#                error_message = self.process.stderr.readlines()
#
#                if returncode == 1:
#                    # failed
#                    
#                    pass
#                    print 'failed:', error_message 
#                    #TODO message box if using gui
#                    
#                if returncode == 127:
#                    # missing shared library (on Linux only?)
#                    
#                    pass
#                    print 'failed:', error_message 
#                    print 'shared library error:', 'try "export LD_LIBRARY_PATH=/path/to/libecsb.so.0"'
#                    #TODO message box if using gui
#            
#            else:
#                print 'finished'
#                
#            # stop the polling timer
##            self.timer.Stop()

    _temporal_formulas_list = List(TemporalFormula)
    _add_temporal_formula = Button
    _edit_temporal_formula = Button
    _remove_temporal_formula = Button
    selected_temporal_formula = Instance(TemporalFormula)


if __name__ == '__main__':
#    execfile('prism_experiment.py')
    execfile('mc2_experiment.py')
