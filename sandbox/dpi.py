from __future__ import division
import os; os.environ['ETS_TOOLKIT'] = 'qt4'

from enthought.traits.api import HasTraits, Int, Float, Property, on_trait_change
from enthought.traits.ui.api import View, VGroup, HGroup, Item

from enthought.traits.api import HasTraits, Instance, Str, Button
from matplotlib.figure import Figure
from enthought.traits.ui.api import View, VGroup, Item, Spring
from infobiotics.commons.traits.ui.qt4.matplotlib_figure_editor import MPLFigureEditor

from enthought.pyface.api import FileDialog, OK

class FigureSize(HasTraits):
    
    figure = Instance(Figure)
    def _figure_changed(self):
        if self.figure is not None:
            self.dpi = self.figure.dpi
            self.width_inches, self.height_inches = self.figure.bbox_inches.size
        
    dpi = Int(100)
    width_pixels = Int(640) #TODO use Property?
    height_pixels = Int(480)
    width_inches = Float(6.4)
    height_inches = Float(4.8)
    
    def _dpi_changed(self):
        self.width_pixels = int(self.width_inches * self.dpi) #FIXME gets increasingly ridiculous as dpi tends to 1
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
        buttons=['OK','Cancel'],
        title='Adjust figure size',
    )


class TraitsPlot(HasTraits):
    figure = Instance(Figure, ())
    title = Str('title')
    
    def traits_view(self):
        return View(
            VGroup(
                Item('figure',
                    show_label=False,
                    editor=MPLFigureEditor(
                        toolbar=True
                    ),
                ),
                HGroup(
                    Spring(),
                    Item('save_resized', show_label=False),
                ),
            ),
            resizable=True,
            title=self.title
        )
        
    save_resized = Button
    def _save_resized_fired(self):
        ''' To save a matplotlib figure with custom width and height in pixels 
        requires changing the bounding box while is being rendered! '''
        
        # get figure size
        figure_size = FigureSize(figure=self.figure)
        old_dpi = figure_size.dpi
        old_width_inches = figure_size.width_inches
        old_height_inches = figure_size.height_inches
        ui = figure_size.edit_traits(kind='modal')
        
        # maybe change figure size
        if ui.result:
            self.figure.dpi = figure_size.dpi # set new dpi
            self.figure.bbox_inches.p1 = figure_size.width_inches, figure_size.height_inches # set new width and height in inches
        else:
            return

        # get file name with (correct choice of formats)
        fd = FileDialog(
            action='save as',
            wildcard=FileDialog.create_wildcard('All available formats', ['*.eps','*.png', '*.pdf', '*.ps', '*.svg']),
        )
        if fd.open() != OK:
            return
        file_name = fd.path
        
        # save it
        self.figure.savefig(file_name)

        # restore original figure size
        self.figure.dpi = old_dpi # restore old dpi
        self.figure.bbox_inches.p1 = old_width_inches, old_height_inches # restore old width and height in inches
        

if __name__ == '__main__':
    traits_plot = TraitsPlot()
    fig = traits_plot.figure
    ax = fig.add_subplot(111)
    ax.plot(range(10))
    traits_plot.configure_traits()
    
