import os
#from enthought.traits.api import BaseFile
from enthought.traits.api import BaseStr
from infobiotics.commons.api import can_read, can_write, can_execute
from infobiotics.thirdparty.which import which, WhichError

#class RelativeFile(BaseFile):
class RelativeFile(BaseStr):
    """ Defines a trait whose value must be the name of a file (which can be 
    relative to a directory other than the current working directory, as
    specified by 'directory_name').
    
    """
    def __init__(self, 
        value='', 
        filter=[], 
        auto_set=False, 
        entries=0, 
        exists=False, exists_name='',
        directory='', directory_name='',
        absolute=False,
        readable=None, writable=None, executable=None,
        **metadata
    ):
        """ Creates a RelativeFile trait.
        
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
            The file will if necessary be resolved to an absolute path using the
            value of directory and/or os.getcwd().
            if absolute is True: 
                value will be an absolute path.
            else: 
                value will be a relative path. 
        readable : either True, False or None
            Implies file exists.
            if readable is True: 
                validate will return an error if the file cannot be read.
            elif readable is False: 
                validate will return an error if the file can be read.
        writable : either True, False or None
            Implies directory exists (see can_write in common).
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

        self.absolute = absolute
        
        if directory != '' and directory_name != '':
            raise ValueError, "Please specify only 'directory' or 'directory_name', the value of '%s' named in the attribute directory_name will override '%s' in the attribute directory of the %s trait." % (directory_name, directory, self.__class__.__name__)
        
#        self.directory = directory if directory != '' else os.getcwd() # can't set this in class definition: it will always be the location of the module  
        self.directory = directory  

        self.directory_name = directory_name

        self.exists_name = exists_name
            
        # make exists True if readable or executable are not None
        if (readable is not None or executable is not None) and not exists:
            exists = True

        self.readable = readable
        self.writable = writable
        self.executable = executable

        super(RelativeFile, self).__init__(
#            value, filter, auto_set, entries, exists, **metadata
            value, **metadata
        )

        if isinstance(filter, (str, unicode)):
            filter = [filter]
        self.filter = filter
        self.auto_set = auto_set
        self.entries = entries
        self.exists = exists
        
#        self.editor = self.create_editor() # problem with circular imports - try not subclassing BaseFile instead.

#    default_value = ''
#
#    def get_default_value(self):
#        return default_value

#    info_text = 'a file name' # used if info() and full_info() are not defined
#
#    def info(self): # used if full_info() is not defined
#        return self.info_text

    def full_info(self, object, name, value):
        ''' Constructs an error string to be incorporated into a TraitError.
        
        '''
        return self._full_info(object, name, value)
        
    def _full_info(self, object, name, value, kind='file name'):
        ''' Constructs an error string to be incorporated into a TraitError.
        
        '''
        permissions = []
        if self.readable is not None:
            permissions.append('readable ') if self.readable else permissions.append('non-readable ')
        if self.writable is not None:
            permissions.append('writable ') if self.writable else permissions.append('non-writable ')
        if self.executable is not None:
            permissions.append('executable ') if self.executable else permissions.append('non-executable ')
        
        info = 'a '
        if self.exists:
            info = 'an existing '
        if len(permissions) > 0:
            info += ', '.join(permissions)
            
        if self.absolute:
            if len(permissions) > 0:
                info += 'and '
            info += 'absolute '
        
        info += kind
        
        if self.directory != '' and not self.absolute:
#            info += '\n' # make tooltips easier to read # now done using wrap
            info += " in '%s'" % os.path.abspath(self.directory)
#            info += '\n'  
        
        return info
           
    def _set_directory_from_directory_name(self, object):
        ''' Factored out of _validate because it also used in post_setattr. '''
        if self.directory_name == '':
            return
        directory = getattr(object, self.directory_name) #FIXME won't work for extended trait names (Range doesn't seem to do this either, maybe sync_value or _sync_values does?)
        if directory != '':
            self.directory = directory
        
    def _set_exists_from_exists_name(self, object):
        if self.exists_name == '':
            return
        self.exists = getattr(object, self.exists_name)

    def validate(self, object, name, value):
        ''' Calls _validate so that we can reuse _validate for Directory traits. ''' 
        return self._validate(object, name, value)

    def _validate(self, object, name, value, function=os.path.isfile):
        """ Validates that a specified value is valid for this trait.

        Note: The there is *not* a 'fast validator' version that performs 
        this check in C.
        
        if directory = '/tmp'
        and abspath = '/tmp/file'
        return 'file'
        """
        value = super(RelativeFile, self).validate(object, name, value) # validate value using BaseStr's validator 
#        print 'value =', value
        
        self._set_directory_from_directory_name(object)
        
        directory = self.directory
        if directory == '':
            if not os.path.isabs(value):
                try:
                    value = which(value)
                except WhichError:
#                    print 'WhichError, value =', value #TODO
                    pass
        if not os.path.isabs(directory):
            directory = os.path.join(os.getcwd(), directory)
#        print 'directory =', directory
        
        if not os.path.isabs(value):
            abspath = os.path.join(directory, value)
        else:
            abspath = value # needed by isfile below
#        print 'abspath =', abspath
        
#        print 'self.absolute =', self.absolute
        if self.absolute:
            value = abspath

        self._set_exists_from_exists_name(object)
        
        if not self.exists: # we don't care whether it exists 
            if self.writable is not None: # we care whether it can be written (created)
                # validate whether it is writable failing last
                if self.writable: # we care that it can be written
                    if can_write(abspath): # we can write it
                        return value
                    # we can't write it so drop through to self.error()
                else: # we care that it can't be written
                    if not can_write(abspath): # we can't write it
                        return value
                    # we can write it so drop through to self.error()
            else: # we don't care whether it can be written
                return value
        
        elif function(abspath): # we care whether it exists
            if self.readable is not None: # we care whether it can be read
                # validate whether it is readable failing fast 
                if self.readable: # we care that it can be read
                    if not can_read(abspath): # we can read it
                        self.error(object, name, value)
                else: # we care that it can't be read
                    if can_read(abspath): # we can read it
                        self.error(object, name, value)
            if self.writable is not None: # we care whether it can be written
                # validate whether it is writable failing fast
                if self.writable: # we care that it can be written
                    if not can_write(abspath): # we can't write it
                        self.error(object, name, value)
                else: # we care that it can't be written
                    if can_write(abspath): # we can write it
                        self.error(object, name, value)
            if self.executable is not None: # we care whether it can be executed
                # validate whether it is executable failing fast
                if self.executable: # we care that it can be executed
                    if not can_execute(abspath): # we can't execute it
                        self.error(object, name, value)
                else: # we care that it can't be executed
                    if can_execute(abspath): # we can execute it
                        self.error(object, name, value)
            return value # it does exist and we can/can't read/write/execute it appropriately
        # it doesn't exist
        self.error(object, name, value)

    def post_setattr(self, object, name, value):
        # only required here the first time the value is set
        self._set_directory_from_directory_name(object)
        if not os.path.isabs(value):
            if not os.path.isabs(self.directory):
                directory = os.path.join(os.getcwd(), self.directory)
            else:
                directory = self.directory
            value = os.path.join(directory, value)
        object.__dict__[name+'_'] = value # create shadow value
    
    def create_editor(self):
        from infobiotics.commons.traits.ui.qt4.relative_file_editor import RelativeFileEditor
        editor = RelativeFileEditor(
            absolute=self.absolute,
            auto_set=self.auto_set,
            directory=self.directory,
            directory_name=self.directory_name,
            entries=self.entries,
            exists=self.exists,
            exists_name=self.exists_name,
            filter=self.filter or [],
        )
        return editor
