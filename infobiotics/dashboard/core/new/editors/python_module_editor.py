from api import FileEditorHandler, CodeFileEditor, KeyBindings, KeyBinding, default_key_bindings
import os.path

class PythonModuleEditorHandler(FileEditorHandler):
    def run(self, info):
        ''' Run the text as Python code. '''
        info.object.run()

class PythonModuleEditor(CodeFileEditor):
    ''' A Python code editor. '''
    
    lexer = 'python'
    
    def _wildcards_default(self):
        ext = ['*.py']
        import sys
        if sys.platform.startswith('win'):
            ext.append('*.pyw')
        return [('Python modules',ext)]
    
    def _key_bindings_default(self): # can't do key_bindings = KeyBindings(... as all editors end up sharing same key_bindings
        return KeyBindings(
            default_key_bindings + [
                KeyBinding(
                    binding1    = 'Ctrl-r',
                    description = 'Run the file',
                    method_name = 'run'),
            ]
        )
    
    def _handler_default(self): # can't do: handler = PythonModuleEditorHandler() as all editors end up sharing same handler
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
    