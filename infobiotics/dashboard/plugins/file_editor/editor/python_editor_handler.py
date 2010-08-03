from file_editor_handler import FileEditorHandler

class PythonEditorHandler(FileEditorHandler):

    def run(self, info):
        ''' Run the text as Python code. '''
        info.object.run()
