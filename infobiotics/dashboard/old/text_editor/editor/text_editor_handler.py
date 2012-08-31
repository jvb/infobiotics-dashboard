from traitsui.api import Handler

class TextEditorHandler(Handler):
    ''' Necessary for KeyBindings to function. '''

    def run(self, info):
        ''' Run the text as Python code. '''
        info.object.run()
    
    def save(self, info):
        ''' Save the text to disk. '''
        info.object.save()
