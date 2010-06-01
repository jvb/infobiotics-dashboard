from infobiotics.common.api import ParamsView, MenuBar, file_menu
from infobiotics.commons.api import can_read, mkdir_p
import os
from enthought.traits.api import (
    Property, Str, List, Unicode, Bool, Instance, TraitError,
)
from enthought.pyface.api import FileDialog, OK
from enthought.traits.ui.api import View, Item, Group
from infobiotics.commons.traits.ui.api import HelpfulController
from infobiotics.common.params_preferences_helper import ParamsPreferencesHelper
from enthought.preferences.api import get_default_preferences

#from enthought.traits.ui.fixed_file_dialog import (
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

class ParamsHandler(HelpfulController):
    
    def traits_view(self):
        return self.get_traits_view(ParamsView)
    
    def get_traits_view(self, ViewClass):
        help_menu = self.get_help_menu() # see HelpfulController
        menubar = MenuBar(
            file_menu,
            help_menu,
        ) if help_menu is not None else MenuBar(
            file_menu,
        ) 
        return ViewClass(
            self.params_group,
            id = self.id,
            menubar = menubar,
        ) 
        
    params_group = Instance(Group) 
    
    def _params_group_default(self):
        raise NotImplementedError

    id = Str(desc='the ID to use when preserving window size and position')
    
    title = Property(Str, depends_on='model._params_file, model._cwd')

    def _get_title(self):
        path = self.model._params_file
        if len(path) > 0:
            dirname, basename = os.path.split(path)
            dirname = os.path.relpath(dirname, self.model._cwd)
            if dirname == '.':
                return '%s %s' % (self.model._params_program_name, basename)
            else:
                return '%s %s (%s)' % (self.model._params_program_name, basename, dirname)
            return 
        else:
            return self.model._params_program_name

    def _title_changed(self, title):
        if self.info is not None and self.info.initialized:
            if self.info.ui is not None:
                self.info.ui.title = title
#            else:
#                print self.__class__.__name__
            
    def init(self, info):
        info.ui.title = self.title
        self.load_preferences()
        self.status = "Please ensure the current working directory is correct."

    def load_preferences(self):
        helper = ParamsPreferencesHelper(
            preferences=get_default_preferences(),
            preferences_path=self.model._preferences_path,
        )
#        print get_default_preferences().filename
        # restoring self.model._cwd here, moved from Params._cwd_default
        _cwd = helper._cwd
        try:
            helper._cwd = _cwd # ensure helper checks _cwd is a file that exists, etc., rather than model or _cwd's editor 
            self.model._cwd = _cwd
        except TraitError:
            self.model._cwd = os.getcwd()

    def save_preferences(self):
        preferences = get_default_preferences()
        preferences.set(self.model._preferences_path + '._cwd', self.model._cwd)
        preferences.flush()

    def closed(self, info, is_ok): # must return True or else window is unscloseable!
        if is_ok:
            self.save_preferences()
        return True

    status = Str

    def load(self, info):
        ''' Load the traits of an experiment from a .params XML file. '''
        params = info.object
        title = 'Load %s parameters' % params._parameters_name
        file_name = self.get_load_file_name_using_PyFace_FileDialog(title)
#        file_name = self.get_load_file_name_using_Traits_FileDialog(title)
        if file_name is not None:
            params.load(file_name)
            self.status = "Loaded '%s'." % file_name
        
    def get_load_file_name_using_PyFace_FileDialog(self, title):
        fd = FileDialog(
            wildcard=self.wildcard, 
            title=title,
            default_filename = self.model._params_file,
            default_directory = self.model._cwd_
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
            self.status = "Saved '%s'." % file_name
                                   
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
    