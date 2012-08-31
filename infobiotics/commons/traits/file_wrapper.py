''' Attempts to overcome the problem of 'children' in 'enthought.io.api.File'
objects being None instead of [] when there are no children (i.e. the file is
not a directory).
    
Solving this problem enables the wrapper class to be used a TreeNode type for a
TreeEditor.

Note: TreeEditor must operate on an Instance trait. 
      
'''


from enthought.io.api import File
from enthought.traits.api import HasTraits, Str, Instance, List, Any#, This


class FileWrapper(HasTraits):
    file = Instance(File)
    children = List(Any)
    
    def __init__(self, path, *args, **kwargs):
        super(HasTraits, self).__init__(*args, **kwargs)
        self.file = File(path) # triggers _file_changed

    def _file_changed(self, file):
        if file.children is not None:
            self.children = [self.__class__(child.path) for child in file.children]
    

#class FileWrapper(File):
#    def _children_changed(self, children):
#        if children is None:
#            self.children = []
#        else:
#            self.children = [FileWrapper(child.path) for child in children]


#class FileWrapper(File):
#    children_ = Property(depends_on='children')
#    @cached_property
#    def _get_children_(self):
#        if self.children is None:
#            return []
#        else:
#            return self.children



if __name__ == '__main__':
    print FileWrapper('../shared').children
    print FileWrapper('../shared').children[0].children 
