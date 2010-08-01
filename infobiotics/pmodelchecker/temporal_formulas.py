from enthought.traits.api import (
    HasTraits, Str, Float, Int, List, Button, Any, Enum, Unicode, Any, Property,
    on_trait_change,
)
from enthought.traits.ui.api import (
    View, Item, HGroup, VGroup, Group, Spring, ListEditor, TableEditor,
    CodeEditor, Spring, TextEditor
)
from enthought.traits.ui.table_column import ObjectColumn
from infobiotics.commons.traits.ui.api import HelpfulController, help_action
#from infobiotics.commons.traits.float_with_minimum import FloatWithMinimum

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
    # don't replicate range_or_value from model_parameter_names, 
    # if they want a constant they can just put it in the formula 
    name = Str
    lower = Float(0)
    step = Float(0.5)
    upper = Float(1)
#    lower = FloatWithMinimum(0)
#    step = FloatWithMinimum(0.5)
#    upper = FloatWithMinimum(1) # default values don't seem to work
    
    dp = Int(desc='the most decimal places between lower, step and upper')

    @on_trait_change('lower, step, upper')
    def determine_precision(self):
        mdp = 0
        for value in (self.lower, self.step, self.upper):
            split = str(value).split('.')
            if len(split) == 2:
                if int(split[1]) == 0:
                    continue
                dp = len(split[1])
                if dp > mdp: 
                    mdp = dp
        self.dp = mdp

    def format(self, value):
        if self.dp > 0:
            return "%.*f" % (self.dp, value)
        else:
            return "%d" % (value)
        
def evaluate_temporal_formula_parameter_range(value):
    try:
        f = float(eval(value))
        if f < 0:
            raise TraitError()
        return f 
    except:
        raise TraitError()

temporal_formula_parameter_range_editor=TextEditor(evaluate=evaluate_temporal_formula_parameter_range)

class TemporalFormulaParameterItem(Item):
    editor = temporal_formula_parameter_range_editor
    

class TemporalFormulaHandler(HelpfulController):
    
    help_urls = [('Property specification', 'http://www.prismmodelchecker.org/manual/PropertySpecification/Introduction')]
    
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
                selected_text='selected_text',
            ), 
            tooltip='Multiple lines will be concatenated.'), 
        HGroup(
            Spring(),
            Item('model_parameter_name_to_insert', label='Model parameters:'), #FIXME descriptions (EnumEditor?)
            Item('insert', show_label=False, enabled_when='object.model_parameter_name_to_insert is not None'),
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
#                            Item('lower'),
#                            Item('step'),
#                            Item('upper'),
#                            Item('lower', editor=temporal_formula_parameter_range_editor),
#                            Item('step', editor=temporal_formula_parameter_range_editor),
#                            Item('upper', editor=temporal_formula_parameter_range_editor),
                            TemporalFormulaParameterItem('lower'),
                            TemporalFormulaParameterItem('step'),
                            TemporalFormulaParameterItem('upper'),
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
    buttons = ['Undo', 'Cancel', 'OK', help_action],#, 'Revert'],
    resizable = True,
    title = 'Edit temporal formula',
    handler = TemporalFormulaHandler(),
    height=100,
    id = 'temporal_formula_view',
)


class TemporalFormula(HasTraits):

    traits_view = temporal_formula_view
    
    line = Int
    column = Int
    selected_text = Str
    params_handler = Any#Instance(PModelCheckerParamsHandler)
    model_parameter_names = Property(List(Unicode), depends_on='params_handler.model_parameter_names')
    def _get_model_parameter_names(self):
        return self.params_handler.model_parameter_names 
    model_parameter_name_to_insert = Enum(values='model_parameter_names')
    insert = Button
    def _insert_fired(self):
        if self.model_parameter_name_to_insert is None:
            return
        lines = self.formula.split('\n')
        line = lines[self.line]
        col = self.column-len(self.selected_text)
        line = line[:col] + self.model_parameter_name_to_insert + line[self.column:]
        lines[self.line] = line
        self.formula = '\n'.join(lines)
        self.column = col + len(self.model_parameter_name_to_insert) + 1
        # focus given back to CodeEditor in TemporalFormulaHandler.object_insert_changed()
        
    formula = Str
    parameters = List(TemporalFormulaParameter)#, [TemporalFormulaParameter(name='T')]) was causing all first Parameters to be same instance!
    def _parameters_default(self):
        return [TemporalFormulaParameter(name='T')]
    
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
            
    parameters_string = Str
    @on_trait_change('parameters, parameters.lower, parameters.step, parameters.upper')
    def update_parameters_string(self):
        self.parameters_string = ','.join(['%s=%s:%s:%s' % (parameter.name, parameter.format(parameter.lower), parameter.format(parameter.step), parameter.format(parameter.upper)) for parameter in self.parameters if parameter.name != ''])


if __name__ == '__main__':
    from mc2.mc2_experiment import MC2Experiment
    MC2Experiment().configure()
    