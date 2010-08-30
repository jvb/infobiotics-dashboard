# This file is part of the Infobiotics Workbench. See LICENSE for copyright.
# $Id: __init__.py 286 2009-08-25 17:51:05Z jvb $
# $HeadURL: https://psiren.cs.nott.ac.uk/repos/infobiotics/gui-current/trunk/src/metamodel/__init__.py $
# $Author: jvb $
# $Revision: 286 $
# $Date: 2009-08-25 18:51:05 +0100 (Tue, 25 Aug 2009) $


from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QAction, QIcon


def addActions(target, actions):
    '''
    Helper function that adds actions to a QObject target, often a QMenu, or
    possibly a widget for use with setContextMenuPolicy(Qt.ActionsContextMenu).
    '''
    for action in actions:
        if action is None:
            action = QAction(target)
            action.setSeparator(True)
            target.addAction(action)
        else:
            target.addAction(action)


def createAction(parent, text, slot=None, shortcut=None, 
                 icon=None, tip=None, checkable=False, 
                 signal="triggered()"):
    '''
    Helper function that creates QActions with a given QObject parent.
    '''
    action = QAction(text, parent)
    if icon is not None:
        action.setIcon(QIcon(":/%s.png" % icon))
    if shortcut is not None:
        action.setShortcut(shortcut)
    if tip is not None:
        action.setToolTip(tip)
        action.setStatusTip(tip)
    if slot is not None:
        parent.connect(action, SIGNAL(signal), slot)
    if checkable:
        action.setCheckable(True)
    return action
