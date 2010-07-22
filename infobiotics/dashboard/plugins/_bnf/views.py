from enthought.pyface.workbench.api import TraitsUIView
from enthought.traits.api import Str, Instance
from enthought.traits.ui.api import View, Item, TextEditor
from infobiotics.dashboard.plugins.bnf.actions import *
from infobiotics.dashboard.plugins.bnf.bnf_file_trees import *
from enthought.envisage.ui.workbench.workbench_window import WorkbenchWindow


# example folders and add new action

local_path = '/home/jvb/phd/eclipse/infobiotics/Infobiotics Dashboard/infobiotics/workbench/plugins/bnf/' #FIXME
example1 = local_path + 'modelRepository/pulsePropagation'
example2 = local_path + 'modelRepository/pulsePropagationRelay'
example3 = local_path + 'modelRepository/repressilator'

def example_folders(file_wrapper_class):
    return [
        file_wrapper_class(example1),
        file_wrapper_class(example2),
        file_wrapper_class(example3),
    ]

def add_new_folder():
    return [NullFileWrapper(''),]



# file trees    

class BNFFileTreeWithWindow(BNFFileTree):
    window = Instance(WorkbenchWindow)
    file_wrapper_class = Class
    editor_class = Class

    def _folder_list_default(self):
        return FolderList(folders=example_folders(self.file_wrapper_class)+add_new_folder())

    def open_object(self, object):
        self.window.workbench.edit(object.file, kind=self.editor_class)
    
    def new_folder(self, path):
        self.folder_list.folders.insert(1, self.file_wrapper_class(path))


class LPPFileTree(BNFFileTreeWithWindow):
    file_wrapper_class = LPPFileWrapper
    editor_class = LPPEditor


class SPSFileTree(BNFFileTreeWithWindow):
    file_wrapper_class = SPSFileWrapper
    editor_class = SPSEditor


class LATFileTree(BNFFileTreeWithWindow):
    file_wrapper_class = LATFileWrapper
    editor_class = LATEditor


class PLBFileTree(BNFFileTreeWithWindow):
    file_wrapper_class = PLBFileWrapper
    editor_class = PLBEditor


# views

class BNFView(TraitsUIView):
    category = 'BNF'
    file_tree_class = Class
    file_tree = Instance(BNFFileTreeWithWindow)

    def _file_tree_default(self):
        return self.file_tree_class(window=self.window)
    
    traits_view = View(
        Item('file_tree', show_label=False, style='custom')
    ) 


class LPPView(BNFView):
    id = 'LPPView'
    name = 'Lattice Population P systems'
    file_tree_class = LPPFileTree
    
    
class SPSView(BNFView):
    id = 'SPSView'
    name = 'Stochastic P systems'
    file_tree_class = SPSFileTree
    
    
class LATView(BNFView):
    id = 'LATView'
    name = 'Lattices'
    file_tree_class = LATFileTree


class PLBView(BNFView):
    id = 'PLBView'
    name = 'Module libraries'
    file_tree_class = PLBFileTree
    