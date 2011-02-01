#TODO update docstrings

import os.path
from relative_file import RelativeFile

class RelativeDirectory(RelativeFile):
    '''Defines a trait whose value must be the name of a directory (which can 
    be relative to a directory other than the current working directory, as
    specified by the 'directory' attribute or the value of the attribute on the
    HasTraits object named in the 'directory_name' attribute).'''
    
    def get_default_value(self):
        if self.absolute:
            value = os.path.abspath(self.directory)
        else:
            value = '.' # the same directory as self.directory 
        return (1, value)
    
    def __init__(self,
        value='.', #TODO how does this square with get_default_value?
        filter=[],
        auto_set=False,
        entries=0,
        exists=False, exists_name='',
        directory='', directory_name='',
        absolute=False,
        readable=None, writable=None, executable=None,
        empty_ok=False, empty_ok_name='',
        **metadata
    ):
        '''Creates a RelativeDirectory trait.
        
        Parameters
        ----------
        value : string
            The default value for the trait
        filter : list
            A list of wildcard strings to filter filenames in the file dialog 
            box used by the attribute trait editor.
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
            Implies parent directory exists (see can_write).
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
        *value* or '.' if not absolute else 
            os.abspath(os.path.join(self.directory, value)) # == os.path.normpath(os.path.join(os.getcwd(), self.directory, value) 
        
        '''
        super(RelativeDirectory, self).__init__(
            value, filter, auto_set, entries,
            exists, exists_name,
            directory, directory_name,
            absolute,
            readable, writable, executable,
            empty_ok, empty_ok_name,
            **metadata
        )

    def full_info(self, object, name, value):
        '''Calls RelativeFile._full_info with kind='directory'.'''
        return self._full_info(object, name, value, kind='directory')
           
    def validate(self, object, name, value):
        '''Calls RelativeFile._validate with function=os.path.isdir.'''
        return self._validate(object, name, value, function=os.path.isdir)
   
    def create_editor(self):
        '''
        RelativeDirectoryEditor (factory) has a directory trait that has a 
        directory attribute that cannot be empty if the traits empty_ok value 
        is False.
        
        RelativeDirectory trait has a directory attribute that cannot be empty 
        if the traits empty_ok value is False.
        
        RelativeFile trait has a directory attribute that can be empty even if 
        the traits empty_ok value is False.
        
        If the directory *attribute* of a RelativeDirectory trait is empty the 
        trait's value is relative to os.getcwd().    
        '''
        from infobiotics.commons.traits.ui.qt4.relative_directory_editor import RelativeDirectoryEditor
        editor = RelativeDirectoryEditor(
            filter=self.filter or [],
            auto_set=self.auto_set,
            entries=self.entries,
            absolute=self.absolute,
            exists_name=self.exists_name,
            directory=os.path.abspath(self.directory), # must not be '' if RelativeDirectoryEditor.directory(empty_ok=False) which it is by default
            directory_name=self.directory_name,
            empty_ok=self.empty_ok,
            empty_ok_name=self.empty_ok_name,
        )
        return editor
    
