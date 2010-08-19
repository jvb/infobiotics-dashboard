from text_file_editor import TextFileEditor
from enthought.traits.api import Code, Int, Str, List, Color, Enum, Bool
from enthought.traits.ui.api import Group, Item, CodeEditor

class CodeFileEditor(TextFileEditor):
    ''' A generic code editor. '''
    
    content = Code
    
    # CodeEditor traits http://www.cs.nott.ac.uk/~jvb/ETS34_API/enthought.traits.ui.editors.code_editor.ToolkitEditorFactory.html
    auto_scroll = True
    auto_set = True
    column = Int
    dim_color = Str(desc='#rrggbb')
    dim_lines = List(Int)
    foldable = True
    _key_bindings = None # overrides self.key_bindings inherited from AbstractFileEditor?
    lexer = 'null'
    line = Int
    mark_color = Color(15526360)
    mark_lines = List(Int)
    search = Enum('bottom', 'top', 'none')
    search_color = Color(16777108)
    selected_color = Color(16777108)
    selected_line = Int
#    def select_line(self, lineno):
#        ''' Selects the specified line. '''
#        self.ui.info.content.selected_line = lineno
    selected_text = Str
    show_line_numbers = Bool(True)
    squiggle_color = Str('#FF0000')
    squiggle_lines = List(Int)

    items = (
        Item(label='Ctrl-F to search'),
    )
    def _group_default(self):
        return Group(
            Item('content', style='custom',
                editor=CodeEditor(
                    auto_scroll=self.auto_scroll,
                    auto_set=self.auto_set,
                    column='column',
                    dim_color='dim_color',
                    dim_lines='dim_lines',
                    foldable=self.foldable,
                    key_bindings=self._key_bindings,
                    lexer=self.lexer,
                    line='line',
                    mark_color=self.mark_color,
                    mark_lines='mark_lines',
                    search=self.search,
                    search_color=self.search_color,
                    selected_color=self.selected_color,
                    selected_line='selected_line',
                    selected_text='selected_text',
                    show_line_numbers=self.show_line_numbers,
                    squiggle_color='squiggle_color',
                    squiggle_lines='squiggle_lines',
                ),
            ),
            *self.items,
            show_labels = False
        )
    
