from __future__ import with_statement
from infobiotics.commons.api import read, write
from infobiotics.core.params_handler import ParamsHandler
from enthought.traits.api import List, Unicode, Button, Instance, Enum, on_trait_change, Str, DelegatesTo
from model_parameters import ModelParameters
from temporal_formulas import TemporalFormula, TemporalFormulaParameter
import os.path

class PModelCheckerParamsHandler(ParamsHandler):
    ''' Traits shared by PRISMParamsHandler and MC2ParamsHandler. '''

    task = Enum(['Approximate', 'Build', 'Verify'], desc="the task to perform:\n'Approximate' or 'Verify' the input properties\n'Build' the corresponding Markov chain")
    
    temporal_formulas = List(TemporalFormula)
    selected_temporal_formula = Instance(TemporalFormula)
    add_temporal_formula = Button
    edit_temporal_formula = Button
    remove_temporal_formula = Button
    default_temporal_formula = Str

    model_parameters_object = Instance(ModelParameters)
    model_parameter_names = List(Unicode) # used in TemporalFormula for model_parameter_name_to_insert Enum
    model_parameters = DelegatesTo('model_parameters_object') # i.e. self.model_parameters_object.model_parameters
    
    def init(self, info): 
        super(PModelCheckerParamsHandler, self).init(info)
        self.sync_trait('task', info.object, mutual=False) # see POptimizerParamsHandler.init()
        self.forward_changes_in_model_to_model_parameters()

    def load(self, info):
        super(PModelCheckerParamsHandler, self).load(info)
        self.forward_changes_in_model_to_model_parameters()

    def forward_changes_in_model_to_model_parameters(self):
        '''The reverse of forward_changes_in_model_parameters_to_model.'''
        if self.model_parameters_object is not None:
            self.model_parameters_object.model_parameters = self.model.model_parameters

    @on_trait_change('model_parameters')
    def forward_changes_in_model_parameters_to_model(self):
        self.model.model_parameters = self.model_parameters

    @on_trait_change('model._translated')
    def model_specification_changed(self):
#        if self.model._translated and self.model._model_specification_changed: # removed guards and passing IOError in ModelParameters._directory_changed
        self.model_parameters_object = ModelParameters(directory=self.model.directory)
        self.model_parameter_names = [modelVariable.name for modelVariable in self.model_parameters_object.modelVariables]
    
    def object_temporal_formulas_changed(self, info):
        if not os.path.isfile(info.object.temporal_formulas_):
            return
        with read(info.object.temporal_formulas_) as f: 
            lines = f.readlines()
        if len(lines) == 0 or lines[0].strip() != 'Formulas:':
            return
        del self.temporal_formulas[:] # clear list
        for line in lines[1:]:
            line = line.strip()
            
            # skip empty lines
            if len(line) == 0:
                continue
            
            # extract formula
            first = line.find('"')
            second = line.find('"', first + 1)
            formula = line[first + 1:second]
            
            # extract parameters
            parameters_start = line.find('{', second + 1)
            parameters_end = line.find('}', parameters_start + 1)
            parameters = []
            for parameter in line[parameters_start + 1:parameters_end].split(','):
                name_and_values = parameter.split('=')
                name = name_and_values[0].strip()
                values = name_and_values[1].split(':')
                lower = values[0]
                step = values[1]
                upper = values[2]
                
                # create parameter objects
                parameters.append(TemporalFormulaParameter(name=name, lower=float(lower), step=float(step), upper=float(upper)))

            # create formula object and add to list
            temporal_formula = TemporalFormula(
                formula=formula,
                parameters=parameters,
                params_handler=self,
            )
            self.temporal_formulas.append(temporal_formula)

    def _temporal_formulas_items_changed(self):
        ''' Refreshes temporal_formulas. '''
        temporal_formulas = self.temporal_formulas
        self.temporal_formulas = []
        self.temporal_formulas = temporal_formulas
#        for temporal_formula in self.temporal_formulas:
#            print '"' + temporal_formula.formula + '" {' + temporal_formula.parameters_string + '}'
    
    def __edit_temporal_formula(self, temporal_formula):
        result = temporal_formula.edit_traits(kind='livemodal').result 
        if result:
            temporal_formula.formula = temporal_formula.formula.replace('\n', '')
            temporal_formula.update_parameters_string()
        return result 
    
    def _add_temporal_formula_fired(self):
        temporal_formula = TemporalFormula(
            params_handler=self,
            formula=self.default_temporal_formula,
        )
        if self.__edit_temporal_formula(temporal_formula):
            self.temporal_formulas.append(temporal_formula)
            self.selected_temporal_formula = temporal_formula
        
    def _edit_temporal_formula_fired(self):
        temporal_formula = self.selected_temporal_formula
        if temporal_formula is not None:
            self.__edit_temporal_formula(temporal_formula)
            
    def _remove_temporal_formula_fired(self):
        temporal_formula = self.selected_temporal_formula
        if temporal_formula is not None:
            self.temporal_formulas.remove(temporal_formula)
            self.selected_temporal_formula = None

    def save(self, info):
        self.write_temporal_formulas_file()
        super(PModelCheckerParamsHandler, self).save(info)
    
    def perform(self, info):
        self.write_temporal_formulas_file() # in case Perform with unsaved parameters
        super(PModelCheckerParamsHandler, self).perform(info)
        
    def write_temporal_formulas_file(self):
        ''' Write temporal_formulas file, e.g.
            
Formulas:
"P=?[ (Time=1000)U([protein1_(0,0)] >= B ^ [protein1_(0,0)] < B + 5){Time=1000}]" {B=0:10:300}
"P=?[ (Time=R*10)U([protein1_(0,0)] >= A){Time=R*10}]" {R=0:20:200, A=0:1:10}
            
        '''
        with write(self.model.temporal_formulas_) as f:
            f.writelines(['Formulas:\n'] + ['"' + temporal_formula.formula + '" {' + temporal_formula.parameters_string + '}\n' for temporal_formula in self.temporal_formulas])
        

def test():
    execfile('pmodelchecker_params.py')
        
if __name__ == '__main__':
    test()
