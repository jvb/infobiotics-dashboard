from file_editor import save_key_binding

class PythonEditor(TraitsUIEditor):
    ''' A Python code editor. '''
    
    content = Code

    def _key_bindings_default(self):
        key_bindings = KeyBindings(
            save_key_binding,
            KeyBinding(
                binding1    = 'Ctrl-r',
                description = 'Run the file',
                method_name = 'run'),
        )
        return key_bindings

    def _save(self, file):
        ''' . '''
        file.write(self.content)
        
    def run(self):
        ''' Runs the file as Python. '''
        
        self.save() # The file must be saved first! #TODO do the same with experiments 
        
        if os.path.splitext(self.obj.path)[1] not in ('.py','.pyw'):
            print 'Not a Python file!'
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