# This file is part of the Infobiotics Workbench. See LICENSE for copyright.
# $Id: __init__.py 286 2009-08-25 17:51:05Z jvb $
# $HeadURL: https://psiren.cs.nott.ac.uk/repos/infobiotics/gui-current/trunk/src/metamodel/__init__.py $
# $Author: jvb $
# $Revision: 286 $
# $Date: 2009-08-25 18:51:05 +0100 (Tue, 25 Aug 2009) $

import os; os.environ['ETS_TOOLKIT']='qt4'
from infobiotics.dashboard.plugins.experiments.params_experiment_handler import ParamsExperimentHandler

from infobiotics.dashboard.shared.unified_logging import unified_logging
logger = unified_logging.get_logger('pmodelchecker_experiment_handler')

#from infobiotics.dashboard.plugins.pmodelchecker.temporal_formulas import *
from temporal_formulas import *

from enthought.traits.api import Button

class PModelCheckerExperimentHandler(ParamsExperimentHandler):
    
#    def __init__(self, *args, **kwargs):
#        print 'PModelCheckerExperimentHandler was created'
#        super(PModelCheckerExperimentHandler, self).__init__(*args, **kwargs)

#    def closed(self, info, is_ok):
#        print 'PModelCheckerExperimentHandler was closed'
#        super(PModelCheckerExperimentHandler, self).closed(info, is_ok)

#    def load(self, info): #test whether this overrides ParamsExperimentHandler.load()...it does.
#        pass
    
#    def object__add_temporal_formula_fired(self, info): # fired doesn't work, even for a button
#        logger.debug('object__add_temporal_formula_fired')
    def object__add_temporal_formula_changed(self, info): # changed works, even for a button
        formula = TemporalFormula()
        formula.edit_traits(kind='modal')
#        # only add formulas with new parameters 
#        for temporal_formula in self._temporal_formulas_list:
#            if temporal_formula == formula:
#                return
        info.object._temporal_formulas_list.append(formula)
        
    def object__edit_temporal_formula_changed(self, info):
        formula = info.object.selected_temporal_formula
        if formula is not None:
            formula.edit_traits(kind='modal')
        
    def object__remove_temporal_formula_changed(self, info):
        formula = info.object.selected_temporal_formula
        if formula is not None:
            info.object._temporal_formulas_list.remove(formula)
            info.object.selected_temporal_formula = None
   
#    def object__temporal_formulas_changed(self, info):
#        raise NotImplementedError('object__temporal_formulas_changed')             

#    #TEST event trait on handler (see temporal_formulas.temporal_formulas_group)
#    dclick = Button
#    def _dclick_fired(self):
#        print 'dclick'

    #TEST setattr
    def setattr(self, info, object, name, value):
        super(PModelCheckerExperimentHandler, self).setattr(info, object, name, value)
#        print object, name, value
        info.object._dirty = True
    def object__dirty_changed(self, info):
        info.ui.title += '*'

#    def object_edit__mcss_experiment_changed(self, info):
#        if info.initialized:
#            _mcss_experiment = info.object._mcss_experiment 
#            if _mcss_experiment is None:
#                _mcss_experiment = McssExperiment()
#            _mcss_experiment.edit_traits(kind='modal')#TODO view=
#    # done in MC2Experiment.__edit_mcss_experiment_fired() for some reason?
                   

if __name__ == '__main__':
    execfile('pmodelchecker_experiment.py')
    