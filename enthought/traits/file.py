import os
from enthought.traits.api import BaseFile
from common.api import can_read, can_write, can_execute#, path_join_overlapping, split_directories

class File(BaseFile):
    """ Defines a trait whose value must be the name of a file (which can be 
    relative to a directory other than the current working directory.)
    
    """
    def __init__(self, value='', filter=[], auto_set=False, entries=0, 
                 exists=False,  
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
        
        if directory != '' and directory_name != '':
            raise ValueError, "Please specify only 'directory' or 'directory_name', the value of '%s' named in the attribute directory_name will override '%s' in the attribute directory of the %s trait." % (directory_name, directory, self.__class__.__name__)
        
        self.directory = directory if directory != '' else os.getcwd() # can't set this in class definition: it will always be the location of the module  
        self.directory_name = directory_name

        self.absolute = absolute

        # make exists True if readable or executable are not None
        if (readable is not None or executable is not None) and not exists:
            exists = True

        self.readable = readable
        self.writable = writable
        self.executable = executable

        super(File, self).__init__(value, filter, auto_set, entries, exists, **metadata)

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
        
    def _full_info(self, object, name, value, kind='file name '):
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
        
        if self.directory != '':
#            info += '\n' # make tooltips easier to read # now done using wrap
            info += "in '%s'" % os.path.abspath(self.directory)
#            info += '\n'  
        
        return info
           

    def validate(self, object, name, value):
        ''' Calls _validate so that we can reuse _validate for Directory 
        traits. 
        
        '''
        return self._validate(object, name, value)

    def _set_directory_from_directory_name(self, object):
        ''' Factored out of _validate because it also used in post_setattr. '''
        if self.directory_name != '':
#            #TODO will this be different for the editor? if directory_name = 'controller.directory' for instance.
#            # coerce directory_name
#            if not directory_name == '':
#                if not directory_name.startswith(('object.','controller.','model.')):
#                    directory_name = 'object.' + directory_name
            directory = getattr(object, self.directory_name) #FIXME won't work for extended trait names (Range doesn't seem to do this either, maybe sync_value or _sync_values does?)
#            print 'object.%s =' % self.directory_name, directory
            
            # update self.directory here because we didn't know object in __init__
            if directory != '':
                self.directory = directory
#                print 'self.directory =', self.directory

    def _validate(self, object, name, value, function=os.path.isfile):
        """ Validates that a specified value is valid for this trait.

        Note: The there is *not* a 'fast validator' version that performs 
        this check in C.
        
        if directory = '/tmp'
        and abspath = '/tmp/file'
        return 'file'
        """
        value = super(BaseFile, self).validate(object, name, value) # validate value using BaseStr's validator 
#        print 'value =', value
        
        self._set_directory_from_directory_name(object)
        
        directory = self.directory
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
        
#        print 'self.exists =', self.exists
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
#                print 'self.readable =', self.readable 
                # validate whether it is readable failing fast 
                if self.readable: # we care that it can be read
                    if not can_read(abspath): # we can read it
                        self.error(object, name, value)
                else: # we care that it can't be read
                    if can_read(abspath): # we can read it
                        self.error(object, name, value)
            if self.writable is not None: # we care whether it can be written
#                print 'self.writable =', self.writable
                # validate whether it is writable failing fast
                if self.writable: # we care that it can be written
                    if not can_write(abspath): # we can't write it
                        self.error(object, name, value)
                else: # we care that it can't be written
                    if can_write(abspath): # we can write it
                        self.error(object, name, value)
            if self.executable is not None: # we care whether it can be executed
#                print 'self.executable =', self.executable
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
        ''' Sets self.abspath. '''
#        if value == '':
#            self.abspath = value
#        elif not os.path.isabs(value):

        # only required here the first time the value is set
        self._set_directory_from_directory_name(object)
        
        if not os.path.isabs(value):
            if not os.path.isabs(self.directory):
                directory = os.path.join(os.getcwd(), self.directory)
            else:
                directory = self.directory
            self.abspath = os.path.join(directory, value)
        else:
            self.abspath = value
#        print 'self.abspath =', self.abspath
    
    def create_editor(self):
        from enthought.traits.ui.qt4.file_editor2 import FileEditor
        editor = FileEditor(
            filter=self.filter or [],
            auto_set=self.auto_set,
            entries=self.entries,
            directory=self.directory,
            directory_name=self.directory_name,
            absolute=self.absolute,
        )
        return editor



def test_trait():
    from enthought.traits.api import HasTraits, Str
    
#    os.chdir('/tmp/permissions_test')
    
    class Test(HasTraits):
        
        different_directory = Str('/tmp/permissions_test/writable')
#        different_directory = Str('writable') #TODO failed?: uses os.path.join(os.getcwd(), self.different_directory) even if directory is set
        
        file = File('default',
#            directory = '', # passed: uses os.getcwd()
            directory = '/tmp/permissions_test', # passed: uses'/tmp/permissions_test' 
            
#            directory_name = '', # passed: uses directory
            directory_name = 'different_directory', # passed: uses different_directory over directory, raise AttributeError when object has no attribute named by directory_name 

#            exists = False, # passed: uses nonexistent file as value #TODO should this fail if an existing file is set? (regular File traits don't fail) [could do exists=None like readable, etc.]
#            exists = True, # passed: raises error if value doesn't exist otherwise returns value 

#            absolute = False, # passed: returns value
#            absolute = True, # passed: returns abspath instead of value

#            readable = None, # passed: doesn't make exists = True 
#            readable = True, # passed: raises error if value is not readable and makes exists = True
#            readable = False, # passed: raises error if value is executable and makes exists = True

#            writable = None, # passed: doesn't check if value is writable regardless of exists
#            writable = True, # passed: raises error if value is not writable (and exists = False)
#            writable = False, # passed: raises error is value is writable (and exists = False)

#            executable = None, # passed: doesn't make exists = True
#            executable = True, # passed: raises error if value is not executable and makes exists = True
#            executable = False, # passed: raises error if value is executable and makes exists = True

            auto_set = True,
        )
        
    t = Test()
    
    print 't.file =', t.file
    print
    
    def test_t(file_name):
#        print 'test_t(%s)' % file_name
        t.file = file_name
        print 't.file =', t.file
        print 
    
    test_t('readonly')
#    test_t('writable')
#    test_t('executable')
#    test_t('unreadable')

#    t.configure_traits()
        

def test_implicit_editor():
    from enthought.traits.api import HasTraits
    from enthought.traits.directory import Directory
    
    os.chdir('/tmp') # works when directory is not set or directory is relative
    
    class Test(HasTraits):
        file = File('module1.sbml',
            desc='tooltip',
            auto_set = True,
            exists = True,
            directory_name = 'other_directory',
            absolute = True,
        )
        other_directory = Directory('/home/jvb/phd/eclipse/infobiotics/dashboard/infobiotics/mcss/test/models', 
            auto_set=True,
            exists=True,
        )
        
    Test().configure_traits()


#def test_explicit_editor():
#    from enthought.traits.api import HasTraits, Str, Directory
#    from enthought.traits.ui.api import View, Item
#    from enthought.traits.ui.qt4.file_editor2 import FileEditor
#    
#    os.chdir('/tmp/permissions_test') # works when directory is not set or directory is relative
#    
#    class Test(HasTraits):
#        file = File(
#            auto_set = True,
#            exists = True,
#            directory = 'readonly',
#        )
#
#    traits_view = View(
#        Item('file',
#            editor=FileEditor(
#                directory = 'writable',
#            ),
#        ),
#    )
#        
#    Test().configure_traits()

def test_explicit_editor():
    from enthought.traits.api import HasTraits, Str
    from enthought.traits.ui.api import View, Item
    from enthought.traits.ui.qt4.file_editor2 import FileEditor
    from enthought.traits.directory import Directory
    
    os.chdir('/tmp/permissions_test') # works when directory is not set or directory is relative
    
    class Test(HasTraits):
        file = File(
            auto_set = True,
            exists = True,
#            directory = 'readonly',
        )
        
        other_directory = Directory('/tmp') 
        
        traits_view = View(
            Item('file',
                editor=FileEditor(
                    directory_name = 'other_directory',
                ),
            ),
        )
        
    Test().configure_traits()



def test_explicit_editor2(): 
    from enthought.traits.api import HasTraits, Property, Str, Button, Instance, Directory
    from enthought.traits.ui.api import View, Item
    from enthought.traits.ui.qt4.file_editor2 import FileEditor
    
    file_editor2 = FileEditor(
#        directory='/tmp',
        directory_name='directory',
    )
    
    class Test(HasTraits):
        directory = Directory('/home/jvb/phd/eclipse/infobiotics/dashboard/infobiotics/mcss/test/models', auto_set=True, exists=True)
        
        def _directory_changed(self):
            print 'Test._directory_changed(self):', self.directory
        
        def _directory_name_changed(self):
            print 'Test._directory_name_changed(self):', self.directory_name            
    
        file = File('module1.sbml',
            desc='tooltip',
            auto_set=True,
            exists=True,
    #        readable=False,
    #        writable=True,
    #        executable=False,
    #        absolute=True,
    #        directory='/home/jvb/phd/eclipse/infobiotics/dashboard/infobiotics/mcss/test/models',
#            directory_name='directory',
    #        directory_name='object.directory',
        )
        
        value = Property(depends_on='file')
        
        def _get_value(self):
            return self.file
        
        cwd = Button
        
        def _cwd_fired(self):
            self.directory = os.getcwd() 

        file2 = File(directory='/home/jvb')

        traits_view = View( 
            'directory',
#            'file',
            'value',
            'cwd',
#            'file2',
            Item('file2', 
                editor=file_editor2
            ),
            'editor.directory',
            'editor.directory_name',
            
        )
        
    t = Test()
    
#    file_editor2.directory = '/usr'
    
    t.configure_traits(context={'object':t, 'editor':file_editor2})


if __name__ == '__main__':
#    test_trait()
    test_implicit_editor()
#    test_explicit_editor()
    