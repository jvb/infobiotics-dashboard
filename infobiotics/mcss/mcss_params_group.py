from traitsui.api import Group, VGroup, Item, HGroup, Spring, EnumEditor#, TextEditor
from infobiotics.commons.traits_.ui.values_for_enum_editor import values_for_EnumEditor
from infobiotics.mcss.mcss_params_handler import dmq2, dm#, ode1#default_model_format, default_simulation_algorithm, default_ode_solver, default_neighbourhood 

mcss_params_group = Group(
    VGroup(
        VGroup(
            VGroup(
                VGroup(
                    Item('model_file'),
                    HGroup(
                        Item('handler.model_format',
                            label='XML type',
                            visible_when='object.model_file.endswith(".xml")',
                        ),
#                        Item('just_psystem', visible_when='handler.model_format_ != "sbml"', label='Just initialise P system'),
                        Item('duplicate_initial_amounts', visible_when='handler.model_format_ == "sbml"'),
                    ),
                    label='P system model',
                ),
                VGroup(
                    Item('data_file'),
                    Item('max_time'),
                    Item('log_interval'),

				    #Item('handler.simulation_algorithm'),
				    Item('handler.simulation_algorithm_type', label='Type', style='custom'),

					Item('handler.simulation_algorithm',
						editor=EnumEditor(
							values=values_for_EnumEditor([dmq2, dm]),
						),
						label='SSA',
						visible_when='handler.simulation_algorithm_type=="stochastic-discrete"',#object.simulation_algorithm!="ode1"'),
					),
                    Item('seed', label='Seed', visible_when='handler.simulation_algorithm_type=="stochastic-discrete"'),#enabled_when='object.simulation_algorithm!="ode1"'),							
					Item('runs', visible_when='handler.simulation_algorithm_type=="stochastic-discrete"'),#visible_when='object.simulation_algorithm!="ode1"'),

                    Item('handler.ode_solver', label='ODE solver', visible_when='handler.simulation_algorithm_type=="deterministic-continuous"'),#object.simulation_algorithm!="ode1"'),
				    
                    label='Simulation',
                ),
                label='Input'
            ),
        
            VGroup(

                VGroup(
    #                Item('log_type', label='Logging type'),
    #                Item('log_propensities', enabled_when='object.log_type == "reactions"'),
    #                Item('log_volumes'),
                    Item('log_steady_state'),
                    Item('log_degraded'),
    #                Item('log_memory', label='Log output to memory'),
                    HGroup(
                        Item('compress', label='Compress data'),
                        Item('compression_level', label='Level', enabled_when='object.compress==True'),
                    ),
                    label='Output'
                ),
                
#                HGroup(
                VGroup(
                    Item('handler.neighbourhood', label='Neighbourhood'),
#                    Item('periodic_x', label='Periodic X dimension'),
#                    Item('periodic_y', label='Periodic Y dimension'),
#                	 Item('periodic_z', label='Periodic Z dimension'),
                    HGroup(
                    Item(label='Periodic boundary conditions for dimensions:'),
	                    Item('periodic_x', label='X'),
	                    Item('periodic_y', label='Y'),
#	                    Item('periodic_z', label='Z'),
                    ),
    #                Item('division_direction', label='Direction of cell division'),
    #                Item('keep_divisions', label='Keep dividing cells'),
    #                Item('growth_type', label='Volume growth type'),
                    label='Lattice'
                ),
#				),

				VGroup(
					Item('max_runtime'),
					label='Additional stopping criteria',
				),

                label='Optional',
            ),
               
        #    VGroup(
        #        Item(label='Copy and paste the script below to reproduce this experiment.'),
        #        Item('repr', show_label=False, style='custom', editor=TextEditor()), #TODO
        #        label='script',
        #    ),
            
            layout='tabbed',
        ),
    ),
    Spring(),
)


if __name__ == '__main__':
    execfile('mcss_params.py')
    
