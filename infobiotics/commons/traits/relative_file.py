#TODO update docstrings

import os
#from enthought.traits.api import BaseFile
from enthought.traits.api import BaseStr
from infobiotics.commons.api import can_read, can_write, can_write_file, can_execute
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
        empty_ok=False, empty_ok_name='',
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
            Implies directory exists (see can_write).
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
        TODO empty_ok, empty_ok_name,
                
        Default Value
        -------------
        *value* or ''
        
        """

        self.absolute = absolute
        
        if directory != '' and directory_name != '': #TODO necessary?
            raise ValueError("Please specify only 'directory' or 'directory_name', the value of '%s' named in the attribute directory_name will override '%s' in the attribute directory of the %s trait." % (directory_name, directory, self.__class__.__name__))
        self.directory = directory  
        self.directory_name = directory_name

        self.exists_name = exists_name
            
        if readable or executable:
            exists = True

        self.readable = readable
        self.writable = writable
        self.executable = executable

        self.empty_ok = empty_ok
        self.empty_ok_name = empty_ok_name

        super(RelativeFile, self).__init__(
#            value, filter, auto_set, entries, exists, **metadata # File
            value, **metadata # BaseStr
        )

        if isinstance(filter, (str, unicode)):
            filter = [filter]
        self.filter = filter
        self.auto_set = auto_set
        self.entries = entries
        self.exists = exists # why are these set here rather than in super?
        
#        self.editor = self.create_editor() # problem with circular imports - try not subclassing BaseFile instead.

#    info_text = 'a file name' # used if info() and full_info() are not defined
#
#    def info(self): # used if full_info() is not defined
#        return self.info_text

    def full_info(self, object, name, value):
        '''Calls _full_info with kind='file name' so that we can call 
        _full_info with kind='directory' for RelativeDirectory traits.'''
        return self._full_info(object, name, value, kind='file name')
        
    def _full_info(self, object, name, value, kind):
        '''Constructs an error string to be incorporated into a TraitError.'''
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
        
        if not os.path.isabs(value) or (self.directory != '' and not self.absolute):
#            info += '\n' # make tooltips easier to read # now done using wrap
            info += " in '%s'" % os.path.abspath(self.directory)
#            info += '\n'  

        return info
           
    def _set_directory_from_directory_name(self, object):
        ''' Factored out of _validate because it also used in post_setattr. '''
        if self.directory_name == '':
            return
        self.directory = getattr(object, self.directory_name)#, self.directory) #FIXME won't work for extended trait names (Range doesn't seem to do this either, maybe sync_value or _sync_values does?)
        
    def _set_exists_from_exists_name(self, object):
        if self.exists_name == '':
            return
        self.exists = getattr(object, self.exists_name)#, self.exists)

    def _set_empty_ok_from_empty_ok_name(self, object):
        if self.empty_ok_name == '':
            return
        self.empty_ok = getattr(object, self.empty_ok_name)#, self.empty_ok)

    def validate(self, object, name, value):
        '''Calls _validate with function=os.path.isfile so that we can call 
        _validate with function=os.path.isdir for RelativeDirectory traits.
        
        Also enables separate evaluation of value.
        ''' 
        return self._validate(object, name, value, function=os.path.isfile)

    def _validate(self, object, name, value, function):
        '''Validates that a specified value is valid for this trait.

        Note: The there is *not* a 'fast validator' version that performs 
        this check in C.
        '''
        value = super(RelativeFile, self).validate(object, name, value) # validate value using BaseStr's validator 

        # sync self.empty_ok from object
        self._set_empty_ok_from_empty_ok_name(object)
        if not self.empty_ok and value == '':#TODO use len(value).strip == 0 instead? 
            self.error(object, name, value)

        # sync self.directory from object
        self._set_directory_from_directory_name(object)

        # find executable files in system path if directory == '' and value is relative
        if self.directory == '':
            if not os.path.isabs(value):
                # value is relative
                try:
                    value = which(value)
                    # value is an executable file in system path
                except WhichError:
                    # value is not an executable file in system path
                    pass
        
        abspath = self._abspath(value)
        
        if self.absolute:
            value = abspath
#            #TODO is this a bad idea? 
#            # shouldn't value be absolute already for self.absolute to be useful
#            # or should validate return the valid form
#            '''
#            validate(self, object, name, value)
#            This method validates, coerces, or adapts the specified value as the 
#            value of the name trait of the object object. This method is called 
#            when a value is assigned to an object trait that is based on this 
#            subclass of TraitType and the class does not contain a definition for 
#            either the get() or set() methods. This method must return the original
#            value or any suitably coerced or adapted value that is a legal value 
#            for the trait. If value is not a legal value for the trait, and cannot 
#            be coerced or adapted to a legal value, the method should either raise 
#            a TraitError or call the error method to raise the TraitError on its 
#            behalf.        
#            '''

        # sync self.exists from object
        self._set_exists_from_exists_name(object)
        
        # sync self.empty_ok from object
        self._set_empty_ok_from_empty_ok_name(object)
        
        if not self.exists: # we don't care whether it exists 
            if self.writable is not None: # we care whether it can be written (created)
                # validate whether it is writable failing last
                if self.writable: # we care that it can be written
                    if function == os.path.isfile and not self.empty_ok: #FIXME? value should be a file if it is not empty
                        if can_write_file(abspath): # can we write the file?
                            return value # we can write it
                        # we can't write it so drop through to self.error()
                    else: # function == os.path.isdir # it should be a directory
                        if can_write(abspath): # can we write the directory?
                            return value # we can write it
                        # we can't write it so drop through to self.error()
                else: # we care that it can't be written
                    #TODO need to switch on function as above?
                    if not can_write(abspath): 
                        return value # we can't write it
                    # we can write it so drop through to self.error()
            else: # we don't care whether it can be written
                return value
        
        elif function(abspath): # we care whether it exists (isfile implies exists)
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
        self.error(object, name, value) # function returned False

    def post_setattr(self, object, name, value):
        '''Creates a shadow value (name + '_') with absolute path.'''
        # sync self.directory from object
        self._set_directory_from_directory_name(object) # only required here the first time the value is set
        # create shadow value
        abspath = self._abspath(value) 
#        print abspath
        object.__dict__[name + '_'] = abspath # setattr doesn't work so we have to mutate the object's dictionary instead
    
    def _abspath(self, value):
        '''Correctly returns the absolute and normalised path to the value: 
        with a trailing os.sep (e.g '/') if necessary. 
        
        os.path.abspath(path) prepends os.getcwd() if not os.path.isabs(path) 
        BUT strips trailing os.sep (i.e. where value == '') which is
        not desirable for can_write_file or other functions that depend on 
        os.path.split to determine if a path is a file or directory, so we must
        add it back if it would have been lost
        
        TODO how does this affect mapped drives?
        '''
        if os.path.isabs(value):
            return value
        else:
            abspath = os.path.abspath(os.path.join(self.directory, value)) # handles '..' or '.' in value 
            # concatenate lost os.sep if it would have been removed by os.path.abspath or os.path.normpath
            abspath = abspath + (os.sep if value == '' or value.endswith(os.sep) else '') # append lost separator for directories
            return abspath 
    
    def create_editor(self):
        from infobiotics.commons.traits.ui.qt4.relative_file_editor import RelativeFileEditor
        editor = RelativeFileEditor(
            absolute=self.absolute,
            auto_set=self.auto_set,
            directory=os.path.abspath(self.directory), # # must not be '' if RelativeFileEditor.directory(empty_ok=False) which it is by default
            directory_name=self.directory_name,
            entries=self.entries,
            exists=self.exists,
            exists_name=self.exists_name,
            empty_ok=self.empty_ok,
            empty_ok_name=self.empty_ok_name,
            filter=self.filter or [],
        )
        return editor
