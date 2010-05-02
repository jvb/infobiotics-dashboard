from infobiotics.pmodelchecker.mc2.api import MC2ParamsHandler, MC2ExperimentProgressHandler
from infobiotics.common.api import ExperimentHandler

class MC2ExperimentHandler(MC2ParamsHandler, ExperimentHandler):

    _progress_handler = MC2ExperimentProgressHandler 

#    def has_valid_parameters(self):
#        '''
#        
#        
#        example:
#            from infobiotics.dashboard.shared.files import can_read, can_write
#        
#            # test
#            if not can_read(self.<file>):
#                # failed
#                self.problem = "The file specified by '<file>' ('%s') cannot be read." % self.<file>
#                return False
#            else:
#                #succeeded
#                pass
#                # further tests
#
#        '''
#        
#        from infobiotics.dashboard.shared.files import can_read, can_write
#        
#        if not can_read(self.model_specification):
#            self.problem = "The file specified by 'model_specification' ('%s') cannot be read." % self.model_specification
#            return False
#        else:
#            # further tests
#            pass
#            #TODO try and parse model_specification
#
#        #TODO temporal_formulas
#        
#        #TODO formula_parameters
#        
#        #TODO number_samples
#        
#        if self.simulations_generatedMC2:
#            if not can_read(self.simulations_file_MC2):
#                self.problem = "The file specified by 'simulations_file_MC2' ('%s') cannot be read." % self.simulations_file_MC2
#                return False
#        elif self.simulations_generatedHDF5:
#            if not can_read(self.simulations_file_HDF5):
#                self.problem = "The file specified by 'simulations_file_HDF5' ('%s') cannot be read." % self.simulations_file_HDF5
#                return False
#
#        if not self.simulations_generatedHDF5 and not self.simulations_generatedMC2:
#            if not can_read(self.mcss_params_file):
#                self.problem = "The file specified by 'mcss_params_file' ('%s') cannot be read." % self.mcss_params_file
#                return False
#        
#        if not can_write(self.temporal_formulas):
#            self.problem = "'%s' cannot be written." % self.temporal_formulas
#            return False
#        
#        # reset problem and return true
#        self.problem = ''
#        return True

#    def perform(self):
#        if not self.simulations_generatedHDF5:
#            # save mcss_params_file with absolute path
#            # save _mcss_experiment.file with absolute path
#            pass 
#        pass
#        super(MC2Experiment, self).perform()


if __name__ == '__main__':
    execfile('mc2_experiment.py')
    