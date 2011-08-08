from __future__ import division
from enthought.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'qt4'
from enthought.traits.api import HasTraits, Instance, Range, Int, Float 
from matplotlib.figure import Figure
from enthought.traits.ui.api import View, VGroup, HGroup, Item, Spring
from enthought.pyface.api import FileDialog, OK
    
class MatplotlibFigureSize(HasTraits):
    
    figure = Instance(Figure)
    def _figure_changed(self):
        if self.figure is not None:
            self.dpi = self.figure.dpi
            self.width_inches, self.height_inches = self.figure.bbox_inches.size
        
    dpi = Range(60, 2400, 100)
    width_pixels = Int(640)
    height_pixels = Int(480)
    width_inches = Float(6.4)
    height_inches = Float(4.8)
    
    def _dpi_changed(self):
        self.width_pixels = int(self.width_inches * self.dpi)
        self.height_pixels = int(self.height_inches * self.dpi)
    
    def _width_pixels_changed(self):
        self.width_inches = self.width_pixels / self.dpi    
    
    def _height_pixels_changed(self):
        self.height_inches = self.height_pixels / self.dpi

    def _width_inches_changed(self):
        self.width_pixels = int(self.width_inches * self.dpi)

    def _height_inches_changed(self):
        self.height_pixels = int(self.height_inches * self.dpi)
        
    view = View(
        VGroup(
            HGroup(
                Item('width_inches', label='width'),
                Item('height_inches', label='height'),
                label='inches',
            ),
            HGroup(
                Spring(),
                Item('dpi', label='Dots per inch'),
                Spring(),
            ),
            HGroup(
                Item('width_pixels', label='width'),
                Item('height_pixels', label='height'),
                label='pixels',
            ),
            show_border=True,
        ),
        buttons=['OK', 'Cancel'],
        title='Adjust figure size',
    )


def resize_and_save_matplotlib_figure(figure):        
    ''' To save a matplotlib figure with custom width and height in pixels 
    requires changing the bounding box while is being rendered! '''
   
    # get figure size
    figure_size = MatplotlibFigureSize(figure=figure)
    old_dpi = figure_size.dpi
    old_width_inches = figure_size.width_inches
    old_height_inches = figure_size.height_inches
    ui = figure_size.edit_traits(kind='modal')
    
    # maybe change figure size
    if ui.result:
        figure.dpi = figure_size.dpi # set new dpi
        figure.bbox_inches.p1 = figure_size.width_inches, figure_size.height_inches # set new width and height in inches
    else:
        return

    # get file name with (correct choice of formats)
    fd = FileDialog(
        action='save as',
        wildcard=FileDialog.create_wildcard('All available formats', ['*.eps', '*.png', '*.pdf', '*.ps', '*.svg']),
    )
    if fd.open() != OK:
        return
    file_name = fd.path
    
    # save it
    figure.savefig(file_name)

    # restore original figure size
    figure.dpi = old_dpi # restore old dpi
    figure.bbox_inches.p1 = old_width_inches, old_height_inches # restore old width and height in inches
        

def test_resize_and_save_matplotlib_figure():
    from enthought.traits.api import HasTraits, Instance, Button
    from enthought.traits.ui.api import View, VGroup, HGroup, Item, Spring
    from matplotlib.figure import Figure
    from infobiotics.commons.traits.ui.qt4.matplotlib_figure_editor import MatplotlibFigureEditor
    
    class Example(HasTraits):
        figure = Instance(Figure, ())
        
        def traits_view(self):
            return View(
#                VGroup(
                    Item('figure',
                        show_label=False,
                        editor=MatplotlibFigureEditor(
                            toolbar=True
                        ),
                    ),
#                    HGroup(
#                        Spring(),
#                        Item('save_resized', show_label=False),
#                    ),
#                ),
                resizable=True,
            )
        # use 'Save resized' button on MatplotlibFigureEditor toolbar instead
#        save_resized = Button
#        def _save_resized_fired(self):
#            resize_and_save_matplotlib_figure(self.figure)
    
    example = Example()
    fig = example.figure
    ax = fig.add_subplot(111)
    ax.plot(range(10))
#    resize_and_save_matplotlib_figure(fig)
    example.configure_traits()
    

if __name__ == '__main__':
    test_resize_and_save_matplotlib_figure()
    
