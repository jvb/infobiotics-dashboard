from pmodelchecker_params import PModelCheckerParams

class MC2Params(PModelCheckerParams):
    
    _parameter_set_name = 'mc2'
    
    model_checker = 'MC2'
    
    def parameter_names(self):
        ''' Returns the subset of PModelChecker parameter names required for a 
        PModelChecker experiment with MC2.
        
        '''
        if self.simulations_generatedHDF5:
            return [
                'model_specification',
                'model_checker',
                'temporal_formulas',
                'number_samples',
                'results_file',
                'simulations_generatedHDF5',
                'simulations_file_hdf5',
                'simulations_generatedMC2',
                'simulations_file_MC2',
            ]
        else:
            return [
                'model_specification',
                'model_checker',
                'temporal_formulas',
                'number_samples',
                'results_file',
                'simulations_generatedHDF5',
                'simulations_file_hdf5',
                'simulations_generatedMC2',
                'simulations_file_MC2',
                'mcss_params_file',
            ]

    def has_valid_parameters(self):
        '''
        
        
        example:
            from infobiotics.dashboard.shared.files import can_read, can_write
        
            # test
            if not can_read(self.<file>):
                # failed
                self.problem = "The file specified by '<file>' ('%s') cannot be read." % self.<file>
                return False
            else:
                #succeeded
                pass
                # further tests

        '''
        
        from infobiotics.dashboard.shared.files import can_read, can_write
        
        if not can_read(self.model_specification):
            self.problem = "The file specified by 'model_specification' ('%s') cannot be read." % self.model_specification
            return False
        else:
            # further tests
            pass
            #TODO try and parse model_specification

        #TODO temporal_formulas
        
        #TODO formula_parameters
        
        #TODO number_samples
        
        if self.simulations_generatedMC2:
            if not can_read(self.simulations_file_MC2):
                self.problem = "The file specified by 'simulations_file_MC2' ('%s') cannot be read." % self.simulations_file_MC2
                return False
        elif self.simulations_generatedHDF5:
            if not can_read(self.simulations_file_HDF5):
                self.problem = "The file specified by 'simulations_file_HDF5' ('%s') cannot be read." % self.simulations_file_HDF5
                return False

        if not self.simulations_generatedHDF5 and not self.simulations_generatedMC2:
            if not can_read(self.mcss_params_file):
                self.problem = "The file specified by 'mcss_params_file' ('%s') cannot be read." % self.mcss_params_file
                return False
        
        if not can_write(self.temporal_formulas):
            self.problem = "'%s' cannot be written." % self.temporal_formulas
            return False
        
        # reset problem and return true
        self.problem = ''
        return True

    def perform(self):
        
#        if not has_parameters():
#            if not application...:
#                print self.problem #TODO
#                return False
        
        print self.mcss_params_file
        print self._mcss_experiment.file #TEST when mcss_params_file exists, changes are made to _mcss_experiment
        
        if not self.simulations_generatedHDF5:
            # save mcss_params_file with absolute path
            # save _mcss_experiment.file with absolute path
            pass 
            
        # write temporal formulas to file #TODO repeat for PRISMExperiment
        with open(self.temporal_formulas, 'w') as temporal_formulas_file:
            '''
            Formulas:
            "P=?[ (Time=1000)U([protein1_(0,0)] >= B ^ [protein1_(0,0)] < B + 5){Time=1000}]" {B =0:10:300}
            "P=?[ (Time=R*10)U([protein1_(0,0)] >= 50){Time=R*10}]" {R = 0:20:200}
            '''
            lines = ['Formulas:\n']
            for temporal_formula in self._temporal_formulas_list:
                line = '"%s"' % temporal_formula.formula
                line += ' {'
                for i, parameter in enumerate(temporal_formula.parameters):
                    if i != 0:
                        line += ', ' 
                    line += '%s=%s:%s:%s' % (parameter.name, parameter.lower_bound, parameter.step, parameter.upper_bound)
                line += '}'
