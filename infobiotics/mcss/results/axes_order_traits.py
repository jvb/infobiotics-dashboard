import os; os.environ['ETS_TOOLKIT'] = 'qt4'
from enthought.traits.api import HasTraits, List, Str, Enum, Button
from enthought.traits.ui.api import View, VGroup, VSplit, Item, SetEditor, ListEditor, EnumEditor

class Axis(HasTraits):
    name = Str
    function = Enum(['mean', 'standard deviation', 'variance', 'median', 'sum', 'minimum', 'maximum'])

    def __str__(self):
        return self.name

    view = View(
        Item('function',
            show_label=False,
            style='custom',
        )
    )

class AxesOrder(HasTraits):
    axes = List(Axis)
    order = List(Axis)
    ok = Button
    
    def _axes_default(self):
        return [
            Axis(name='Runs'),
            Axis(name='Species'),
            Axis(name='Compartments'),
            Axis(name='Timepoints'),
        ]

    view = View(
        VGroup(
            VSplit(
                VGroup(
                    Item(label='Choose the axes (and reorder if necessary):'),
                    Item('order',
                        show_label=False,
                        editor=SetEditor(
                            name='axes',
                            ordered=True,
                            left_column_title='Available axes',
                            right_column_title='Selected',
                        ),
                    ),
                ),
                VGroup(
                    Item(label='Choose a function to calculate for each axis:'),
                    Item('order',
                        show_label=False,
                        style='custom',
                        editor=ListEditor(
                            use_notebook=True,
                            deletable=False,
                            page_name='.name',
                            style='custom',
                        ),
                    ),
                ),
            ),
            show_border=True,
        ),
        title='Calculate over axes for selected data',
        buttons=['OK', 'Cancel'],
        id='AxesOrder',
        resizable=True,
    )


def main(): 
    ao = AxesOrder(
#        axes=['Runs', 'Species', 'Compartments', 'Timepoints'],
#        axes=['Runs', 'Species', 'Compartments'],
    )
    result = ao.edit_traits(kind='modal')
    if result:
#        for axis in ao.order: print (axis.name.lower(), axis.function) # more like an ordered dictionary
        axes = [axis.name.lower() for axis in ao.order]
        functions = [axis.function for axis in ao.order]
        return axes, functions
            

if __name__ == '__main__':
    functions, axes = main()
    print functions
    print axes
