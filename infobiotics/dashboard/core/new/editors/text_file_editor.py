from api import AbstractFileEditor
from enthought.traits.api import Str

class TextFileEditor(AbstractFileEditor):
    ''' A text file editor. '''
    
    content = Str

    wildcards = [('Text files',['*.txt'])]

    def save_(self, file):
        ''' Overloaded method that implements saving the file. '''
        file.write(self.content)
        
    def load_(self, file):
        ''' Overloaded method that implements loading the file. '''
        self.content = file.read()
