from enthought.traits.api import BaseFile

class File(BaseFile):
    """ Defines a trait whose value must be the name of a file using a C-level
        fast validator.
    """

    def __init__(self, value='', filter=[], auto_set=False, entries=0, 
                 directory='', directory_name='',
                 exists=False, **metadata ):
        """ Creates a File trait.

        Parameters
        ----------
        value : string
            The default value for the trait
        filter : string
            A wildcard string to filter filenames in the file dialog box used by
            the attribute trait editor.
        auto_set : boolean
            Indicates whether the file editor updates the trait value after
            every key stroke.
        exists : boolean
            Indicates whether the trait value must be an existing file or
            not.
        #TODO

        Default Value
        -------------
        *value* or ''
        """
        if not exists:
            # Define the C-level fast validator to use:
            fast_validate = ( 11, basestring )

        if directory == '':
            import os
            directory = os.getcwd()
        self.directory = directory
        if not directory_name == '' and not directory_name.startswith('object.'):
            directory_name = 'object.' + directory_name
        self.directory_name = directory_name

        super( File, self ).__init__( value, filter, auto_set, entries, exists,
                                      **metadata )
        
    def create_editor(self):
        from enthought.traits.ui.qt4.file_editor2 import FileEditor
        editor = FileEditor(
            filter=self.filter or [],
            auto_set=self.auto_set,
            entries=self.entries,
            directory=self.directory,
            directory_name=self.directory_name,
        )
        return editor
    