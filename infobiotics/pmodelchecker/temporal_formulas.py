from enthought.traits.api import HasTraits, Str, Float, Int, List, Button, Any
from enthought.traits.ui.api import (
    View, Item, HGroup, VGroup, Group, Spring, ListEditor, TableEditor,
    Handler, CodeEditor, Spring
)
from enthought.traits.ui.table_column import ObjectColumn

temporal_formulas_group = VGroup(
    HGroup(   
        Item('temporal_formulas'),#, label='File'),
    ),
    Item('handler.temporal_formulas', 
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
            selection_mode='row', selected='handler.selected_temporal_formula',
            dclick='handler.edit_temporal_formula', # fires PModelCheckerHandler.object__edit_temporal_formula_changed()!
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
        Spring(),
        Item('handler.add_temporal_formula', show_label=False),
        Item('handler.edit_temporal_formula', show_label=False, enabled_when='handler.selected_temporal_formula is not None'),
        Item('handler.remove_temporal_formula', show_label=False, enabled_when='len(handler.temporal_formulas) > 0 and handler.selected_temporal_formula is not None'),
        Spring(),
    ),
)

class TemporalFormulaParameter(HasTraits):
    name = Str
    lower = Float(0)
    step = Float(0.5)
    upper = Float(1)
    # don't replicate range_or_value from model_parameter_names, 
    # if they want a constant they can just put it in the formula 

class TemporalFormulaHandler(Handler):
    
    def object_insert_changed(self, info):
        ''' Set focus back to CodeEditor. Works despite raising AttributeError! '''
        for editor in info.ui._editors:
            if hasattr(editor, '_scintilla'):
                try:
                    editor._scintilla.setFocus(True)
                except AttributeError:
                    pass

temporal_formula_view = View(
    VGroup(
        Item(label='Formula:'),
        Item('formula', 
            show_label=False,
            style='custom', 
            editor=CodeEditor(
                lexer='null', 
                show_line_numbers=False, 
                auto_set=True, 
                line='line', 
                column='column',
            ), 
            tooltip='Multiple lines will be concatenated.'), 
        HGroup(
            Spring(),
            Item('model_parameter_name_to_insert', label='Model parameters:'), #FIXME descriptions (EnumEditor?)
            Item('insert', show_label=False),
            Spring(),
        ),
        Item(label='Formula parameters:'),
        Item('parameters',
            show_label=False,
            style='custom', 
            editor=ListEditor(
                style='custom',
                use_notebook=True,
                page_name='.name',
                view = View(
                    Group(    
                        Item('name'),
                        HGroup(
                            Item('lower'),
                            Item('step'),
                            Item('upper'),
                        ),
                        show_border=True,
                    ),
                ),
                selected='selected',
            ),
        ),
        HGroup(
            Spring(),
            Item('add_new_parameter', show_label=False), 
            Item('remove_current_parameter', show_label=False, enabled_when='len(object.parameters) > 1'),
            Spring(),
        ),
        show_border = True,
    ),
    buttons = ['Undo', 'Cancel', 'OK'],#, 'Revert'],
    resizable = True,
    title = 'Edit temporal formula',
    handler = TemporalFormulaHandler(),
    height=100,
    id = 'temporal_formula_view',
)


from enthought.traits.api import Int, Str, Button, List, Enum, Unicode

class TemporalFormula(HasTraits):

    traits_view = temporal_formula_view
    
    line = Int
    column = Int
    model_parameter_names = List(Unicode)
    model_parameter_name_to_insert = Enum(values='model_parameter_names')
    insert = Button
    
    def _insert_fired(self):
        lines = self.formula.split('\n')
        line = lines[self.line]
        line = line[:self.column] + self.model_parameter_name_to_insert + ' ' + line[self.column:]
        lines[self.line] = line
        self.formula = '\n'.join(lines)
        # focus given back to CodeEditor in TemporalFormulaHandler.object_insert_changed()
        

    formula = Str('P = ? [ true U[A,A] (  >= X ) ]') #TODO better example? #TODO help?
    parameters = List(TemporalFormulaParameter, [TemporalFormulaParameter(name='A'), TemporalFormulaParameter(name='X')])
    
    parameters_string = Str
    add_new_parameter = Button
    remove_current_parameter = Button
    
    selected = Any

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
                parameters_string += '%s=%s:%s:%s' % (parameter.name, parameter.lower, parameter.step, parameter.upper)
        self.parameters_string = parameters_string


if __name__ == '__main__':
#    execfile('mc2_experiment.py')
    execfile('prism_params.py')
    
    