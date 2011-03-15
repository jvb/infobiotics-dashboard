from enthought.envisage.ui.action.api import ActionSet, Action, Group, Menu

PKG = 'infobiotics.plugins.dashboard.actions'
#PKG = '.'.join(__name__.split('.')[:-1]) + '.actions'

class CoreActionSet(ActionSet):
#from enthought.envisage.ui.workbench.workbench_action_set import WorkbenchActionSet
#class CoreActionSet(WorkbenchActionSet):
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
            class_name=PKG + '.python_module_action:PythonModuleAction',
            group='NewFileGroup',
            path='MenuBar/File/New'),
        Action(
            id='UntitledTextFileAction',
            class_name=PKG + '.untitled_text_file_action:UntitledTextFileAction',
            group='NewFileGroup',
            path='MenuBar/File/New'),
        
#        Action(
#            id='OpenAction', #TODO
#            class_name=PKG + 'OpenAction',
#            group='NewGroup',
#            path='MenuBar/File'),
        Action(
            id='OpenTextFileAction', #TODO remove to UnifiedOpenDialog
            class_name=PKG + '.open_text_file_action:OpenTextFileAction',
            group='OpenGroup',
            path='MenuBar/File'),
        
        Action(
            id='SaveFile',
            class_name=PKG + '.save_action:SaveAction',
            group='SaveGroup',
            path='MenuBar/File'),
        Action(
            id='SaveAsFile',
            class_name=PKG + '.save_as_action:SaveAsAction',
            group='SaveGroup',
            path='MenuBar/File'),
    ]
