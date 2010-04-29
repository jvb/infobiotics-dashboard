import os
from file import File
from common.api import can_read, can_write, can_execute#, path_join_overlapping, split_directories

class Directory(File):
    """ Defines a trait whose value must be the name of a directory (which can 
    be relative to a directory other than the current working directory.)
    
    """
    def __init__(self, value='', filter=[], auto_set=False, entries=0, 
                 exists=False, exists_name='',
                 directory='', directory_name='',
                 absolute=False,
                 readable=None, writable=None, executable=None,
                 **metadata ):
        """ Creates a File trait.
        
        Parameters
        ----------
        value : string
            The default value for the trait
        filter : string
            A wildcard string to filter directories in the file dialog box used 
            by the attribute trait editor.
        auto_set : boolean
            Indicates whether the file editor updates the trait value after
            every key stroke.
        exists : boolean
            Indicates whether the trait value must be an existing file or
            not.
        directory : string
            Specifies a directory prefix that a trait value which is a relative 
            path can be resolved to. If directory is itself a relative path it 
            will be used to prefix the trait value and joined to the current 
            working directory. 
        directory_name : string 
            Specifies an optional extended trait name to sync with directory. 
        absolute : boolean
            Indicates whether the trait value must be an absolute path or not.
            The directory will if necessary be resolved to an absolute path 
            using the value of directory and/or os.getcwd().
            if absolute is True: 
                value will be an absolute path.
            else: 
                value will be a relative path. 
        readable : either True, False or None
            Implies directory exists.
            if readable is True: 
                validate will return an error if the directory cannot be read.
            elif readable is False: 
                validate will return an error if the directory can be read.
        writable : either True, False or None
            Implies parent directory exists (see can_write in common).
            if writable is True:
                validate will return an error if the directory cannot be 
                written.
            elif writable is False: 
                validate will return an error if the directory can be written.
        executable : either True, False or None
            Implies directory exists.
            if executable is True: 
                validate will return an error if the directory cannot be 
                executed.
            elif executable is False: 
                validate will return an error if the directory can be executed.
                
        Default Value
        -------------
        *value* or ''
        
        """
        super(Directory, self).__init__(value, filter, auto_set, entries, 
                                        exists, exists_name, 
                                        directory, directory_name,
                                        absolute,
                                        readable, writable, executable,
                                        **metadata)

    def full_info(self, object, name, value):
        ''' Constructs an error string to be incorporated into a TraitError. '''
        return self._full_info(object, name, value, kind='directory ')
           
    def validate(self, object, name, value):
        ''' Calls File._validate with os.path.isdir as function. '''
        return self._validate(object, name, value, os.path.isdir)
   
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
    