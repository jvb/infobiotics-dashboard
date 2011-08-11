import numpy as np
import sip
sip.setapi('QString', 1)
from enthought.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'qt4'
from enthought.traits.api import HasTraits, Instance, on_trait_change, Button, List
from enthought.traits.ui.api import View, Item
from enthought.mayavi import mlab
from enthought.mayavi.core.pipeline_base import PipelineBase
from enthought.mayavi.core.ui.mayavi_scene import MayaviScene
from enthought.mayavi.tools.mlab_scene_model import MlabSceneModel
from enthought.tvtk.pyface.scene_editor import SceneEditor
#from enthought.mayavi.core.ui.api import MlabSceneModel, SceneEditor
from PyQt4.QtGui import qApp
from enthought.pyface.ui.qt4.gui import GUI

class Surfaces(HasTraits):
    scene = Instance(MlabSceneModel, ())
    surfaces = List(Instance(PipelineBase))
    
    def __init__(self, arrays, **traits):
        HasTraits.__init__(self, **traits)
        self.arrays = arrays
        zmax = np.max(self.arrays)
        self.warp_scale = (1 / zmax) * 10

    def surf_default(self, arrayindex, **kwargs):
        surf = mlab.surf(self.arrays[arrayindex, :,:,0], 
            warp_scale=self.warp_scale,
            **kwargs)
        
        # Retrieve the LUT of the surf object.
        lut = surf.module_manager.scalar_lut_manager.lut.table.to_array()
        
        # The lut is a 255x4 array, with the columns representing RGBA
        # (red, green, blue, alpha) coded with integers going from 0 to 255.
        
        # We modify the alpha channel to add a transparency gradient
#        lut[:, -1] = np.linspace(0, 255, 256)
#        print lut.shape # (256, 4)
        if arrayindex == 1:
            lut[:, 0] = np.linspace(0, 255, 256) # red
            lut[:, 1] = np.linspace(0, 0, 256) # alpha
            lut[:, 2] = np.linspace(255, 0, 256) # blue
#            lut[:, 3] = np.linspace(0, 255, 256) # alpha
        else:
            lut[:, 0] = np.linspace(0, 0, 256) # red
            lut[:, 1] = np.linspace(0, 255, 256) # alpha
            lut[:, 2] = np.linspace(255, 0, 256) # blue
#            lut[:, 3] = np.linspace(0, 255, 256) # alpha
            
        
        # and finally we put this LUT back in the surface object. We could have
        # added any 255*4 array rather than modifying an existing LUT.
        surf.module_manager.scalar_lut_manager.lut.table = lut
        
        # We need to force update of the figure now that we have changed the LUT.
        mlab.draw()
        
        self.scene.scene_editor.isometric_view() #WARNING removing this line causes the surface not to display and the axes to rotate 90 degrees vertically!
        return surf
    
    @on_trait_change('scene.activated')
    def create_pipeline(self):
        kwargs = dict(
            #TODO colours
        )
        for i in range(len(self.arrays)): 
            self.surfaces.append(self.surf_default(i), **kwargs)
    
    play = Button
    def _play_fired(self):
        for i in range(len(self.arrays[0, :,:])):
            for surfaceindex in range(len(self.surfaces)):
                GUI.invoke_later(self.set_zindex, i, surfaceindex)

    def set_zindex(self, zindex, surfaceindex):
        self.surfaces[surfaceindex].mlab_source.set(scalars=self.arrays[surfaceindex, :, :, zindex])

    view = View(
        Item(
            'scene', 
            show_label=False, 
            editor=SceneEditor(scene_class=MayaviScene)
        ),
        Item('play', show_label=False),
        kind='panel', 
        resizable=True,
    )


#npzfile = np.load('/home/jvb/Desktop/pulseInverter.h5_surfaces.npz')
#proteinGFP = npzfile['proteinGFP']
#proteinCI = npzfile['proteinCI']
npzfile = np.load('/home/jvb/Desktop/ThreeLayers.h5_surfaces.npz')
FP1 = npzfile['FP1']
FP2 = npzfile['FP2']
arrays = np.array([FP1, FP2])    
surfaces = Surfaces(arrays)
    
if __name__ == '__main__':
    self = surfaces.edit_traits().control
    self.show()
    self.raise_()
    qApp.processEvents()
    exit(qApp.exec_())
    