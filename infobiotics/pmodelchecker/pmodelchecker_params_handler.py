from infobiotics.shared.api import ParamsHandler, List, Button, Instance
from infobiotics.pmodelchecker.api import TemporalFormula

class PModelCheckerParamsHandler(ParamsHandler):
    ''' Contains common parameter traits that should not be specified in 
    PModelCheckerParams. '''
    
    _temporal_formulas_list = List(TemporalFormula)
    _add_temporal_formula = Button
    _edit_temporal_formula = Button
    _remove_temporal_formula = Button
    selected_temporal_formula = Instance(TemporalFormula)
    
    def _add_temporal_formula_changed(self, info): # changed works, even for a button
        formula = TemporalFormula()
        formula.edit_traits(kind='modal')
#        # only add formulas with new parameters 
#        for temporal_formula in self._temporal_formulas_list:
#            if temporal_formula == formula:
#                return
        self._temporal_formulas_list.append(formula)
        
    def _edit_temporal_formula_changed(self, info):
        formula = self.selected_temporal_formula
        if formula is not None:
            formula.edit_traits(kind='modal')
        
    def _remove_temporal_formula_changed(self, info):
        formula = self.selected_temporal_formula
        if formula is not None:
            self._temporal_formulas_list.remove(formula)
            self.selected_temporal_formula = None
    