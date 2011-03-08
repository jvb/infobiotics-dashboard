from infobiotics.core.views import ParamsView, file_menu
from enthought.traits.ui.menu import Menu, Action, MenuBar
#from infobiotics.commons.api import can_read, mkdir_p
import os
from enthought.traits.api import Str, List, Unicode, Instance, Property, Bool, cached_property
from enthought.pyface.api import OK
from enthought.pyface.ui.qt4.file_dialog import FileDialog
from enthought.traits.ui.api import Group#, View, Item, 
from infobiotics.commons.traits.ui.api import HelpfulController
from enthought.preferences.ui.api import PreferencesPage, PreferencesManager

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

tools_menu = Menu(
    Action(
        name='&Preferences',
        action='edit_preferences',
        tooltip='TODO',
        enabled_when='len(controller._preferences_pages) > 0',
    ),
    name='&Tools'
)

class ParamsHandler(HelpfulController):
    
    params_group = Instance(Group)
    
    def _params_group_default(self):
        raise NotImplementedError

    id = Str(desc='the ID to use when preserving window size, position and monitor')
    
    def get_traits_view(self, ViewClass):
        help_menu = self.get_help_menu() # see HelpfulController
        menubar = MenuBar(
            file_menu,
            tools_menu,
            help_menu,
        ) if help_menu is not None else MenuBar(
            file_menu,
            tools_menu,
        ) 
        return ViewClass(
            self.params_group,
            id=self.id,
            menubar=menubar,
        ) 
    
    def traits_view(self): # overridden in ExperimentHandler
        return self.get_traits_view(ParamsView)

    status = Str
    
    def init(self, info):
#        self.status = "Please ensure the current working directory is correct." #TODO
        info.ui.title = self.title
        
    title = Property(Str, depends_on='model._params_file, model.directory')

    @cached_property
    def _get_title(self):
        titles = [self.model.executable_name]
        path = self.model._params_file
        if len(path) > 0:
            dirname, basename = os.path.split(path)
            dirname = os.path.relpath(dirname, self.model.directory)
            if dirname == '.':
                titles += [basename]
            else:
                titles += [basename, '(%s)' % dirname]
        return ' '.join(titles)

    def _title_changed(self, title):
        if self.info is not None and self.info.initialized:
            if self.info.ui is not None:
                self.info.ui.title = title
    
    def object__dirty_changed(self, info):
        if info.initialized:
            if info.object._dirty:
                info.ui.title = self.title + '*'
            else:
                info.ui.title = self.title        



    preferences_pages = List(PreferencesPage)
    def _preferences_pages_default(self):
        ''' Subclasses of ParamsHandler should override this method if more than one PreferencesPage is used. '''
        return [self.preferences_page]
    
    preferences_page = Instance(PreferencesPage)
    def _preferences_page_default(self):
#        raise NotImplementedError('e.g. return McssParamsPreferencesPage')
        return None
    
    _preferences_pages = Property(depends_on='preferences_pages', desc='filters instances of None from preferences_pages for enabled_when in Preferences Action')
    def _get__preferences_pages(self):
        return [page for page in self.preferences_pages if page is not None]
    
    def edit_preferences(self, info):
        preferences_manager = PreferencesManager(pages=self._preferences_pages) # must pass in pages manually 
        ui = preferences_manager.edit_traits(kind='modal') # should edit preferences modally
        if ui.result: # only save preferences if OK pressed
            for page in self.preferences_pages: # save preferences for each page as they could have different preferences nodes (files)
                page.preferences.save() # must save preferences manually
        return ui.result


    def close_window(self, info):
        info.ui.control.close()

    def closed(self, info, is_ok): # must return True or else window is uncloseable!
        if is_ok:
            self.model.save_preferences()
        return True

    def load(self, info):
        ''' Load the traits of an experiment from a .params XML file. '''
        
        from enthought.traits.ui.message import auto_close_message, error, message
        if info.object._dirty:
            if message(str('Save current parameters before loading?'), title='Unsaved parameters', buttons=['OK', 'Cancel']):
                self.save(info)        

        params = info.object
        title = 'Load %s parameters' % params._parameters_name
        file_name = self.get_load_file_name_using_PyFace_FileDialog(title)
