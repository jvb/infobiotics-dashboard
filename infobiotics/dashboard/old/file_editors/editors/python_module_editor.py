from text_file_editor import TextFileEditor
from enthought.traits.api import Code
from enthought.traits.ui.key_bindings import KeyBindings, KeyBinding
from abstract_file_editor import save_key_binding

class PythonModuleEditor(TextFileEditor):
    ''' A Python code editor. '''
    
    content = Code

    def _wildcards_default(self):
        ext = ['*.py']
        import sys
        if sys.platform.startswith('win'):
            ext.append('*.pyw')
        return [('Python modules',ext)]
    
#    key_bindings = KeyBindings( # all editors end up sharing same key_bindings
#        save_key_binding,
#        KeyBinding(
#            binding1    = 'Ctrl-r',
#            description = 'Run the file',
#            method_name = 'run'),
#    )
    def _key_bindings_default(self):
        return KeyBindings(
            save_key_binding,
            KeyBinding(
                binding1    = 'Ctrl-r',
                description = 'Run the file',
                method_name = 'run'),
        )
    
#    handler = PythonModuleEditorHandler() # all editors end up sharing same handler
    def _handler_default(self):
        from python_module_editor_handler import PythonModuleEditorHandler
        return PythonModuleEditorHandler()

    def run(self):
        ''' Runs the file as Python. '''
        
        self.save() # The file must be saved first! #TODO do the same with experiments 
        
        if os.path.splitext(self.obj.path)[1] not in ('.py','.pyw'):
            print 'Not a Python file!' #TODO auto_close_message
            return 
        
        # Execute the code.
        if len(self.obj.path) > 0:
            view = self.window.get_view_by_id(
                'enthought.plugins.python_shell_view'
            )
            if view is not None:
                view.execute_command(
                    'execfile(r"%s")' % self.obj.path, 
                    hidden=False
                )

    def select_line(self, lineno):
        ''' Selects the specified line. '''
        self.ui.info.content.selected_line = lineno
    