from enthought.traits.api import BaseDirectory

class Directory(BaseDirectory):
    """ Defines a trait whose value must be the name of a directory using a
        C-level fast validator.
    """

    def __init__(self, value='', filter=[], auto_set=False, entries=0, 
                 directory='', directory_name='',
                 exists=False, **metadata ):
        """ Creates a Directory trait.

        Parameters
        ----------
        value : string
            The default value for the trait
        auto_set : boolean
            Indicates whether the directory editor updates the trait value
            after every key stroke.
        exists : boolean
            Indicates whether the trait value must be an existing directory or
            not.
        #TODO

        Default Value
        -------------
        *value* or ''
        """
        # Define the C-level fast validator to use if the directory existence
        # test is not required:
        if not exists:
            self.fast_validate = ( 11, basestring )

        if directory == '':
            import os
            directory = os.getcwd()
        self.directory = directory
        if not directory_name == '' and not directory_name.startswith('object.'):
            directory_name = 'object.' + directory_name
        self.directory_name = directory_name

        super( Directory, self ).__init__( value, auto_set, entries, exists,
                                           **metadata )

    def create_editor(self):
        from enthought.traits.ui.qt4.directory_editor2 import DirectoryEditor
        editor = DirectoryEditor(
            filter=self.filter or [],
            auto_set=self.auto_set,
            entries=self.entries,
            directory=self.directory,
            directory_name=self.directory_name,
        )
        return editor
    