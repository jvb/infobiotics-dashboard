from PyQt4.QtGui import QListWidget, QAbstractItemView
from PyQt4.QtCore import SIGNAL, pyqtSignal, Qt, SLOT
from infobiotics.commons.pyqt4.actions import add_actions, create_action
import operator
import re

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
        
        # filtering
        self._locked = False # necessary for safe filtering
        self.filter_text = ''
        self.is_filtered = False
        
        # sorting
        self.setSortingEnabled(False) # don't use QListWidget sort method
        self.is_sorted = False

        if use_built_in_context_menu:

            add_actions(
                self,
                [
                    create_action(self, 'Select &All', self.selectAll),
                    create_action(self, '&Invert Selection', self.invert_selection),
                    None,
                    create_action(self, '&Sort Ascending', lambda: self.sortItems(order=Qt.AscendingOrder)),
                    create_action(self, 'Sort &Descending', lambda: self.sortItems(order=Qt.DescendingOrder)),
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

    def select(self, row):
        self.item(row).setSelected(True)
        print 'got here'

    def selectAll(self, checked=True): #TODO only_visible (True is same as QListWidget.selectAll!)
        self.disconnect(self, SIGNAL('itemSelectionChanged()'), self.remember_selection)
        if checked:
            super(ListWidget, self).selectAll()
        else:
            self.clearSelection()
            for item in self.selected:
                item.setSelected(True) 
        self.connect(self, SIGNAL('itemSelectionChanged()'), self.remember_selection)
#        #TODO unittests
#        self.insertItem(2, '20')
#        self.addItem('21')
#        self.addItems(['22', '23'])
#        self.insertItems(2, ['22', '23'])
    
    def invert_selection(self, only_visible=True): # False is same as QListWidget.selectAll()!
#        for item in self.all_items():
#            if item.isSelected():
#                item.setSelected(False)
#            else:
#                item.setSelected(True)
        if only_visible:
            [item.setSelected(not item.isSelected()) for item in self.visible_items()]
        else:   
            [item.setSelected(not item.isSelected()) for item in self.all_items_generator()]
    
    def addItem(self, item, in_original_order=True):
        if in_original_order and self.is_sorted:
            self.sortItems(False, quiet=True)
            super(ListWidget, self).addItem(item) # don't replace with self.insertItem(row=self.count())
            self.sortItems(True, quiet=True)
        else:
            super(ListWidget, self).addItem(item)
    
    def addItems(self, items, in_original_order=True):
        for item in items:
            self.addItem(item, in_original_order)
    
    def insertItem(self, row, item, in_original_order=True):
        if in_original_order and self.is_sorted: #TODO ambiguous?
            self.sortItems(False, quiet=True)
            super(ListWidget, self).insertItem(row, item)
            self.sortItems(True, quiet=True)
        else:
            super(ListWidget, self).insertItem(row, item)

    def insertItems(self, row, items, in_original_order=True):
        for item in items:
            self.insertItem(row, item, in_original_order)

    def all_items_generator(self, in_original_order=True):
        if in_original_order:
            all_items_in_current_order = self.all_items_generator(in_original_order=False)
            if not hasattr(self, '_items') or set(self._items) != set(all_items_in_current_order):
                self._items = all_items_in_current_order
            return (item for item in self._items)
        else:
            return [self.item(i) for i in range(self.count())]
    
    def all_items(self, in_original_order=True):
        return list(self.all_items_generator(in_original_order))

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
        ''' Remove items but do not destroy them, as opposed to clear(). '''
        for i in reversed(range(self.count())): # must be reversed so that we don't change the order of the items during loop
            self.takeItem(i)
#        for _ in range(self.count()): # or just take zeroth item each item - maybe slower?
#            self.takeItem(0)

    def sortItems(self, checked=True, order=Qt.AscendingOrder, quiet=False, regex_functions=[]):


        def fix_text_beginning_with_numbers(match, item):
            return float(match.group())
        regex_functions.append(('^\d+(\.?\d*)', fix_text_beginning_with_numbers))
        
        if order not in (Qt.AscendingOrder, Qt.DescendingOrder):
            raise ValueError('order not in (Qt.AscendingOrder, Qt.DescendingOrder)')
        
        self.disconnect(self, SIGNAL('itemSelectionChanged()'), self.remember_selection)

        items = self.all_items() # must be done here so that self._items (with original ordering) is created via all_items_generator
        
        if checked:
#            self.setSortingEnabled(True)
#            super(ListWidget, self).sortItems() # doesn't sort strings beginning with numbers properly
            
            self.empty()
            
            enumerated_items = [[i, item] for i, item in enumerate(items)]
        
            for i, item in enumerated_items:
                matched = False
                for regex, function in regex_functions:
                    match = re.match(regex, item.text())
                    if match:
#                        print regex
                        enumerated_items[i].append(function(match, item))
                        matched = True
                        break
                if not matched:
                    enumerated_items[i].append(item.text())
            
            def add_items_sorted(reverse):
                for _, item, _ in sorted(enumerated_items, key=operator.itemgetter(2), reverse=reverse): 
                    super(ListWidget, self).addItem(item)
            
            if order == Qt.AscendingOrder:
                add_items_sorted(reverse=False)
            else: # order == Qt.DescendingOrder:
                add_items_sorted(reverse=True)
            
            is_sorted = True
            
        else:
#            self.setSortingEnabled(False)

            self.empty()
            
            # add them back in the original order
            for item in items: 
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
            self.is_sorted = is_sorted
            if not quiet:
                self.is_sorted_changed.emit(self.is_sorted)
            
        self.connect(self, SIGNAL('itemSelectionChanged()'), self.remember_selection)

    def selected_count(self):
        return len(self.selectedItems())
    
    def visible_items_generator(self): #TODO in_original_order
        return (item for item in self.all_items() if not item.isHidden())
    
    def visible_items(self):
        return list(self.visible_items_generator())
    
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
        self.connect(sort_check_box, SIGNAL('toggled(bool)'), self.sortItems)
#        self.connect(self, SIGNAL('is_sorted_changed()'), sort_check_box, SLOT('toggled(bool)'))
    
    def filter_line_edit_factory(self, parent=None):
        filter_line_edit = QLineEdit(parent)
        self.connect_filter_line_edit(filter_line_edit)
        return filter_line_edit
    
    def connect_filter_line_edit(self, filter_line_edit):
        ''' Enables functionality to be add to line edit outside of factory. '''
        self.connect(filter_line_edit, SIGNAL('textChanged(QString)'), self.filter)

        #TODO move to filter_line_edit_factory?
        from infobiotics.commons.qt4 import version
        split = version.split('.')
        if int(split[0]) > 4 or (int(split[0]) == 4 and int(split[1]) >= 7):
            filter_line_edit.setPlaceholderText('Filter')

class CheckBoxListWidget(ListWidget):
    
    def __init__(self, parent=None, use_built_in_context_menu=True):
        super(CheckBoxListWidget, self).__init__(parent, use_built_in_context_menu)
        
        self.connect(self, SIGNAL('itemDoubleClicked(QListWidgetItem*)'), self.toggle_item_check_state)
        
    def toggle_item_check_state(self, item):
        if item.checkState() == Qt.Unchecked:
            item.setCheckState(Qt.Checked)
        else:
            item.setCheckState(Qt.Unchecked)
    
    def check_selected(self):
        for item in self.selectedItems():
            item.setCheckState(Qt.Checked)

    def uncheck_selected(self):
        for item in self.selectedItems():
            item.setCheckState(Qt.Unchecked)
    
    def checked_items(self):
        return [item for item in self.all_items() if item.checkState() == Qt.Checked]

    
    

if __name__ == '__main__':
    from PyQt4.QtGui import QApplication, QWidget, QVBoxLayout, QLineEdit, QCheckBox, QPushButton
    app = QApplication([])
    
    list_widget = CheckBoxListWidget()
#    list_widget.addItems([str(i) for i in reversed(range(0, 15, 2))])
#    list_widget.addItems(['1.1', '1.0a', '1.0b', '2', '12'])
#    list_widget.addItems(['a', '1', '2', 'a(1,2)', 'a(1.2)', 'a(2,1)', '2,1'])
    list_widget.addItems(['a(1,2)', '(0,2)e', 'b(1,1)', 'a(2,1)', '(99,100)', '(100,99)'])
    
    filter_line_edit = list_widget.filter_line_edit_factory()
    
    all_selected_check_box = list_widget.all_selected_check_box_factory()    
    
    invert_selection_push_button = list_widget.invert_selection_push_button_factory('&Invert Selection')
    
    sort_check_box = list_widget.sort_check_box_factory()
    
    layout = QVBoxLayout()
    layout.addWidget(list_widget)
    layout.addWidget(filter_line_edit)
    layout.addWidget(all_selected_check_box)
    layout.addWidget(invert_selection_push_button)
    layout.addWidget(sort_check_box)
    widget = QWidget()
    widget.setLayout(layout)
    widget.setGeometry(600, 300, 200, 480)
    widget.show()
    exit(app.exec_())
