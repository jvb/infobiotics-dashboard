import numpy as np
import sip
sip.setapi('QString', 1)
from enthought.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'qt4'
from enthought.traits.api import HasTraits, Instance, on_trait_change, Button
from enthought.traits.ui.api import View, Item
from enthought.mayavi import mlab
from enthought.mayavi.core.pipeline_base import PipelineBase
from enthought.mayavi.core.ui.mayavi_scene import MayaviScene
from enthought.mayavi.tools.mlab_scene_model import MlabSceneModel
from enthought.tvtk.pyface.scene_editor import SceneEditor
#from enthought.mayavi.core.ui.api import MlabSceneModel, SceneEditor

#npzfile = np.load('/home/jvb/Desktop/pulseInverter.h5_surfaces.npz')
#proteinGFP = npzfile['proteinGFP']
#proteinCI = npzfile['proteinCI']

npzfile = np.load('/home/jvb/Desktop/ThreeLayers.h5_surfaces.npz')
#print npzfile.files
#exit()

FP1 = npzfile['FP1']
FP2 = npzfile['FP2']


class Surf(HasTraits):
    scene = Instance(MlabSceneModel, ())
    surf = Instance(PipelineBase) # surf = plot
#    def _scene_default(self):
#        return MlabSceneModel()
    
    def __init__(self, array, **traits):
        HasTraits.__init__(self, **traits)
        self.array = array
        zmax = np.max(self.array)
        self.warp_scale = (1 / zmax) * 10
#        (xmin, xmax), (ymin, ymax) = (0, len(self.array)), (0, len(self.array[0]))
#        zmin = 0 #TODO not if we are subtracting
#        self.extent = [xmin, xmax, ymin, ymax, zmin, zmax]

    def surf_default(self):
        surf = mlab.surf(self.array[:,:,0], 
#            extent=self.extent, 
            warp_scale=self.warp_scale)
        self.scene.scene_editor.isometric_view() #WARNING removing this line causes the surface not to display and the axes to rotate 90 degrees vertically!
        return surf
    
    @on_trait_change('scene.activated')
    def create_pipeline(self):
        self.surf = self.surf_default() 
    
    play = Button
    def _play_fired(self):
        import time
        for i in range(len(self.array[:,:])):
            from enthought.pyface.ui.qt4.gui import GUI
            GUI.invoke_later(self.set_zindex, i)
#            time.sleep(0.1)

    def set_zindex(self, zindex):
        self.surf.mlab_source.set(scalars=self.array[:, :, zindex])

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
    
    
if __name__ == '__main__':    
    #mlab.show()
    from PyQt4.QtGui import qApp
    self = Surf(FP1).edit_traits().control
    self.show()
    self.raise_()
    qApp.processEvents()
    exit(qApp.exec_())
    