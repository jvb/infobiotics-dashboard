from PyQt4.QtGui import QListWidget, QAbstractItemView, QListWidgetItem
from PyQt4.QtCore import SIGNAL, pyqtSignal, Qt, SLOT
from infobiotics.commons.pyqt4.actions import add_actions, create_action, QActionGroup,\
    create_action_group, separator
from infobiotics.commons.qt4 import disable_widgets, enable_widgets

import operator
import re

def createQListWidgetItem(item):
    '''Wraps item strings in QListWidgetItems so they can be returned.'''
    return QListWidgetItem(item) if not isinstance(item, QListWidgetItem) else item 

        
class ListWidget(QListWidget):
    ''' QListWidget that preserves original ordering, with filtering, sorting, 
    and selection methods. ''' 

    # signals
    is_filtered_changed = pyqtSignal(bool)
    filter_changed = pyqtSignal(str)
    is_sorted_changed = pyqtSignal(bool)
#    selected_count_changed = pyqtSignal(str) #TODO emit '%d/%d (%d)' % (self.selected_and_visible_count(), self.visible_count(), self.count()) if filtered else '%d/%d' % (self.selected_count(), self.count()) where 10 is the number selected and 100 is self.count()

    def __init__(self, parent=None, use_built_in_context_menu=True):
        super(ListWidget, self).__init__(parent)
        
        # selection
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.selected = []
        self.connect(self, SIGNAL('itemSelectionChanged()'), self.remember_selection)
        self.connect(self, SIGNAL('itemSelectionChanged()'), lambda: self.selectAllAction.setDisabled(self.selected_visible_count() == self.visible_count()))
        
        # filtering
        self._locked = False # necessary for safe filtering
        self.filter_text = ''
        self.is_filtered = False
        
        # sorting
        self.setSortingEnabled(False) # don't use QListWidget sort method
        self.is_sorted = False

        self.selectAllAction = create_action(self, 'Select &All', self.selectAll)
        self.invertSelectionAction = create_action(self, '&Invert Selection', self.invert_selection) 

        self.sortAscendingAction = create_action(self, '&Sort Ascending', lambda: self.sortItems(order=Qt.AscendingOrder))
        self.sortDescendingAction = create_action(self, 'Sort &Descending', lambda: self.sortItems(order=Qt.DescendingOrder))
        self.restoreOriginalOrderAction = create_action(self, '&Restore Original Order', lambda: self.sortItems(False))
#        sortActionGroup = create_action_group(self)
#        self.sortAscendingAction = create_action(sortActionGroup, '&Sort Ascending', lambda: self.sortItems(order=Qt.AscendingOrder))
#        self.sortDescendingAction = create_action(sortActionGroup, 'Sort &Descending', lambda: self.sortItems(order=Qt.DescendingOrder))
#        self.restoreOriginalOrderAction = create_action(sortActionGroup, '&Restore Original Order', lambda: self.sortItems(False))
        
        self.restoreOriginalOrderAction.setDisabled(True)

        if use_built_in_context_menu:
            add_actions(
                self,
                [
                    self.selectAllAction,
                    self.invertSelectionAction,
                    None,
                    self.sortAscendingAction,
                    self.sortDescendingAction,
                    self.restoreOriginalOrderAction,
#                    sortActionGroup,
                ]
            )
            self.setContextMenuPolicy(Qt.ActionsContextMenu)
#            # alternatively:
#            self.setContextMenuPolicy(Qt.CustomContextMenu)
#            self.connect(self, SIGNAL('customContextMenuRequested(const QPoint &)'),
#                         self.showContextMenuForWidget)
#        def showContextMenuForWidget(self, pos):
#            contextMenu = QMenu("Context menu", self)
#            addActions(contextMenu, [
#                createAction(self, 'Check selected', self.checkSelected),
#                createAction(self, 'Uncheck selected', self.uncheckSelected),
#                None, # shorthand for a seperator (see addActions)
#                createAction(self, 'Invert selection', self.invertSelection),
#                createAction(self, 'Select all', self.selectAll)])
#            contextMenu.exec_(self.mapToGlobal(pos))

    def remember_selection(self):
        self.selected = self.selectedItems()

    def select(self, row): #TODO override __getitem__ for indexing and slicing
        len_all_items = len(self.all_items()) 
        if row > len_all_items - 1:
            import sys
            sys.stderr.write('ListWidget.select(row=%s): row > %s, nothing selected.\n' % (row, len_all_items))
            return
        if row < 0:
            row = len_all_items + row
        self.item(row).setSelected(True)

    def selectAll(self, checked=True): #TODO only_visible (True is same as QListWidget.selectAll!)
        self.disconnect(self, SIGNAL('itemSelectionChanged()'), self.remember_selection)
        if checked:
