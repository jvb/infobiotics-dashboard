from enthought.traits.api import HasTraits, TraitError
from enthought.traits.ui.api import View#, Item#, Handler
#from infobiotics.commons.traits.relative_file import RelativeFile
from infobiotics.commons.traits.relative_directory import RelativeDirectory
#from infobiotics.core.traits.params_relative_directory import ParamsRelativeDirectory
from infobiotics.core.traits.params_relative_file import ParamsRelativeFile

class Params(HasTraits):
    
#    file = File(exists=True)
#    directory = Directory(exists=True)
    
#    relative_file = RelativeFile#(exists=True)
#    relative_directory = RelativeDirectory#(exists=True)
    directory = RelativeDirectory(absolute=True, auto_set=True, writable=True, exists=True, desc='the location file paths can be relative to.') # writable alone does not implies exists
    
    #ParamsRelativeFile = RelativeFile(directory_name='directory', auto_set=True)
#    params_relative_directory = ParamsRelativeDirectory(empty_ok=True)
#    params_relative_file = ParamsRelativeFile(empty_ok=True, exists=True)
#    params_relative_directory = ParamsRelativeDirectory(writable=True)
#    params_relative_file = ParamsRelativeFile(writable=True)
#    params_relative_directory = ParamsRelativeDirectory(writable=True, empty_ok=True)
#    params_relative_file = ParamsRelativeFile(writable=True, empty_ok=True)
    readable = ParamsRelativeFile(readable=True, desc='readable')
    executable = ParamsRelativeFile(executable=True)
    writable = ParamsRelativeFile(writable=True)
    
    view = View(
        'directory',
#        'file',
#        'relative_directory',
#        'relative_file',
#        'params_relative_directory',
#        'params_relative_file',
        'readable',
        'writable',
        'executable',
        resizable=True,
        id='id',
        buttons=['OK'],
    )

    def _directory_changed(self, old, new):
#        '''Show what happens when directory changed.'''
        print "self.directory =  '%s' (previously '%s')" % (new, old),
#        print "self.directory_ = '%s'" % self.directory_
#        for t in traits:
#            if isinstance(self.trait(t).handler, (RelativeFile, RelativeDirectory)): # RelativeDirectory not strictly needed as it is a subclass of RelativeFile 
#                print "self.%s = '%s'" % (t, getattr(self, t))
#        print
        
        # do this in a handler?
        '''
        1) directory changes from '/home/jvb/dashboard' to '/home/jvb' 
        invalidating _params_relative_file, can prompt to either
            * how can I find out if traits values are invalid? *
            1.1) copy files references in parameters to new
            1.2) rewrite paths relative to new directory
            1.3) rewrite path as absolute to old directory
            1.4) do nothing
        
        '''
        # the relative file/directory traits which are invalidated by directory changing
        invalids = []
        for t in self.parameter_names():
            if isinstance(self.trait(t).handler, ParamsRelativeFile):# RelativeDirectory not needed as it is a subclass of RelativeFile 
                try:
                    self.trait(t).handler.validate(self, t, getattr(self, t))
                except TraitError, e:
                    invalids.append(t)
        if len(invalids) > 0:
            print 'invalidated', [invalid for invalid in invalids]
#
#
#    def _params_relative_directory_changed(self, old, new):
#        print "self.params_relative_directory =  '%s' (previously '%s')" % (new, old),
#        print "self.params_relative_directory = '%s'" % self.params_relative_directory_
#        print
#    
#    def _params_relative_file_changed(self, old, new):
#        print "self.params_relative_file =  '%s' (previously '%s')" % (new, old),
#        print "self.params_relative_file_ = '%s'" % self.params_relative_file_
#        print
            
    def parameter_names(self):
        return 'readable', 'writable', 'executable'
        #    'relative_directory',
        #    'relative_file',
        #    'params_relative_directory',
        #    'params_relative_file',
            
    def __str__(self):
        s = ''
        s += '\n'.join(
            ["%s = %s" % (parameter_name, getattr(self, parameter_name)) + ("(%s)" % self.trait(parameter_name).handler.desc if self.trait(parameter_name).handler.desc is not None else "") for parameter_name in self.parameter_names()]
        )
        return s


def main():
    params = Params(
        readable='readable',
        executable='executable',
#        writable='writable/writable',
        writable='readonly/writable',
    )

#    attrs = ('directory', 'directory_name') 
#    for a in attrs:
##        print a 
#        for i in traits:
#            print '%s.%s' % (i, a), '=', "'%s'" % getattr(t.trait(i).handler, a)
#        print 

    import os, tempfile
    temp_file_dir = os.path.dirname(tempfile.NamedTemporaryFile(delete=True).name) 
    temp_file_name = 'test'
    temp_file_path = os.path.join(temp_file_dir, temp_file_name)
    if os.path.exists(temp_file_path):
        print "loading traits from '%s'" % temp_file_path
        print
#    params.configure_traits(temp_file_path)
#    print params
#    print params.trait('readable').handler.exists
    params.configure_traits()
    
    
if __name__ == '__main__':
    main()
