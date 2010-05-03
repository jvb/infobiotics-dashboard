from enthought.traits.api import HasTraits, Int, List, Tuple, Float
from enthought.traits.ui.api import View, Item, RangeEditor
#
#class Test(HasTraits):
#    
#    ranges = List(Tuple(Str, Tuple(Float, Float, Float)))
#    
#    def traits_view(self):
#        items = []
#        for range in self.ranges:
#            pass
#            item = Item(editor=RangeEditor())
#            
#        return View(
#            *items
#        )
#    
#    
#if __name__ == '__main__':
#    Test(ranges=[('a',(0,1,10)),('b'(1.0,0.5,20))]).configure_traits()
#    
    
    
## object_trait_attrs.py --- Example of per-object trait attributes
#from enthought.traits.api import HasTraits, Range
#
#class GUISlider(HasTraits):
#
#    def __init__(self, eval=None, label='Value',
#                 trait=None, min=0.0, max=1.0,
#                 initial=None, **traits):
#        HasTraits.__init__(self, **traits)
#        if trait is None:
#            if min > max:
#                min, max = max, min
#            if initial is None:
#                initial = min
#            elif not (min <= initial <= max):
#                initial = [min, max][
#                            abs(initial - min) >
#                            abs(initial - max)]
#            trait = Range(min, max, value = initial)
#        self.add_trait(label, trait)
        
        
from enthought.traits.api import HasTraits, Range

class GUISlider(HasTraits):

    def __init__(self, eval=None, label='Value',
                 trait=None, min=0.0, max=1.0,
                 initial=None, **traits):
        HasTraits.__init__(self, **traits)
        if trait is None:
            if min > max:
                min, max = max, min
            if initial is None:
                initial = min
            elif not (min <= initial <= max):
                initial = [min, max][
                            abs(initial - min) >
                            abs(initial - max)]
            trait = Range(min, max, value = initial)
        self.add_trait(label, trait)
        print label
        
    def add_slider(self, name, min, max, initial, ):
        
if __name__ == '__main__':
    GUISlider(initial=0.5).configure_traits()
        
        
        
                