from __future__ import division
import os; os.environ['ETS_TOOLKIT'] = 'qt4'

from enthought.traits.api import HasTraits, Int, Float, Property, on_trait_change
from enthought.traits.ui.api import View, VGroup, HGroup, Item

class Test(HasTraits):
    
    dpi = Int(100)
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
        
#    @on_trait_change('width_pixels, height_pixels')
#    def set_inches(self):
#        self.width_inches = self.width_pixels / self.dpi
#        self.height_inches = self.height_pixels / self.dpi
    
#    @on_trait_change('dpi, width_inches, height_inches')
#    def set_pixels(self):
#        self.width_pixels = int(self.width_inches * self.dpi)
#        self.height_pixels = int(self.height_inches * self.dpi)
    
    view = View(
        VGroup(
            Item('dpi', label='Dots per inch'),
            HGroup(
                Item('width_pixels', label='width'),
                Item('height_pixels', label='height'),
                label='pixels',
            ),
            HGroup(
                Item('width_inches', label='width'),
                Item('height_inches', label='height'),
                label='inches',
            ),
            show_border=True,
        ),
    )


Test().configure_traits()