#            self.selectAllAction.setEnabled(False)
            super(ListWidget, self).selectAll()
        else:
#            self.selectAllAction.setEnabled(True)
            self.clearSelection()
            for item in self.selected:
                item.setSelected(True) 
        self.connect(self, SIGNAL('itemSelectionChanged()'), self.remember_selection)
    
    def invert_selection(self, only_visible=True):
        if only_visible:
            [item.setSelected(not item.isSelected()) for item in self.visible_items()]
        else:   
            [item.setSelected(not item.isSelected()) for item in self.all_items()]
    
    def addItem(self, item, in_original_order=True):
        item = createQListWidgetItem(item)
        if in_original_order and self.is_sorted:
            self.sortItems(False, quiet=True)
        super(ListWidget, self).addItem(item) # don't replace with self.insertItem(row=self.count()) # why not?
        if self.is_sorted:
            self.sortItems(quiet=True)
        return item
    
    def addItems(self, items, in_original_order=True):
        return [self.addItem(item, in_original_order) for item in items]

    def insertItem(self, row, item, in_original_order=True):
        item = createQListWidgetItem(item)
        if in_original_order and self.is_sorted:
            self.sortItems(False, quiet=True)
        super(ListWidget, self).insertItem(row, item)
        if self.is_sorted:
            self.sortItems(quiet=True)
        return item

    def insertItems(self, row, items, in_original_order=True):
        return [self.insertItem(row, item, in_original_order) for item in items]

    def remove(self, item):
        '''Removes item from ListWidget and deletes it. If you want to keep it use pop(item).'''
        row = self.row(item)
        self.takeItem(row)
        self._items.remove(item)
        del item
        
    def pop(self, item_or_row):
        '''Removes item and returns it.'''
        if not isinstance(item_or_row, int):
            # item_or_row is (hopefully) an item
            item_or_row = self.row(item_or_row)
        # item_or_row is the row
        item = self.takeItem(item_or_row)
        self._items.remove(item)
        return item
    
    def all_items(self, in_original_order=True):
        items = [self.item(i) for i in range(self.count())]
        if not hasattr(self, '_items'):
            self._items = items
        diff = set(items).difference(self._items)
        if diff:
            self._items.extend([item for item in items if item in diff])
        if in_original_order:
            return self._items
        else:
            return items

    def filter(self, text, quiet=False):
        if self._locked == True:
            return
        
        self._locked = True
        
        filtered = set([item for item in self.findItems(text, Qt.MatchContains)])

        unfiltered = frozenset(self.all_items()).symmetric_difference(filtered)
        
        for item in unfiltered:
            item.setHidden(True)
        for item in filtered:
            item.setHidden(False)
            
        if len(filtered) > 0:
            is_filtered = True
        else:
            is_filtered = False
            
        if is_filtered != self.is_filtered:
            self.is_filtered = is_filtered
            if not quiet:
                self.is_filtered_changed.emit(self.is_filtered)

        if text != self.filter_text:
            self.filter_text = text
            if not quiet:
                self.filter_changed.emit(self.filter_text)
            
        self._locked = False
        
    def empty(self):
        '''Remove items but do not destroy them, as opposed to clear().'''
        
        # precautionary update of self._items before removing everything 
        if not hasattr(self, '_items'):
            self._items = self.all_items()
        
        for i in reversed(range(self.count())): # must be reversed so that we don't change the order of the items during loop
            self.takeItem(i)
