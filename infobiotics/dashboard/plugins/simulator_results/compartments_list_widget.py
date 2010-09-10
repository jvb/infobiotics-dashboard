from infobiotics.commons.pyqt4.list_widget import ListWidget
from infobiotics.commons.pyqt4.actions import add_actions, create_action

class CompartmentsListWidget(ListWidget):

    def __init__(self, parent=None, use_built_in_context_menu=True):
        super(CompartmentsListWidget, self).__init__(parent, use_built_in_context_menu)
        
        if use_built_in_context_menu:

            def name_then_x_then_y(match, item):
                return item.text().replace(',', '.')
#            ('.*\(\d+,\d+\)$', name_then_x_then_y)

            def name_then_y_then_x(match, item):
                x_and_y = match.group().split('(')[1].split(')')[0]
                x, y = x_and_y.split(',')
                return '%s%s.%s' % (match.group().split(':')[0], y, x)
#            ('.*\(\d+,\d+\)$', name_then_y_then_x)

            def x_then_y(match, item):
                return float(match.group().split('(')[1].split(')')[0].replace(',', '.'))
#            ('.*\(\d+,\d+\)$', x_then_y)
            
            def y_then_x(match, item):
                x_and_y = match.group().split('(')[1].split(')')[0]
                x, y = x_and_y.split(',')
                return float('%s.%s' % (y, x))
#            ('.*\(\d+,\d+\)$', y_then_x)

            add_actions(self,
                [
                    None,
                    create_action(self, 'Sort by name then x then y ascending', lambda: self.sortItems(regex_functions=[('.*\(\d+,\d+\)$', name_then_x_then_y)])),
                    create_action(self, 'Sort by name then x then y descending', lambda: self.sortItems(order=Qt.DescendingOrder, regex_functions=[('.*\(\d+,\d+\)$', name_then_x_then_y)])),
                    None,
                    create_action(self, 'Sort by name then y then x ascending', lambda: self.sortItems(regex_functions=[('.*\(\d+,\d+\)$', name_then_y_then_x)])),
                    create_action(self, 'Sort by name then y then x descending', lambda: self.sortItems(order=Qt.DescendingOrder, regex_functions=[('.*\(\d+,\d+\)$', name_then_y_then_x)])),
                    None,
                    create_action(self, 'Sort by x then y ascending', lambda: self.sortItems(regex_functions=[('.*\(\d+,\d+\)$', x_then_y)])),
                    create_action(self, 'Sort by x then y descending', lambda: self.sortItems(order=Qt.DescendingOrder, regex_functions=[('.*\(\d+,\d+\)$', x_then_y)])),
                    None,
                    create_action(self, 'Sort by y then x ascending', lambda: self.sortItems(regex_functions=[('.*\(\d+,\d+\)$', y_then_x)])),
                    create_action(self, 'Sort by y then x descending', lambda: self.sortItems(order=Qt.DescendingOrder, regex_functions=[('.*\(\d+,\d+\)$', y_then_x)])),
                ]
            )
