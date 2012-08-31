import os
#os.environ['ETS_TOOLKIT']='qt4'
from traits.api import HasTraits, Str, List, Instance
from traitsui.api import View, Item, TreeEditor, TreeNode
from infobiotics.shared.file_wrapper import FileWrapper
from pyface.api import DirectoryDialog, OK
from apptools.io.api import File


class BNFFileWrapper(FileWrapper):
    extension = Str('Only use subclasses of BNFFileWrapper.')
    
    def _children_changed(self, children):
        ''' Ensures children excludes any files that do not have the extension 
        specified by this wrapper and any folders that do not contain files
        that do.
        
        '''
        self.children = [
            child for child in children if 
                child.has_files_of_correct_extension()
        ]

    def has_files_of_correct_extension(self):
        ''' Returns true if 'file' is a file of the correct extension or is a 
        folder containing a file of the correct extension, otherwise false.
        
        '''
        if self.file.is_file:
            if self.file.ext.lower() == self.extension.lower():
                return True
            else:
                return False
        elif self.file.is_folder:
            found = False
            for child in self.children:
                if child.has_files_of_correct_extension():
                    found = True
            return found


class LPPFileWrapper(BNFFileWrapper):
    extension = '.lpp'

class SPSFileWrapper(BNFFileWrapper):
    extension = '.sps'

class LATFileWrapper(BNFFileWrapper):
    extension = '.lat'

class PLBFileWrapper(BNFFileWrapper):
    extension = '.plb'


class NullFileWrapper(BNFFileWrapper):
    pass
    
no_view = View()

label_view = View(
    Item('label')
)


class NullFileWrapperTreeNode(TreeNode):
    node_for=[NullFileWrapper]
    menu=False
    label='=Add new folder...'
    children=''
    view=no_view
        

from traitsui.menu import Menu, Separator
#from traitsui.qt4.tree_editor import \
#    NewAction, CopyAction, CutAction, PasteAction, DeleteAction, RenameAction
    
class BNFFileWrapperTreeNode(TreeNode):
    node_for=[LPPFileWrapper, SPSFileWrapper, LATFileWrapper, PLBFileWrapper]
    label='file.name'
    children='children'
    view=no_view
    copy=False
#    menu=False
    menu=Menu(
#        NewAction,
        Separator(),
#        DeleteAction,
    )
    tooltip='file.absolute_path'
    icon_path='',
    icon_item='',
    icon_open='',
    icon_group='',
    delete_me=True


class FolderList(HasTraits):
    folders = List(BNFFileWrapper)
    

class FolderListTreeNode(TreeNode):
    node_for=[FolderList]
    label='=Should be hidden with TreeEditor(hide_root=True,...'
    children='folders'
    view=no_view
    delete=True


def bnf_tree_node_definitions():
    ''' Returns a list of TreeNode instances in an appropriate order.
    
    Should ensure that the order of TreeNode definitions is correct when node
    types are related to each other.
        
    '''
    return [
        FolderListTreeNode(),
        BNFFileWrapperTreeNode(),
        NullFileWrapperTreeNode(),
    ]


bnf_tree_editor = TreeEditor(
    nodes=bnf_tree_node_definitions(),
    auto_open=3,
    editable=False,
#    selected='selected',
    on_dclick='object.dclicked',
    show_icons=False,
#    icon_size=(32,32),
    lines_mode='on',
    hide_root=True,
)


class BNFFileTree(HasTraits):
    folder_list = Instance(FolderList)
    selected = Instance(BNFFileWrapper)
    
    traits_view = View(
        Item('folder_list', 
            show_label=False,
            editor=bnf_tree_editor,
        ),
    )

    def dclicked(self, object):
        if object.file.is_file:
            self.open_object(object)
        if object in self.folder_list.folders:
            dd = DirectoryDialog()
            if dd.open() == OK:
                if isinstance(object, NullFileWrapper):
                    self.new_folder(dd.path)
                elif object.file.is_folder:
                    object.file = File(dd.path)
    
    def open_object(self, object):
        raise NotImplementedError
        
    def new_folder(self, path):
        raise NotImplementedError
        

class BNFFileTreeExample(BNFFileTree):
    folder_list = FolderList(
        folders=[
#            NullFileWrapper('hello'),
#            LATFileWrapper('modelRepository/pulsePropagation'),
#            LATFileWrapper('modelRepository/pulsePropagationRelay'),
#            LATFileWrapper('modelRepository/repressilator'),
        ]
    )

    def open_object(self, object):
        #TODO open in appropriate bnf_editor
        raise NotImplementedError
    
    def new_folder(self, path):
        self.folder_list.folders.insert(1, LATFileWrapper(path))
        


if __name__ == '__main__':
    BNFFileTreeExample().configure_traits()
    