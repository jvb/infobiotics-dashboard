from envisage.ui.action.api import Action, ActionSet, Group

class TextEditorActionSet(ActionSet):

    groups = [
        Group(
            id = "TextFileGroup",
            path = "MenuBar/File",
            before = "ExitGroup")
    ]

    actions = [
        Action(
            id = "NewFileAction",
            name = "&New Text File",
            class_name='infobiotics.dashboard.plugins.text_editor.actions.NewFileAction',
            group='TextFileGroup',
            path="MenuBar/File"),
        Action(
            id = 'OpenFile',
            name = "&Open Text File...",
            class_name='infobiotics.dashboard.plugins.text_editor.actions.OpenFileAction',
            group='TextFileGroup',
            path="MenuBar/File"),
        Action(
            id = 'SaveFile',
            name = "&Save",
            class_name='infobiotics.dashboard.plugins.text_editor.actions.SaveFileAction',
            group='TextFileGroup',
            path="MenuBar/File"),
        Action(
            id = 'SaveAsFile',
            name = "Save &As...",
            class_name='infobiotics.dashboard.plugins.text_editor.actions.SaveAsFileAction',
            group='TextFileGroup',
            path="MenuBar/File"),
    ]