#        for _ in range(self.count()): # or just take zeroth item each item - maybe slower?
#            self.takeItem(0)

    def sortItems(self, checked=True, order=Qt.AscendingOrder, quiet=False, regex_functions=[]):
        '''
        
        regex_functions is a list of tuples of regex match string and function  

        Different to:
            self.setSortingEnabled(True); 
            super(ListWidget, self).sortItems()
        Which doesn't sort strings beginning with numbers properly
        
        '''
        if order not in (Qt.AscendingOrder, Qt.DescendingOrder):
            raise ValueError('order not in (Qt.AscendingOrder, Qt.DescendingOrder)')
        
        def fix_text_beginning_with_numbers(match, item):
            return float(match.group())
        regex_functions.insert(0, ('^\d+(\.?\d*)', fix_text_beginning_with_numbers))
        
        self.disconnect(self, SIGNAL('itemSelectionChanged()'), self.remember_selection)

        if checked:
            enumerated_items = [[i, item] for i, item in enumerate(self.all_items())]
            for i, item in enumerated_items:
                matched = False
                for regex, function in regex_functions:
                    match = re.match(regex, item.text())
                    if match:
                        enumerated_items[i].append(function(match, item))
                        matched = True
                        break
                if not matched:
                    enumerated_items[i].append(item.text())
            
            def add_items_sorted(reverse):
#                print ', '.join(str(match) for _, _, match in sorted(enumerated_items, key=operator.itemgetter(2), reverse=reverse))
                for _, item, _ in sorted(enumerated_items, key=operator.itemgetter(2), reverse=reverse):
                    super(ListWidget, self).addItem(item)
            
            self.empty()
            if order == Qt.AscendingOrder:
                add_items_sorted(reverse=False)
            else:# order == Qt.DescendingOrder:
                add_items_sorted(reverse=True)
            
            is_sorted = True
            
            if order == Qt.AscendingOrder:
                self.restoreOriginalOrderAction.setDisabled(False)
                self.sortAscendingAction.setDisabled(True)
                self.sortDescendingAction.setDisabled(False)
            else:
                self.restoreOriginalOrderAction.setDisabled(False)
                self.sortAscendingAction.setDisabled(False)
                self.sortDescendingAction.setDisabled(True)
        else:
            self.restoreOriginalOrderAction.setDisabled(True)
            self.sortAscendingAction.setDisabled(False)
            self.sortDescendingAction.setDisabled(False)
            
            # remove all items
            self.empty()
            
            # add them back in the original order
            for item in self.all_items(in_original_order=True): 
                super(ListWidget, self).addItem(item)
            
            is_sorted = False

        # reselect previously selected items
        self.clearSelection()
        for item in self.selected: 
            item.setSelected(True)
            
        # refilter
        if self.filter_text != '':
            self.filter(self.filter_text)

        if is_sorted != self.is_sorted:
            if not quiet:
                self.is_sorted = is_sorted
                self.is_sorted_changed.emit(self.is_sorted)
            
        self.connect(self, SIGNAL('itemSelectionChanged()'), self.remember_selection)


    def selected_count(self):
        return len(self.selectedItems())
    
    def visible_items(self, in_original_order=False):
        return list(item for item in self.all_items(in_original_order) if not item.isHidden())
    
    def visible_count(self):
        return len(self.visible_items())
    
    def selected_visible_items(self):
        return [item for item in self.visible_items() if item.isSelected()]
    
    def selected_visible_count(self):
        return len(self.selected_visible_items())
    
    def all_selected_check_box_factory(self, text='All', parent=None):
        all_selected_check_box = QCheckBox(text, parent)
        self.connect_all_selected_check_box(all_selected_check_box)
        return all_selected_check_box
    
    def connect_all_selected_check_box(self, all_selected_check_box):
        ''' Enables functionality to be add to check box outside of factory. '''
        self.connect(all_selected_check_box, SIGNAL('toggled(bool)'), self.selectAll)
        def all_selected_check_box_toggle_checked_quietly():
            self.disconnect(all_selected_check_box, SIGNAL('toggled(bool)'), self.selectAll)
            if len(self.selectedItems()) != self.count():
                all_selected_check_box.setChecked(False)  
            else:
                all_selected_check_box.setChecked(True)
            self.connect(all_selected_check_box, SIGNAL('toggled(bool)'), self.selectAll)
        self.connect(self, SIGNAL('itemSelectionChanged()'), all_selected_check_box_toggle_checked_quietly)
        
    def invert_selection_push_button_factory(self, text='Invert', parent=None):
        invert_selection_push_button = QPushButton(text)
        self.connect(invert_selection_push_button, SIGNAL('clicked()'), self.invert_selection)
        return invert_selection_push_button

    def sort_check_box_factory(self, text='Sort', parent=None):
        sort_check_box = QCheckBox(text, parent)
        self.connect_sort_check_box(sort_check_box)
        return sort_check_box
    
    def connect_sort_check_box(self, sort_check_box):
        self.connect(sort_check_box, SIGNAL('clicked(bool)'), self.sortItems)
        self.connect(self, SIGNAL('is_sorted_changed(bool)'), sort_check_box, SLOT('setChecked(bool)'))
    
    def filter_line_edit_factory(self, parent=None):
        filter_line_edit = QLineEdit(parent)
        self.connect_filter_line_edit(filter_line_edit)
        return filter_line_edit
    
    def connect_filter_line_edit(self, filter_line_edit):
        ''' Enables functionality to be add to line edit outside of factory. '''
        self.connect(filter_line_edit, SIGNAL('textChanged(QString)'), self.filter)
        from infobiotics.commons.qt4 import version
        split = version.split('.')
        if int(split[0]) > 4 or (int(split[0]) == 4 and int(split[1]) >= 7): # doesn't work with PyQt below 4.7
            filter_line_edit.setPlaceholderText('Filter')


