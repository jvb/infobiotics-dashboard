from __future__ import with_statement
from infobiotics.commons.api import read, write
from infobiotics.common.api import ParamsHandler
from enthought.traits.api import List, Unicode, Button, Instance, Int
from model_parameters import ModelParameters
from temporal_formulas import TemporalFormula, TemporalFormulaParameter
import os.path

class PModelCheckerParamsHandler(ParamsHandler):
    ''' Traits common to PRISMParamsHandler and MC2ParamsHandler. '''
    
    _model_parameters = Instance(ModelParameters)
    
    def init(self, info): #TODO object_model_specification_changed(self, info):
        super(PModelCheckerParamsHandler, self).init(info)
        self._model_parameters = ModelParameters(directory=self.model.directory)
        # must create _model_parameters here rather than __model_parmeters_default() 
        # because DelegatesTo('_model_parameters') causes it to be created before directory.

    model_parameter_names = List(Unicode)
    
    def __model_parameters_changed(self):
        self.model_parameter_names = [modelVariable.name for modelVariable in self._model_parameters.modelVariables]
    
    temporal_formulas = List(TemporalFormula)
    
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
            second = line.find('"', first+1)
            formula = line[first+1:second]
            
            # extract parameters
            parameters_start = line.find('{', second+1)
            parameters_end = line.find('}', parameters_start+1)
            parameters = []
            for parameter in line[parameters_start+1:parameters_end].split(','):
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
                model_parameter_names=self.model_parameter_names
            )
            self.temporal_formulas.append(temporal_formula)

    def _temporal_formulas_items_changed(self):
        ''' Refreshes temporal_formulas. '''
        temporal_formulas = self.temporal_formulas
        self.temporal_formulas = []
        self.temporal_formulas = temporal_formulas
    
    selected_temporal_formula = Instance(TemporalFormula)

    add_temporal_formula = Button
    edit_temporal_formula = Button
    remove_temporal_formula = Button
    
    def __edit_temporal_formula(self, temporal_formula):
        result = temporal_formula.edit_traits(kind='livemodal').result 
        if result:
            temporal_formula.formula = temporal_formula.formula.replace('\n', '')
        return result 
    
    def _add_temporal_formula_fired(self):
        temporal_formula = TemporalFormula(model_parameter_names=self.model_parameter_names, column=23)
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
        super(PModelCheckerParamsHandler, self).save(info)
        self.write_temporal_formulas_file()

    def write_temporal_formulas_file(self):
        with write(self.model.temporal_formulas_) as f:
            '''
            Formulas:
            "P=?[ (Time=1000)U([protein1_(0,0)] >= B ^ [protein1_(0,0)] < B + 5){Time=1000}]" {B =0:10:300}
            "P=?[ (Time=R*10)U([protein1_(0,0)] >= 50){Time=R*10}]" {R = 0:20:200}
            '''
            lines = ['Formulas:\n']
            for temporal_formula in self.temporal_formulas:
                line = '"%s"' % temporal_formula.formula
                line += ' {'
                for i, parameter in enumerate(temporal_formula.parameters):
                    if i != 0:
                        line += ', ' 
                    line += '%s=%s:%s:%s' % (parameter.name, parameter.lower, parameter.step, parameter.upper)
                line += '}\n'
                lines.append(line)
            f.writelines(lines)


if __name__ == '__main__':
    execfile('prism_params.py')
    