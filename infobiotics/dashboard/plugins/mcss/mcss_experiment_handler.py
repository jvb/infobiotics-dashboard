# This file is part of the Infobiotics Workbench. See LICENSE for copyright.
# $Id: __init__.py 286 2009-08-25 17:51:05Z jvb $
# $HeadURL: https://psiren.cs.nott.ac.uk/repos/infobiotics/gui-current/trunk/src/metamodel/__init__.py $
# $Author: jvb $
# $Revision: 286 $
# $Date: 2009-08-25 18:51:05 +0100 (Tue, 25 Aug 2009) $

import os; os.environ['ETS_TOOLKIT']='qt4'
from infobiotics.dashboard.plugins.experiments.params_experiment_handler import ParamsExperimentHandler

from infobiotics.dashboard.shared.unified_logging import unified_logging
logger = unified_logging.get_logger('mcss_experiment_handler')

from enthought.traits.ui.api import View, Item, Group, VGroup, TextEditor

class McssExperimentHandler(ParamsExperimentHandler):

    title = 'mcss'
        
    def _group_default(self):
#        from mcss_group import group
#        return group
        return Group(
            VGroup(
                Item('model_file'),
                Item('model_format', 
                    label='XML type',
                    visible_when='object.model_file.endswith(".xml")',
                ),
                Item('just_psystem', visible_when='object.model_format=="xml"', label='Just initialise P system'),
                Item('duplicate_initial_amounts', visible_when='object.model_format=="SBML" or object.model_file.lower().endswith(".sbml")'),
                Item('max_time'),
                Item('log_interval'),
                Item('runs'),
                Item('data_file'),
#                Item('show_progress'), #TODO popup showing stdout and stderr for each params program
                Item('compress', label='Compress output'),
                Item('compression_level', visible_when='object.compress==True'),
                Item('simulation_algorithm'),
                Item('seed', label='Random seed'),
                label='Required'
            ),
            
            VGroup(
                Item('periodic_x', label='Periodic X dimension'),
                Item('periodic_y', label='Periodic Y dimension'),
                Item('periodic_z', label='Periodic Z dimension'),
                Item('division_direction', label='Direction of cell division'),
                Item('keep_divisions', label='Keep dividing cells'),
                Item('growth_type', label='Volume growth type'),
                label='Spatial'
            ),
            
            VGroup(
                Item('log_type', label='logging type'),
                Item('log_propensities', visible_when='object.log_type == "reactions"'),
                Item('log_volumes'),
                Item('log_steady_state'),
                Item('log_degraded'),
                Item('log_memory', label='log output to memory'),
                Item('dump'),
                label='Logging'
            ),
            
            VGroup(
                Item(label='Copy and paste the script below to reproduce this experiment.'),
                Item('repr', show_label=False, style='custom', editor=TextEditor()), #TODO
                label='script',
            ),
            
            layout='tabbed'
        )

    
if __name__ == '__main__':
    execfile('mcss_experiment.py')
    