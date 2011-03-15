# This file is part of the Infobiotics Workbench. See LICENSE for copyright.
# $Id: __init__.py 286 2009-08-25 17:51:05Z jvb $
# $HeadURL: https://psiren.cs.nott.ac.uk/repos/infobiotics/gui-current/trunk/src/metamodel/__init__.py $
# $Author: jvb $
# $Revision: 286 $
# $Date: 2009-08-25 18:51:05 +0100 (Tue, 25 Aug 2009) $


from actions import addActions, createAction
from PyQt4.QtCore import Qt, SIGNAL
from PyQt4.QtGui import QListWidget, QAbstractItemView, QAction, QMenu, QToolBar, QListWidgetItem


class EnhancedListWidget(QListWidget):
    '''
    An enhanced QListWidget with mass-checking/unchecking of selection,
    inverse selection and an allItems function. 
    '''
    #TODO add undo/redo functionality

    def __init__(self, parent=None):
        QListWidget.__init__(self, parent)
        
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)

        # create context menu actions:
        addActions(self, [
            createAction(self, 'Check selected', self.checkSelected),
            createAction(self, 'Uncheck selected', self.uncheckSelected),
            None, # shorthand for a seperator (see addActions)
            createAction(self, 'Invert selection', self.invertSelection),
            createAction(self, 'Select all', self.selectAll)])
        self.setContextMenuPolicy(Qt.ActionsContextMenu)
#        # alternatively:
#        self.setContextMenuPolicy(Qt.CustomContextMenu)
#        self.connect(self, SIGNAL('customContextMenuRequested(const QPoint &)'),
#                     self.showContextMenuForWidget)
#    def showContextMenuForWidget(self, pos):
#        contextMenu = QMenu("Context menu", self)
#        addActions(contextMenu, [
#            createAction(self, 'Check selected', self.checkSelected),
#            createAction(self, 'Uncheck selected', self.uncheckSelected),
#            None, # shorthand for a seperator (see addActions)
#            createAction(self, 'Invert selection', self.invertSelection),
#            createAction(self, 'Select all', self.selectAll)])
#        contextMenu.exec_(self.mapToGlobal(pos))
    
        self.connect(self, SIGNAL('itemDoubleClicked(QListWidgetItem*)'), self.toggleItemCheckState)
    
        self.setToolTip('Right-clicked for options such as\n"Select all" and "Check selected"')
    
    
    def toggleItemCheckState(self, item):
        if item.checkState() == Qt.Checked:
            item.setCheckState(Qt.Unchecked)
        else:
            item.setCheckState(Qt.Checked)
    
    def checkSelected(self):
        for item in self.selectedItems():
            item.setCheckState(Qt.Checked)


    def uncheckSelected(self):
        for item in self.selectedItems():
            item.setCheckState(Qt.Unchecked)


    def invertSelection(self):
        for item in self.items():
            if item.isSelected():
                item.setSelected(False)
            else:
                item.setSelected(True)


    def items(self):
        return [self.item(i) for i in range(self.count())]

    
    def checkedItems(self):
        return [item for item in self.items() if item.checkState() == Qt.Checked]
    

if __name__ == '__main__':
    from PyQt4.QtGui import QApplication
    app = QApplication([])
    
    w = EnhancedListWidget()
    for i in range(0, 6):
        item = QListWidgetItem('item %s' % i)
#        item.setCheckState(Qt.Unchecked)
        w.addItem(item)
        
    w.show()
    
    app.exec_()
