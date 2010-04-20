import os
from common.api import can_read, can_write, can_execute, path_join_overlapping, split_directories
from enthought.traits.api import BaseFile, TraitError

class File(BaseFile):
    """ Defines a trait whose value must be the name of a file using a C-level
        fast validator.
    """

    def __init__(self, value='', filter=[], auto_set=False, entries=0, 
                 exists=False,  
                 directory=os.getcwd(), directory_name=None, 
                 absolute=False,
                 readable=None, writable=None, executable=None,
                 **metadata ):
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
        directory : string
            Specifies a directory prefix that a trait value which is a relative 
            path can be resolved to. If directory is itself a relative path it 
            will be used to prefix the trait value and joined to the current 
            working directory. 
        directory_name : string 
            Specifies an optional extended trait name to sync with directory. 
        absolute : boolean
            Indicates whether the trait value must be an absolute path or not.
            if absolute is True: 
                the file will if necessary be resolved to an absolute path
                using the value of directory and/or os.getcwd().
            else: 
                the file will be assumed to be relative to directory and/or 
                os.getcwd() for the purposes of exists validation.
        readable : either True, False or None
            Implies file exists.
            if readable is True: 
                validate will return an error if the file cannot be read.
            elif readable is False: 
                validate will return an error if the file can be read.
        writable : either True, False or None
            Implies directory exists.
            if writable is True:
                validate will return an error if the file cannot be written.
            elif writable is False: 
                validate will return an error if the file can be written.
        executable : either True, False or None
            Implies file exists.
            if executable is True: 
                validate will return an error if the file cannot be executed.
            elif executable is False: 
                validate will return an error if the file can be executed.
                
        Default Value
        -------------
        *value* or ''
        
        """
        # disable fast validator
#        if not exists:
#            # Define the C-level fast validator to use:
#            fast_validate = ( 11, basestring )

        # coerce directory
#        if directory == '':
#            directory = os.getcwd()
        self.directory = directory
        
        # coerce directory_name
#        if not directory_name == '':
#            if not directory_name.startswith(('object.','controller.','model.')):
#                directory_name = 'object.' + directory_name
        self.directory_name = directory_name

        self.absolute = absolute
        
        self.readable = readable
        self.writable = writable
        self.executable = executable

        super(File, self).__init__(value, filter, auto_set, entries, exists, **metadata)
           
    def get(self, object, name):
        if self.directory_name is not None:
            print getattr(self, self.directory_name)
#        return object.directory
        # if directory = '/tmp/'
        # and file = '/tmp/file'
        # return 'file'
        return 'see <File>.get()'                           

#    def validate(self, object, name, value):
    def set(self, object, name, value):
        """ Validates that a specified value is valid for this trait.

        Note: The there is *not* a 'fast validator' version that performs 
        this check in C.
        """
        
        try:
            validated_value = super(BaseFile, self).validate(object, name, value)
    
            if os.path.isabs(self.directory):
                directory = self.directory
            else:
                directory = os.path.join(os.getcwd(), self.directory)
    
            if self.absolute:
                # coerce to absolute with directory and/or os.getcwd()
                if not os.path.isabs(validated_value):
                    validated_value = os.path.join(directory, validated_value)
            else:
                if validated_value != '':
                    # coerce to relative with directory and/or os.getcwd()
                    validated_value = os.path.normpath(os.path.relpath(validated_value, directory))
    
            error = None
    
            if self.readable is not None:
                if self.readable:
                    if not can_read(validated_value):
                        error = 'readable'
                else:
                    if can_read(validated_value):
                        error = 'unreadable'
            
            if self.writable is not None:
                if self.writable:
                    if not can_write(validated_value):
                        error = 'writable'
                else:
                    if can_write(validated_value):
                        error = 'unwritable'
    
            if self.executable is not None:
                if self.executable:
                    if not can_execute(validated_value):
                        error = 'executable'
                else:
                    if can_execute(validated_value):
                        error = 'unexecutable'
            
            if error:
                raise TraitError(error)
#                raise TraitError(object, name, error, validated_value)
            
            if not self.exists:
                return validated_value
            elif os.path.isfile(validated_value):
                return validated_value
    
            self.error(object, name, validated_value)

        except TraitError, e:
#            print e
            self.desc = e
            raise
        
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
    
#    default_value = ''
#    def get_default_value(self):
#        return default_value

    def full_info(self, object, name, value):
        
        info = 'an '
        
        if self.exists:
            info += 'existing '

        permissions = []
        
        if self.readable is not None:
            permissions.append('readable') if self.readable else permissions.append('unreadable')

        if self.writable is not None:
            permissions.append('writable') if self.writable else permissions.append('unwritable')

        if self.executable is not None:
            permissions.append('executable') if self.executable else permissions.append('unexecutable')

        if len(permissions) > 0:
            info += ', '.join(permissions)
        
        if info != 'an ' and info != 'an existing ':
            info += 'and '
        if self.absolute:
            info += 'absolute '
        
        if info == 'an ':
            info = 'a '
        
        info += 'file name '
        
        if self.directory != '':
            info += '\n'
            info += 'in %s' % self.directory
            info += '\n'  
        
        return info
#        return self.info()
#
#    info_text = 'a file name'
#    def info(self):
#        return self.info_text


from enthought.traits.api import HasTraits, Property, Str

class Test(HasTraits):
    directory = Str('/home/jvb/phd/eclipse/infobiotics/dashboard/tests/mcss/models')
    file = File('module1.sbml',
#        desc='tooltip',
        auto_set=True,
        exists=True,
#        readable=False,
#        writable=True,
#        executable=False,
        absolute=True,
#        directory='/home/jvb/Desktop/unwritable',
        directory_name='object.directory',
    )
    value = Property(depends_on='file')
    def _get_value(self):
        return self.file
    
if __name__ == '__main__':
    Test().configure_traits()