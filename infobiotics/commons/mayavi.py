from numpy import min, max
import numpy as np

def extent(x, y, z):
    return [min(x), max(x), min(y), max(y), min(z), max(z)]  

def normalize(value, maximum, minimum, scale=1):
    return ((value - minimum) / (maximum - minimum)) * scale

def normalized_extent(x, y, z):
    """ Returns a list [xmin, xmax, ymin, ymax, zmin, zmax] where min = 0 and max = 1.
 
    By normalizing the extents of the surface we get a 3D plot that fits 
    perfectly into a cube, even when there are many more x values than y values
    and vice versa.
    
    """
    xmin = min(x)
    xmax = max(x)
    ymin = min(y)
    ymax = max(y)
    zmin = min(z)
    zmax = max(z)
    return [
        normalize(xmin, xmax, xmin), 
        normalize(xmax, xmax, xmin), 
        normalize(ymin, ymax, ymin), 
        normalize(ymax, ymax, ymin), 
        normalize(zmin, zmax, zmin), 
        normalize(zmax, zmax, zmin)
    ] 

def normalize_array_by_other_array(a, other):
    min = np.min(other)
    return (a - min) * 1 / (np.max(other) - min)
    # brackets are vital here because only '(a - min)' returns an array

def normalized_extent_z_by_other_array(x, y, z, other):
    xmin = min(x)
    xmax = max(x)
    ymin = min(y)
    ymax = max(y)
    normalized_z = normalize_array_by_other_array(z, other)
    zmin = min(normalized_z)
    zmax = max(normalized_z)
    return [
        normalize(xmin, xmax, xmin), 
        normalize(xmax, xmax, xmin), 
        normalize(ymin, ymax, ymin), 
        normalize(ymax, ymax, ymin), 
        zmin, 
        zmax,
    ] 
    
def anim():
    from enthought.mayavi import mlab as M
    M.options.offscreen = True
    M.test_mesh()
    f = M.figure()
    print f
    for i in range(36):
        f.scene.camera.azimuth(10)
        M.savefig('img%02i.png'%i)

import os
os.environ['ETS_TOOLKIT'] = 'qt4' # must be before any traits imports AND must use qApp not QApplication(sys.argv)
from enthought.traits.api import HasTraits, Range, Instance, on_trait_change
from enthought.traits.ui.api import View, Item#, HGroup
from enthought.mayavi.tools.mlab_scene_model import MlabSceneModel
from enthought.tvtk.pyface.scene_editor import SceneEditor
from enthought.mayavi.core.ui.mayavi_scene import MayaviScene
class MlabWidget(HasTraits):

    # initialize traits
    scene = Instance(MlabSceneModel, args=()) # why args=() and not just ()?
    view = View(
                Item('scene', 
                     show_label=False, # get rid of 'Scene:' to the left of the view
#                     resizable=True,
                     padding=0,
                     editor=SceneEditor(scene_class=MayaviScene) # scene_class=MayaviScene adds a Mayavi icon to toolbar
                     ),
                kind='panel', # specifying the kind of view as a panel allows us to treat it as a widget...
#                scrollable=True, 
                resizable=True # ...and make it resize with the layout it is in.
                ) 

    def __init__(self):
        HasTraits.__init__(self)
        self._widget = None
        
    def widget(self):
        if self._widget == None:
#            self._widget = self.edit_traits(
#                view=View(
#                          Item('scene',
#                              editor=SceneEditor(scene_class=MayaviScene),
#                              show_label=False
#                              ),
#                          kind='panel',
#                          resizable=True
#                          )).control 
            self._widget = self.edit_traits().control
            self._widget.setContentsMargins(20,20,20,20) # doesn't do anything
        return self._widget
