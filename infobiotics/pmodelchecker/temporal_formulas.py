from infobiotics.shared.api import (
    HasTraits, Str, Float, List, Button, Any, 
    View, Item, HGroup, VGroup, ListEditor,  
    TableEditor, ObjectColumn, 
)
    
temporal_formula_view = View(
    Item('formula'),
    Item('parameters', 
        style='custom', 
        editor=ListEditor(
            style='custom',
            use_notebook=True,
            page_name='.name',
            view = View(
                Item('name'),
                Item('lower_bound'),
                Item('step'),
                Item('upper_bound'),
                title='Edit Temporal Formula Parameter',
            ),
            selected='selected',
        ),
    ),
    HGroup(
        Item('add_new_parameter', show_label=False), 
        Item('remove_current_parameter', show_label=False),
    ),
    buttons = [
        'OK', 
        'Cancel',
    ],
    width=600,
    resizable=True,
    title='Edit temporal formula properties',
)

class TemporalFormulaParameter(HasTraits):
    name = Str
    lower_bound = Float(0)
    upper_bound = Float(1)
    step=Float(0.5)

class TemporalFormula(HasTraits):
    '''
    MC2 formula_parameters string:
    """
    Formulas
    "<formula>" {<paramName> = <lower>:<step>:<upper>, ..., <paramName> = <lower>:<step>:<upper>}
    "<another_formula>" {...}
    """
    
    PRISM formulas file format:
    """
    <formula1>
    <formula2>
    """
    
    PRISM formula_parameters string:
    """
    parameter_name=low:upper:step, parameter_name_2=low:up:step
    """
    '''
    
    formula = Str('P=a') #TODO better example? #TODO help?
    parameters = List(TemporalFormulaParameter, [TemporalFormulaParameter(name='a')])
    
    parameters_string = Str #TODO rename
    add_new_parameter = Button
    remove_current_parameter = Button
    
    selected = Any
#    def _selected_changed(self, selected):
#        print selected

    def _add_new_parameter_fired(self):
        self.parameters.append(TemporalFormulaParameter())
    
    def _remove_current_parameter_fired(self):
        try:
            self.parameters.remove(self.selected)
        except ValueError:
            pass
            
    def _parameters_changed(self, value):
        parameters_string = ''
        for i, parameter in enumerate(self.parameters):
            if len(parameter.name) > 0:
                if i != 0:
                    parameters_string += ', ' 
                parameters_string += '%s=%s:%s:%s' % (parameter.name, parameter.lower_bound, parameter.step, parameter.upper_bound)
        self.parameters_string = parameters_string

#    def __eq__(self, other):
#        if self.formula == other.formula:
#            matching_parameters = []
#            for parameter in self.parameters:
#                for other_parameter in other.parameters:
#                    print parameter, other_parameter
#                    if parameter == other_parameter:
#                        matching_parameters.append(other_parameter)
#            if len(matching_parameters) == len(self.parameters):
#                return True
#        return False
        
    traits_view = temporal_formula_view

temporal_formulas_group = VGroup(
    HGroup(   
        Item('temporal_formulas', label='File'),
    ),
    Item('handler._temporal_formulas_list', 
        label='Temporal formulas', 
        show_label=False,
        editor=TableEditor(
            columns=[
                ObjectColumn(name='formula',
                    width=0.5,
                    editable=False,
                ),
                ObjectColumn(name='parameters_string', 
                    label='Parameters (name=lower:step:upper)', 
                    width=0.5,
                    editable=False,
                ),
            ],
            selection_mode='row', selected='object.selected_temporal_formula',
            dclick='_edit_temporal_formula', # fires PModelCheckerHandler.object__edit_temporal_formula_changed()!
#            dclick='object._edit_temporal_formula', # so does this
#            dclick='handler.dclick', #TEST event trait on handler, works
            rows=2,
#            menu=Menu(), #TODO
            # not in traitsbackendqt-3.2.0 (@24005)
#            on_dclick=on_dclick, 
#            reorderable=True,
#            deletable=True,
#            editable=True, row_factory=TemporalFormula, auto_add=True,
#            editable=True, edit_view=temporal_formula_view,
        ),
    ),
    HGroup(
        Item('handler._add_temporal_formula', show_label=False),
        Item('handler._edit_temporal_formula', show_label=False, enabled_when='object.selected_temporal_formula is not None'),
        Item('handler._remove_temporal_formula', show_label=False, enabled_when='len(object._temporal_formulas_list) > 0 and object._selected_temporal_formula is not None'),
    ),
    label='Temporal formulas',
)


if __name__ == '__main__':
    execfile('mc2_experiment.py')
    