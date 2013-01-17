from __future__ import division
#import sip; sip.setapi('QString', 2)
from traits.etsconfig.api import ETSConfig; ETSConfig.toolkit = 'qt4'
from traits.api import HasTraits, Instance, Float, Range, on_trait_change
from traitsui.api import View, Item, VGroup
#from tvtk.pyface.scene_model import SceneModel
#from tvtk.pyface.scene_editor import SceneEditor
from mayavi.core.ui.api import MlabSceneModel, SceneEditor
import numpy as np

class MyModel(HasTraits):
#    scene = Instance(SceneModel, ())
    scene = Instance(MlabSceneModel, ())

    from_ = Float
    to = Float
    timestep = Float
    time = Range('from_', 'to', 'timestep')

    view = View(
        Item('scene',
            height=400,
            show_label=False,
            editor=SceneEditor(),
        ),
        VGroup(
#           'meridional', 'transverse'
            'time'
        ),
    )

#    def example(self):
#        from mayavi.__version__ import __version__ as mayavi_version
#        major, minor, micro = mayavi_version.split('.')
#        if major > 3 or (major == 3 and (minor > 2 or (minor == 2 and micro > 1))): 
#            self.scene.mlab.points3d(x, y, z, s, figure=self.scene.mayavi_scene)
#        else:
#            self.scene.mlab.points3d(x, y, z, s)

    def __init__(self, surfaces, xy_min_max, **traits):
        HasTraits.__init__(self, **traits)
        self.surfaces = surfaces
        self.xy_min_max = xy_min_max

    @on_trait_change('scene.activated')
    def create_plot(self):
        (xmin, xmax), (ymin, ymax) = self.xy_min_max
        ranges = [xmin, xmax, ymin, ymax, 0, None]
        
        def _min_max_generator(xmin, xmax, ymin, ymax):
            size = xmax - xmin if xmax - xmin < ymax - ymax else ymax - ymin
            min = 0
            max = min + size
            yield min, max
            while True:
                min = min + 2 * size
                max = min + size
                yield min, max
        
        min_max_generator = _min_max_generator(xmin, xmax, ymin, ymax)    
        
        if xmax - xmin > ymax - ymin:
            longest = 'x'
            zmax = ymax + ymin
        else:
            longest = 'y'
            zmax = xmax + xmin
        
        zmin = 0

        for surface in self.surfaces:
        
            min, max = min_max_generator.next()
                
            if longest == 'x':
                ymin = min
                ymax = max
            else:
                xmin = min
                xmax = max
                
            extent = [
                xmin,
                xmax,
                ymin,
                ymax,
                zmin, #=0,
                zmax, #=np.max(surface),
            ]
            
            data = surface.data
            index_of_greatest_value = np.unravel_index(np.argmax(data), data.shape)[-1] # v.important
            surf = self.scene.mlab.surf(
                data[:, :, index_of_greatest_value], # cross-section in time
                extent=extent,
#                warp_scale=(1 / np.max(surface.data) * zmax),
            )
            surface.surf = surf

#            self.scene.mlab.outline(surf, extent=extent)
            ranges[5] = np.max(surface.data)
            self.scene.mlab.axes(
                surf,
                color=(.7, .7, .7),
                nb_labels=3,
#                extent=extent,
                ranges=ranges,
                xlabel='',
                ylabel='',
                zlabel='',
                x_axis_visibility=False,
                y_axis_visibility=False,
#                z_axis_visibility=False,
            )
            self.scene.mlab.text(xmax + xmax / 3, ymax - ((ymax - ymin) / 2), surface.species, z=zmin, width=0.13)
#            self.scene.mlab.text3d(xmax + xmax / 3, ymax - ((ymax - ymin) / 2), zmin, species)        
        
#        self.scene._update_view(1, 1, 1, 0, 0, 1) # isometric view
#        self.scene._update_view(1, 1.2, 1, 0, 0, 1) # isometric view tilted upwards
        self.scene.mlab.view(45.0, 65, 115, np.array([ 15., 25., 5.]))
        
        self.update_plot(0)

    @on_trait_change('time')
    def update_plot(self, time):
        time_index = int(self.from_ - self.to_)
#        print time #TODO
        for surface in self.surfaces:
            surface.surf.mlab_source.scalars = surface.data[:, :, time_index]

#    @on_trait_change('scene.activated')
#    def create_plot(self):
#        x, y, z, t = curve(self.meridional, self.transverse)
#        self.plot = self.scene.mlab.plot3d(x, y, z, t, colormap='Spectral')
##        self.scene._update_view(1, 1, 1, 0, 0, 1) # isometric view
#        self.scene._update_view(1, 1.2, 1, 0, 0, 1) # isometric view tilted upwards
#
#    meridional = Range(1, 30, 6)
#    transverse = Range(0, 30, 11)
#
#    @on_trait_change('meridional, transverse')
#    def update_plot(self):
#        x, y, z, t = curve(self.meridional, self.transverse)
#        self.plot.mlab_source.set(x=x, y=y, z=z, scalars=t)
#
#from numpy import linspace, pi, cos, sin
#def curve(n_mer, n_long):
#    phi = linspace(0, 2 * pi, 2000)
#    return [ cos(phi * n_mer) * (1 + 0.5 * cos(n_long * phi)),
#            sin(phi * n_mer) * (1 + 0.5 * cos(n_long * phi)),
#            0.5 * sin(n_long * phi),
#            sin(phi * n_mer)]

class Surface(object):
    def __init__(self, species, data):
        self.species = species
        self.data = data
        self.surf = None
        
def setup():
    '''
    Create McssResults
    Select species
    Create Surfaces with species and surface data (x, y, timepoints)
    '''
    import mcss_results
    results = mcss_results.McssResults('tests/pulsePropagation-2_runs.h5')
#    print results.timepoints
    #print results.species_information(); exit()
    species = 'proteinGFP', 'proteinCI', 'proteinLuxI'
    results.select_species(*species)
    surfaces = results.surfaces()
    means = mcss_results.mean(surfaces, 0)
#    zmax = np.max(mcss_results.mean(surfaces, 0))
    return results, [Surface(s, means[i]) for i, s in enumerate(species)]

def configure():
    results, surfaces = setup()
    MyModel(
        surfaces,
        results.xy_min_max(),
        from_=float(results.from_),
        to=float(results.to),
        timestep=float(results.timestep),
    ).configure_traits()

def Qt():
    from PyQt4 import QtGui
    class MainWindow(QtGui.QMainWindow):
        def __init__(self, parent=None):
            QtGui.QWidget.__init__(self, parent)
            self.visualization = MyModel()
            self.ui = self.visualization.edit_traits().control
            self.setCentralWidget(self.ui)
    window = MainWindow()
    window.show()
    QtGui.qApp.exec_()


if __name__ == '__main__':
    configure()
#    Qt()

#    MyModel().edit_traits()