#                line += ' ' 
                line += '\n'             
                lines += line                        
            temporal_formulas_file.writelines(lines)
            # with auto-closes file here at end of it's suite
        
        super(MC2Experiment, self).perform()

    def _simulations_file_hdf5_changed(self, file):
        ''' Tries to extract 'number_of_runs' from 'simulations_file_hdf5'.  
        

        '''
        from infobiotics.dashboard.shared.files import can_read, can_write
        
        # test if 'model_specification' can be read
        if can_read(self.simulations_file_hdf5) and self.simulations_generatedHDF5:
            with tables.openFile(self.simulations_file_hdf5, 'r') as file:
                if not file.root._v_attrs.__contains__('mcss_version'):
                    raise ValueError('%s is not an mcss simulation file' % file)
                self.number_of_runs = int(file.root._v_attrs.number_of_runs)
                
                #TODO use to make number_of_samples a range from 1 to 'number_of_runs'
        
#    #TODO remove these because they work but UI doesn't refresh!
#    def _simulations_generatedHDF5_changed(self):
#        if self.simulations_generatedHDF5:
#            self.trait('simulations_file_hdf5').handler.exists = True
#        else:
#            self.trait('simulations_file_hdf5').handler.exists = False
#    def _simulations_generatedMC2_changed(self):
#        if self.simulations_generatedMC2:
#            self.trait('simulations_file_MC2').handler.exists = True
#        else:
#            self.trait('simulations_file_MC2').handler.exists = False

    _number_samples_for_mc2_when_simulation_file_supplied = Range('_min_number_samples', '_max_number_samples', desc='the number of simulations to use when approximation is applied')
    _min_number_samples = Int(1)
    _max_number_samples = Property(depends_on='_number_of_runs')
    _number_of_runs = Int(1)
    #TODO show/hide number_samples in favour of _number_samples_for_mc2_when_simulation_file_supplied in mc2_group
    def _get__max_number_samples(self):
        return self._number_of_runs

    def _temporal_formulas_changed(self):
        from infobiotics.dashboard.shared.files import can_read
        if not can_read(self.temporal_formulas):
            return
        try:
            with open(self.temporal_formulas, 'r') as f: 
                lines = f.readlines()
                if lines[0].strip() != 'Formulas:':
                    return
                else:
                    del self._temporal_formulas_list[:] # clear list
                    for line in lines[1:]:
                        line = line.strip()
                        if len(line) != 0:
                            first = line.find('"')
                            second = line.find('"', first+1)
                            formula = line[first+1:second]
                            parameters_start = line.find('{', second+1)
                            parameters_end = line.find('}', parameters_start+1)
                            #{B=0:10:300,R=1:1:10}
                            parameters = line[parameters_start+1:parameters_end]
                            parameters_list = []
                            for parameter in parameters.split(','):
#                                print parameter
                                name_and_values = parameter.split('=')
                                name = name_and_values[0]
                                values = name_and_values[1].split(':')
                                lower = values[0]
                                step = values[1]
                                upper = values[2]
#                                print '{%s=%s:%s:%s}' % (name, lower, step, upper)
                                parameters_list.append(TemporalFormulaParameter(name=name, lower_bound=float(lower), step=float(step), upper_bound=float(upper)))

                            temporal_formula = TemporalFormula(formula=formula, parameters=parameters_list)
                            self._temporal_formulas_list.append(temporal_formula)
                                
        except IOError, e:
            logger.error('%s, _temporal_formulas_changed()' % e)

    def __temporal_formulas_list_items_changed(self):
        ''' Refreshes _temporal_formulas_list.
        
        '''
        _temporal_formulas_list = self._temporal_formulas_list
        self._temporal_formulas_list = []
        self._temporal_formulas_list = _temporal_formulas_list
        
    _mcss_experiment = Instance(McssExperiment, McssExperiment())
    
    # update mcss experiment from start, can't think of a better way to do it!
    def __init__(self, *args, **kwargs):
        super(MC2Experiment, self).__init__(*args, **kwargs)
        self._update_mcss_experiment()
    
    @on_trait_change('_mcss_experiment, model_specification, number_samples, simulations_file_hdf5')
    def _update_mcss_experiment(self):
        self._mcss_experiment.model_file = self.model_specification
        self._mcss_experiment.data_file = self.simulations_file_hdf5
        self._mcss_experiment.runs = self.number_samples
        # replace parameter_names function in _mcss_experiment with function that returns reduced list of parameter names
        def parameter_names():
            return [
                # set by MC2Experiment.TODO
                'model_file',
                # set by McssExperiment._model_file_changed()
                'model_format',
                # edited by user
                'duplicate_initial_amounts',
                'max_time',
                'log_interval',
                'compress',
                'compression_level',
                'simulation_algorithm',
                'seed',
                'periodic_x',
                'periodic_y',
                'periodic_z',
                'division_direction',
                'keep_divisions',
                'growth_type',
                'log_type',
                'log_propensities',
                'log_volumes',
                'log_steady_state',
                'log_degraded',
                # not edited by user
                'just_psystem',
            ]
        self._mcss_experiment.parameter_names = parameter_names

    def _mcss_params_file_changed(self, mcss_params_file):
        _mcss_experiment = McssExperiment()
        _mcss_experiment.load(mcss_params_file)
        self._mcss_experiment = _mcss_experiment

    _edit__mcss_experiment = Button(label='Edit')
    
    def __edit__mcss_experiment_fired(self):
        self._mcss_experiment.edit_traits(kind='nonmodal',
            view=View(
                mcss_experiment_parameters_group, # see below
                buttons=['Cancel', 'Undo', 'OK'] + ParamsExperiment.load_save_actions,
                handler=ParamsExperimentHandler(),
                resizable=True,
                title='Edit mcss experiment',
            ),
        )

