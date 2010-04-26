from infobiotics.shared.api import \
    Controller, Property, Str, FileDialog, OK, os, List, Unicode, Bool #, Property, cached_property    
from enthought.traits.ui.api import Controller, View, Item
from enthought.traits.ui.file_dialog2 import (
    MFileDialogModel, FileInfo, TextInfo, OpenFileDialog
)

class CopyInputFilesWithRelativePathsExtension(MFileDialogModel):
#    is_fixed = True # only if inheriting from MFileDialogView or MFileDialogExtension, which is probably wrong 
    copy = Bool(True, desc='whether to copy input files with relative paths to new directory')
    copy_enabled = Bool(False, desc='whether copy is enabled')
#    copy_enabled = Property(Bool, depends_on='file_name') # encouraged to use Property but can't get old file_name that way
#    @cached_property
#    def _get_copy_enabled(self):
#        print os.path.dirname(self.file_name)
#        return False
    def _file_name_changed(self, old, new):
        if old != '':
            if os.path.dirname(new) != os.path.dirname(old):
                self.copy_enabled = True 
            else:
                self.copy_enabled = False
    
    view = View(
        Item('copy', label='Copy required files with relative paths to new directory?', enabled_when='object.copy_enabled'),
    )


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
        title = 'Load %s parameters' % self.model._parameters_name
#        file_name = self.get_load_file_name_using_PyFace_FileDialog(title)
        file_name = self.get_load_file_name_using_Traits_FileDialog(title)
        if file_name is not None:
            info.object.load(file_name)
        
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
            id = 'infobiotics.shared.params_handler:ParamsHandler.get_load_file_name_using_Traits_FileDialog',
        )
        if fd.edit_traits(view='open_file_view', parent=self.info.ui.control).result: # if kind='modal' here fd.file_name never changes!
            return fd.file_name
        return None

    def save(self, info):
        ''' Saves the traits of experiment to a .params XML file. '''
        title='Save %s parameters' % self.model._parameters_name
#        file_name = self.get_save_file_name_using_PyFace_FileDialog(title)
        file_name = self.get_save_file_name_using_Traits_FileDialog(title)
        if file_name is not None:
            result = info.object.save(file_name, force=True) # user will have been prompted to overwrite by the GUI
            if result and self.copy: #TODO
                # for each file in parameter_names with exists=True created directories in os.path.dirname(file_name) and copy abspath to there
                for name in self.model.parameter_names():
                    trait = self.model.base_trait(name)
                    type = trait.trait_type.__class__.__name__
                    if type == 'File':
                        handler = trait.handler
                        exists = handler.exists
                        if exists:
                            print 'new params file', file_name
                            print os.path.dirname(file_name)
                            print getattr(self.model, name)
                            print handler.directory
                            print handler.abspath
                            print os.path.relpath(handler.abspath, handler.directory) 
                    
                    
                    
                 
            
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
            id = 'infobiotics.shared.params_handler:ParamsHandler.get_save_file_name_using_Traits_FileDialog',
        )
            
        if fd.edit_traits(view='open_file_view', parent=self.info.ui.control).result: # if kind='modal' here fd.file_name never changes!
            
            # get whether to copy input files with relative paths or not
            for extension in fd.extensions:
                if isinstance(extension, CopyInputFilesWithRelativePathsExtension):
                    self.copy = extension.copy

            return fd.file_name
        return None
        
    copy = Bool(False)
        
            
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
    

if __name__ == '__main__':
    execfile('params.py')
    