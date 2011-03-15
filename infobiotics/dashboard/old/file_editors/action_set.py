from enthought.envisage.ui.action.api import ActionSet, Action, Group, Menu

PKG = 'infobiotics.dashboard.plugins.file_editors.actions:'#'.'.join(__name__.split('.')[:-1]) + '.actions:'

class FileEditorsActionSet(ActionSet):
#from enthought.envisage.ui.workbench.workbench_action_set import WorkbenchActionSet
#class FileEditorsActionSet(WorkbenchActionSet):
#    enabled_for_perspectives = ['id',]
#    visible_for_perspectives = ['id',]
#
#    enabled_for_views = ['id',]
#    visible_for_views = ['id',]

    groups = [
        Group(
            id='NewGroup',
            path='MenuBar/File',
            before='OpenGroup'),
        Group(
            id='NewObjectGroup',
            path='MenuBar/File/New',
            before='NewFileGroup'),
        Group(
            id='NewFileGroup',
            path='MenuBar/File/New',
            after='NewObjectGroup'),
    ]

    menus = [
        Menu(
            name='&New',
            group='NewGroup',
            groups=['NewObjectGroup','NewFileGroup'],
            path='MenuBar/File'),
    ]

    #TODO toolbars (with icons!)

    actions = [
        Action(
            id='PythonModuleAction',
            class_name=PKG + 'PythonModuleAction',
            group='NewFileGroup',
            path='MenuBar/File/New'),
        Action(
            id='UntitledTextFileAction',
            class_name=PKG + 'UntitledTextFileAction',
            group='NewFileGroup',
            path='MenuBar/File/New'),
        
#        Action(
#            id='OpenAction', #TODO
##            name='&Open...',
#            class_name=PKG + 'OpenAction',
#            group='NewGroup',
#            path='MenuBar/File'),
        Action(
            id='OpenTextFileAction', #TODO remove to UnifiedOpenDialog
#            name='Open &Text File...',
            class_name=PKG + 'OpenTextFileAction',
            group='OpenGroup',
            path='MenuBar/File'),
        
        Action(
            id='SaveFile',
#            name='&Save',
            class_name=PKG + 'SaveAction',
            group='SaveGroup',
            path='MenuBar/File'),
        Action(
            id='SaveAsFile',
#            name='Save &As...',
            class_name=PKG + 'SaveAsAction',
            group='SaveGroup',
            path='MenuBar/File'),
    ]