mcss_experiment_parameters_group = Group(
    VGroup(
        Item('model_file', style='readonly'),
        Item('model_format', visible_when='object.model_file.endswith(".xml")', label='XML type'),
#        Item('just_psystem', visible_when='object.model_format=="xml" or object.model_file.lower().endswith(".psxml")', label='Just initialise P system'),
        Item('duplicate_initial_amounts', visible_when='object.model_format=="SBML" or object.model_file.lower().endswith(".sbml")'),
        Item('max_time'),
        Item('log_interval'),
        Item('runs', style='readonly'),
        Item('data_file', style='readonly'),
#        Item('show_progress'),# not needed when using GUI
        Item('compress', label='Compress output'),
        Item('compression_level', visible_when='object.compress==True'),
        Item('simulation_algorithm'),
        Item('seed', label='Random seed'),
#        label='Required'
    ),
#    
#    VGroup(
#        Item('periodic_x', label='Periodic X dimension'),
#        Item('periodic_y', label='Periodic Y dimension'),
#        Item('periodic_z', label='Periodic Z dimension'),
#        Item('division_direction', label='Direction of cell division'),
#        Item('keep_divisions', label='Keep dividing cells'),
#        Item('growth_type', label='Volume growth type'),
#        label='Spatial'
#    ),
#    
#    VGroup(
#        Item('log_type', label='logging type'),
#        Item('log_propensities', visible_when='object.log_type == "reactions"'),
#        Item('log_volumes'),
#        Item('log_steady_state'),
#        Item('log_degraded'),
##        Item('log_memory', label='log output to memory'),
##        Item('dump'),
#        label='Logging'
#    ),
           
    VGroup(
         Item('program', label='Path to mcss'),
         label='mcss'
    ),
    layout='tabbed'
)        
    
mc2_group = Group(
    
    Item('model_specification'),
    
    VGroup(
        HGroup(
            Item('simulations_file_hdf5', label='mcss simulation file', enabled_when='object.simulations_generatedMC2 != True'),
            Item('simulations_generatedHDF5', label='Simulated?', enabled_when='object.simulations_generatedMC2 != True'),
        ),
        HGroup(
            Item('mcss_params_file', label='mcss parameters file', enabled_when='object.simulations_generatedHDF5 != True and object.simulations_generatedMC2 != True'),
            Item('_edit__mcss_experiment', show_label=False, enabled_when='object.simulations_generatedHDF5 != True and object.simulations_generatedMC2 != True'),
        ),
        HGroup(
               Item('simulations_file_MC2', label='MC2 input file'),
               Item('simulations_generatedMC2', label='Generated?'),
        ),
        Item('number_samples', 
            label='Number of samples', 
#            enabled_when='object.simulations_generatedMC2 != True'
        ),
        label='Simulation data',
    ),

    temporal_formulas_group,   
    
    Item('results_file'),
)