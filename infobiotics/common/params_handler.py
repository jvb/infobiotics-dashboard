from commons.api import can_read, mkdir_p
import os
os.environ['ETS_TOOLKIT']='qt4'
from enthought.traits.api import Property, Str, List, Unicode, Bool
from enthought.pyface.api import FileDialog, OK

from enthought.traits.ui.api import Controller, View, Item
#from enthought.traits.ui.file_dialog2 import (
#    MFileDialogModel, FileInfo, TextInfo, OpenFileDialog
#)
#
#class CopyInputFilesWithRelativePathsExtension(MFileDialogModel):
##    is_fixed = True # only if inheriting from MFileDialogView or MFileDialogExtension, which is probably wrong 
#    copy = Bool(True, desc='whether to copy input files with relative paths to new directory')
#    copy_enabled = Bool(False, desc='whether copy is enabled (if old directory != new directory)')
##    copy_enabled = Property(Bool, depends_on='file_name') # encouraged to use Property but can't get old file_name that way
##    @cached_property
##    def _get_copy_enabled(self):
##        print os.path.dirname(self.file_name)
##        return False
#    def _file_name_changed(self, old, new):
#        if old != '':
#            if os.path.dirname(new) != os.path.dirname(old):
#                self.copy_enabled = True 
#            else:
#                self.copy_enabled = False
#    
#    view = View(
#        Item('copy', label='Copy required files with relative paths to new directory?', enabled_when='object.copy_enabled'),
#    )

class ParamsHandler(Controller):

    title = Property(Str, depends_on='model._params_file, model._cwd')

    def _get_title(self):
        path = self.model._params_file
        if len(path) > 0:
            dirname, basename = os.path.split(path)
            dirname = os.path.relpath(dirname, self.model._cwd)
            if dirname == '.':
                return '%s %s' % (self.model._parameters_name, basename)
            else:
                return '%s %s (%s)' % (self.model._parameters_name, basename, dirname)
            return 
        else:
            return self.model._parameters_name

    def _title_changed(self, title):
        if self.info is not None and self.info.initialized:
            self.info.ui.title = title
            
    def init(self, info):
        info.ui.title = self.title 
    
    def load(self, info):
        ''' Load the traits of an experiment from a .params XML file. '''
        params = info.object
        title = 'Load %s parameters' % params._parameters_name
        file_name = self.get_load_file_name_using_PyFace_FileDialog(title)
#        file_name = self.get_load_file_name_using_Traits_FileDialog(title)
        if file_name is not None:
            params.load(file_name)
        
    def get_load_file_name_using_PyFace_FileDialog(self, title):
        fd = FileDialog(
            wildcard=self.wildcard, 
            title=title,
            default_filename = self.model._params_file,
        )
        if fd.open() == OK:
            return fd.path
        return None
               
    def get_load_file_name_using_Traits_FileDialog(self, title):
        fd = OpenFileDialog(
            file_name = self.model._params_file,
            filter = self.filter,
            title = title,
            id = 'ParamsHandler.get_load_file_name_using_Traits_FileDialog',
        )
        if fd.edit_traits(view='open_file_view', parent=self.info.ui.control).result: # if kind='modal' here fd.file_name never changes!
            return fd.file_name
        return None

    copy = Bool(False, desc='whether to copy required files with relatives paths to new save directory (set by eponymous FileDialog extension)')
#    copy = Bool(True) #TODO remove after adding file_dialog2.py

    def save(self, info):
        ''' Saves the traits of experiment to a .params XML file. '''
        params = info.object
        title='Save %s parameters' % params._parameters_name
        file_name = self.get_save_file_name_using_PyFace_FileDialog(title)
#        file_name = self.get_save_file_name_using_Traits_FileDialog(title)
        if file_name is not None:
            if self.copy: #TODO prompt to overwrite existing files in new directory
                pass
            params.save(file_name, force=True, copy=self.copy) # user will have been prompted to overwrite by the GUI
                                   
    def get_save_file_name_using_PyFace_FileDialog(self, title):
        fd = FileDialog(
            action='save as', 
            wildcard=self.wildcard,
            title = title,
            default_directory = os.path.dirname(self.model._params_file),
        )
        if fd.open() == OK:
            return fd.path
        return None
    
    def get_save_file_name_using_Traits_FileDialog(self, title):
        fd = OpenFileDialog(
            is_save_file = True,
            extensions = [
                CopyInputFilesWithRelativePathsExtension(), 
                FileInfo(),
                TextInfo(),
            ],
            file_name = self.model._params_file,
            filter = self.filter,
            title = title,
            id = 'ParamsHandler.get_save_file_name_using_Traits_FileDialog',
        )
        if fd.edit_traits(view='open_file_view', parent=self.info.ui.control).result: # if kind='modal' here fd.file_name never changes!
            # get whether to copy input files with relative paths or not
            for extension in fd.extensions:
                if isinstance(extension, CopyInputFilesWithRelativePathsExtension):
                    self.copy = extension.copy if extension.copy_enabled else False
            return fd.file_name
        return None
            
    filters = [ # used to create wildcard and filter traits for FileDialog and OpenFileDialog respectively
        ('Experiment parameters', ['*.params']), 
        ('All files', ['*']),
    ]

    filter = List(Unicode) # for OpenFileDialog

    def _filter_default(self):
        filter = []
#        # for QFileDialog.setNamedFilters(filter)
#        for f in self.filters:
#            filter.append('%s (%s)' % (f[0], ' '.join(f[1])))
        # for QDirModel.setNamedFilters(filter)
        filter.append('%s' % ' '.join(self.filters[0][1]))

        return filter

    wildcard = Str(desc='an appropriate wildcard string for a WX or Qt open and save dialog looking for params files.') # for FileDialog

    def _wildcard_default(self):
        try:
            import os
            toolkit = os.environ['ETS_TOOLKIT']
        except KeyError:
            toolkit = 'wx'
        wildcard = ''
        if toolkit == 'qt4':
            for i, w in enumerate(self.filters):
                wildcard += FileDialog.create_wildcard(w[0], w[1])
        else: # assume os.environ['ETS_TOOLKIT'] == ('wx' and not 'null')
            for i, w in enumerate(self.filters):
                # wx: 'py and test (*.py *.test)|*.py;*.test|\ntest (*.test)|*.test|\npy (*.py)|*.py'#|
                w2 = ';'.join(w[1])
                wildcard += '%s (%s)|%s' % (w[0], w2, w2)
                if i < len(self.filters) - 1:
                    wildcard += '|'
        return wildcard
    
#    # set _dirty on model and * on title ---  
#    # self.model._dirty == info.object._dirty == Params()._dirty
#    # http://code.enthought.com/projects/traits/docs/html/TUIUG/handler.html
#
#    def setattr(self, info, object, name, value):
#        super(ParamsController, self).setattr(info, object, name, value)
#        self.model._dirty = True
##        if name in self.model.parameter_names():
##            self.model._dirty = True
#        
#    def object__dirty_changed(self, info):
#        if info.initialized:
#            info.ui.title += '*'
#        else:
#            self.model._dirty = False


if __name__ == '__main__':
    execfile('params.py')
    