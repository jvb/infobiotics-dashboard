from PyQt4.QtCore import SIGNAL, QObject
from PyQt4.QtGui import QAction, QIcon, QActionGroup

def separator(parent):
    separator = QAction(parent) 
    separator.setSeparator(True)
    return separator

def add_actions(target, actions):
    '''Helper function that adds actions to a QObject target, often a QMenu, or
    possibly a widget for use with setContextMenuPolicy(Qt.ActionsContextMenu).
    
    If an item in actions is None then a separator is added.
    
    '''
    for action in actions:
        if action is None:
            target.addAction(separator(target))
        elif isinstance(action, QActionGroup):
            target.addActions(action.actions())
        else:
            target.addAction(action)

def create_action(parent, text, slot=None, shortcut=None, icon=None, tip=None,
    checkable=False, signal="triggered()"):
    '''Helper function that creates QActions with a given QObject parent.'''
    action = QAction(text, parent)
    if icon is not None:
        action.setIcon(QIcon(":/%s.png" % icon))
    if shortcut is not None:
        action.setShortcut(shortcut)
    if tip is not None:
        action.setToolTip(tip)
        action.setStatusTip(tip)
    if slot is not None:
        QObject.connect(action, SIGNAL(signal), slot)
    if checkable:
        action.setCheckable(True)
    return action

def create_action_group(parent, actions=[], enabled=True, exclusive=True, visible=True, hovered_slot=None, triggered_slot=None):
    action_group = QActionGroup(parent)
    for action in actions:
        action_group.addAction(action)
    action_group.setEnabled(enabled)
    action_group.setExclusive(exclusive)
    action_group.setVisible(visible)
    if hovered_slot:
        action_group.connect(action, SIGNAL('hovered(QAction)'), hovered_slot)
    if triggered_slot:
        action_group.connect(action, SIGNAL('triggered(QAction)'), triggered_slot)
    return action_group
    