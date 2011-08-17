from PyQt4.QtCore import Qt
from infobiotics.commons.pyqt4.list_widget import ListWidget
from infobiotics.commons.pyqt4.actions import add_actions, create_action

pattern = '.*\(\d+,\d+\)$'
x_and_y = lambda match: str(match.group()).split('(')[1].split(')')[0].split(',')
name = lambda match: str(match.group()).rsplit(' ')[0] 


class CompartmentsListWidget(ListWidget):
    '''ListWidget with some extra popup menu actions for filtering compartments.'''

    def __init__(self, parent=None, use_built_in_context_menu=True):
        super(CompartmentsListWidget, self).__init__(parent, use_built_in_context_menu)
        
        if use_built_in_context_menu:

            def name_then_x_then_y(match, item):
                x, y = x_and_y(match)
                return (name(match), float(x), float(y))

            def name_then_y_then_x(match, item):
                x, y = x_and_y(match)
                return (name(match), float(y), float(x))

            def x_then_y(match, item):
                x, y = x_and_y(match)
                return (float(x), float(y))
            
            def y_then_x(match, item):
                x, y = x_and_y(match)
                return (float(y), float(x))

            add_actions(self,
                [
                    None,
                    create_action(self, 'Sort by name then x then y ascending', lambda: self.sortItems(regex_functions=[(pattern, name_then_x_then_y)])),
                    create_action(self, 'Sort by name then x then y descending', lambda: self.sortItems(order=Qt.DescendingOrder, regex_functions=[(pattern, name_then_x_then_y)])),
                    None,
                    create_action(self, 'Sort by name then y then x ascending', lambda: self.sortItems(regex_functions=[(pattern, name_then_y_then_x)])),
                    create_action(self, 'Sort by name then y then x descending', lambda: self.sortItems(order=Qt.DescendingOrder, regex_functions=[(pattern, name_then_y_then_x)])),
                    None,
                    create_action(self, 'Sort by x then y ascending', lambda: self.sortItems(regex_functions=[(pattern, x_then_y)])),
                    create_action(self, 'Sort by x then y descending', lambda: self.sortItems(order=Qt.DescendingOrder, regex_functions=[(pattern, x_then_y)])),
                    None,
                    create_action(self, 'Sort by y then x ascending', lambda: self.sortItems(regex_functions=[(pattern, y_then_x)])),
                    create_action(self, 'Sort by y then x descending', lambda: self.sortItems(order=Qt.DescendingOrder, regex_functions=[(pattern, y_then_x)])),
                ]
            )