def check(item, checked=True):
    item.setCheckState(Qt.Checked) if checked else item.setCheckState(Qt.Unchecked)
    return item  
    
def uncheck(item):
    return check(item, False)
    

class CheckBoxListWidget(ListWidget):
    '''ListWidget with checkable items.'''
    
    def __init__(self, parent=None, use_built_in_context_menu=True):
        super(CheckBoxListWidget, self).__init__(parent, use_built_in_context_menu)
        self.connect(self, SIGNAL('itemDoubleClicked(QListWidgetItem*)'), self.toggle_item_check_state)
        
    def addItem(self, item, in_original_order=True, checked=False):
        item = super(CheckBoxListWidget, self).addItem(item, in_original_order)
        check(item, checked)
        return item
    
    def insertItem(self, row, item, in_original_order=True, checked=False):
        item = super(CheckBoxListWidget, self).insertItem(row, item, in_original_order)
        check(item, checked)
        return item
    
    def toggle_item_check_state(self, item):
        return check(item, item.checkState() == Qt.Unchecked)
    
    def check_selected(self, checked=True):
        return [check(item, checked) for item in self.selectedItems()]

    def uncheck_selected(self):
        return self.check_selected(False)
    
    def checked_items(self, only_visible=True):
        if only_visible:
            return [item for item in self.visible_items() if item.checkState() == Qt.Checked]
        else:   
            return [item for item in self.all_items() if item.checkState() == Qt.Checked]
        


if __name__ == '__main__':
    from PyQt4.QtGui import QApplication, QWidget, QVBoxLayout, QLineEdit, QCheckBox, QPushButton
    app = QApplication([])
    
    lw = ListWidget()
#    lw = CheckBoxListWidget()

#    lw.addItems([str(i) for i in reversed(range(0, 15, 2))])
#    lw.addItems(['1.1', '1.0a', '1.0b', '2', '12'])
#    lw.addItems(['a', '1', '2', 'a(1,2)', 'a(1.2)', 'a(2,1)', '2,1'])
    items = ['a(1,2)', '(0,2)e', 'b(1,1)', 'a(2,1)', '(99,100)', '(100,99)']
#    lw.addItems(items)
    for item in items:
        QListWidgetItem(item, lw)
    
    l = QVBoxLayout()
    l.addWidget(lw)
    l.addWidget(lw.filter_line_edit_factory())
    l.addWidget(lw.all_selected_check_box_factory())
    l.addWidget(lw.invert_selection_push_button_factory('&Invert Selection'))
    l.addWidget(lw.sort_check_box_factory())
    
    import random
    button = QPushButton('add random')
    button.connect(button, SIGNAL('clicked(bool)'), lambda: lw.addItem(random.choice(['x','y','z']), True))
    l.addWidget(button)
    button2 = QPushButton('remove random')
    button2.connect(button2, SIGNAL('clicked(bool)'), lambda: lw.pop(random.randint(0, lw.count()-1)))
    l.addWidget(button2)
    
    self = QWidget()
    self.setLayout(l)
    self.setGeometry(600, 400, 200, 480)
    self.setWindowTitle(lw.__class__.__name__)
    self.show()

#    lw.select(-2)
#    lw.select(9)
    
    exit(app.exec_())
