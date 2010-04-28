from common.files import read, write
from infobiotics.shared.api import ParamsHandler, List, Button, Instance
from infobiotics.pmodelchecker.api import TemporalFormula, TemporalFormulaParameter

class PModelCheckerParamsHandler(ParamsHandler):
    ''' Contains traits common to PRISMParamsHandler and MC2ParamsHandler. '''
    
    temporal_formulas = List(TemporalFormula)
    
    def object_temporal_formulas_changed(self, info):
        try:
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
                    temporal_formula = TemporalFormula(formula=formula, parameters=parameters)
                    self.temporal_formulas.append(temporal_formula)
                                
        except IOError, e:
#            logger.error('%s, _temporal_formulas_changed()' % e)
            print e

    def _temporal_formulas_items_changed(self):
        ''' Refreshes temporal_formulas. '''
        temporal_formulas = self.temporal_formulas
        self.temporal_formulas = []
        self.temporal_formulas = temporal_formulas
    
    selected_temporal_formula = Instance(TemporalFormula)

    add_temporal_formula = Button
    edit_temporal_formula = Button
    remove_temporal_formula = Button
    
    def _add_temporal_formula_changed(self): # changed works, even for a button
        formula = TemporalFormula()
        if formula.edit_traits(kind='modal').result:
#        # only add formulas with new parameters 
#        for temporal_formula in self.temporal_formulas:
#            if temporal_formula == formula:
#                return
            self.temporal_formulas.append(formula)
        
    def _edit_temporal_formula_changed(self):
        formula = self.selected_temporal_formula
        if formula is not None:
            formula.edit_traits(kind='modal')
        
    def _remove_temporal_formula_changed(self):
        formula = self.selected_temporal_formula
        if formula is not None:
            self.temporal_formulas.remove(formula)
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
    