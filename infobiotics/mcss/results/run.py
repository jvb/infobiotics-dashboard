class Run(object): #TODO rename McssRun

    def __init__(self, attributes, run_number, simulation):
        self._run_number = run_number
        self._simulation = simulation
        self._compartments_list = []
#        self.main_loop_end_time = attributes.main_loop_end_time
#        self.main_loop_start_time = attributes.main_loop_start_time
        self.number_of_compartments = attributes.number_of_compartments
        self.number_of_timepoints = attributes.number_of_timepoints
#        self.preprocess_end_time = attributes.preprocess_end_time
#        self.preprocess_start_time = attributes.preprocess_start_time
#        self.run_end_time = attributes.run_end_time
#        self.run_start_time = attributes.run_start_time
        self.simulated_time = attributes.simulated_time
#        self.total_reactions_simulated = attributes.total_reactions_simulated