#        file_name = self.get_load_file_name_using_Traits_FileDialog(title)
        if file_name is not None:
            params.load(file_name)
            from infobiotics.commons.strings import shorten_path
            self.status = "Loaded '%s'." % shorten_path(file_name, 70)
        
    def get_load_file_name_using_PyFace_FileDialog(self, title):
        fd = FileDialog(
            wildcard=self.wildcard,
            title=title,
            default_filename=self.model._params_file,
            default_directory=self.model.directory_ # note extra '_' in directory_, this means that it uses the shadow value of the trait 'directory' which is the full path
        )
        if fd.open() == OK:
            return fd.path
        return None
               
#    def get_load_file_name_using_Traits_FileDialog(self, title):
#        fd = OpenFileDialog(
#            file_name=self.model._params_file,
#            filter=self.filter,
#            title=title,
#            id='ParamsHandler.get_load_file_name_using_Traits_FileDialog',
#        )
#        if fd.edit_traits(view='open_file_view', parent=self.info.ui.control).result: # if kind='modal' here fd.file_name never changes!
#            return fd.file_name
#        return None

    copy = Bool(False, desc='whether to copy required files with relatives paths to new save directory (set by eponymous FileDialog extension)')
#    copy = Bool(True) #TODO remove after adding file_dialog2.py

    def save(self, info):
        ''' Saves the traits of experiment to a .params XML file. '''
        params = info.object
        title = 'Save %s parameters' % params._parameters_name
        file_name = self.get_save_file_name_using_PyFace_FileDialog(title)
#        file_name = self.get_save_file_name_using_Traits_FileDialog(title)
        if file_name is not None:
            if self.copy: #TODO prompt to overwrite existing files in new directory
                pass
            params.save(file_name, force=True, copy=self.copy) # user will have been prompted to overwrite by the GUI
            from infobiotics.commons.strings import shorten_path
            self.status = "Saved '%s'." % shorten_path(file_name, 71)
                                   
    def get_save_file_name_using_PyFace_FileDialog(self, title):
        fd = FileDialog(
            action='save as',
            default_filename=self.model._params_file,
            default_directory=self.model.directory_,
            wildcard=self.wildcard,
            title=title,
        )
        if fd.open() == OK:
            return fd.path
        return None
    
#    def get_save_file_name_using_Traits_FileDialog(self, title):
#        fd = OpenFileDialog(
#            is_save_file=True,
#            extensions=[
#                CopyInputFilesWithRelativePathsExtension(),
#                FileInfo(),
#                TextInfo(),
#            ],
#            file_name=self.model._params_file,
#            filter=self.filter,
#            title=title,
#            id='ParamsHandler.get_save_file_name_using_Traits_FileDialog',
#        )
#        if fd.edit_traits(view='open_file_view', parent=self.info.ui.control).result: # if kind='modal' here fd.file_name never changes!
#            # get whether to copy input files with relative paths or not
#            for extension in fd.extensions:
#                if isinstance(extension, CopyInputFilesWithRelativePathsExtension):
#                    self.copy = extension.copy if extension.copy_enabled else False
#            return fd.file_name
#        return None
            
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
        

    has_valid_parameters = Property(Bool, depends_on='info.ui.errors, model.executable')
    @cached_property
    def _get_has_valid_parameters(self):
        # adapted from TraitsBackendQt/enthought/traits/ui/qt4/ui_base.py:BaseDialog._on_error() and ui_modal.py:_ModalDialog.init():ui.on_trait_change(self._on_error, 'errors', dispatch='ui') 
        if not self.info:
            return
        if self.info.initialized:
            if self.info.ui is None:
                return False
            if self.info.ui.errors > 0:
                return False
            if not os.path.isfile(self.model.executable):
                return False
            if self.model.running:
                return False
        return True
    
    def _has_valid_parameters_changed(self, value):
        if value:
            self.status = ''
            return
        if not self.info:
            return
        if self.info.initialized:
            if self.info.ui is None:
                return
            self.status = '\n'.join(['%s must be %s' % (editor.name, editor.object.base_trait(editor.name).full_info(editor.object, editor.name, editor.value)) for editor in self.info.ui._editors if hasattr(editor, '_error') and getattr(editor, '_error', None) is not None])
            #TODO shorten these!
        
if __name__ == '__main__':
    execfile('params.py')
