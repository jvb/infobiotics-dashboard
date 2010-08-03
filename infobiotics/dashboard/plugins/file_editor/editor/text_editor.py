# TextEditor should be half way between a FileEditor and PythonEditor


    def select_line(self, lineno):
        ''' Selects the specified line. '''
        self.ui.info.content.selected_line = lineno
        
    def _load(self, file):
        ''''''
        self.content = f.read()
    
