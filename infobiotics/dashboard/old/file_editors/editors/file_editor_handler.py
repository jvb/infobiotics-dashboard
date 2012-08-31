from traitsui.api import Handler

class FileEditorHandler(Handler):
    ''' Necessary for KeyBindings to function. '''

    def save(self, info):
        ''' Save the file to disk. '''
        info.object.save()
