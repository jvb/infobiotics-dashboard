from __future__ import division
import warnings
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import infobiotics
from enthought.traits.api import *
from enthought.traits.ui.api import *

from infobiotics.mcss.results.mcss_results import McssResults, mean, sum
import numpy as np

from infobiotics.commons.traits.ui.qt4.matplotlib_figure_editor import MatplotlibFigureEditor
from matplotlib.figure import Figure
#from matplotlib.font_manager import FontProperties
#from matplotlib.lines import Line2D
from matplotlib.axes import Axes#, Subplot as AxesSubplot

import os.path

from enthought.mayavi import mlab
from enthought.mayavi.core.pipeline_base import PipelineBase
from enthought.mayavi.core.ui.mayavi_scene import MayaviScene
from enthought.mayavi.tools.mlab_scene_model import MlabSceneModel
from enthought.tvtk.pyface.scene_editor import SceneEditor


class Histograms(HasTraits):
    
    data = Enum(['Compartments', 'Runs'])
    sum_species = Bool(False)
    bins = Range(2,100,10)
#    quanitities_display_units = Enum(...) #TODO

    results = Instance(McssResults)

    max_timepoint_index = Int
    from_timepoint_index = Int
    to_timepoint_index = Int

    amounts = Property(Array, depends_on='data')
    species_amounts_index = Property(Int, depends_on='data')

    _figure = Instance(Figure)
    scene = Instance(MlabSceneModel, ())
    surfaces = List(Instance(PipelineBase))


    def _max_timepoint_index_default(self):
        return len(self.results.timepoints) - 1

    def _from_timepoint_index_default(self):
        return self.max_timepoint_index // 2

    def _to_timepoint_index_default(self):
        return self.max_timepoint_index

    def _data_default(self):
        if self.results.num_selected_compartments > 1:
            return 'Compartments'
        else:
            return 'Runs'

    @cached_property
    def _get_amounts(self):
        if self.data == 'Compartments':
            return self.results.functions_of_amounts_over_runs(mean)[0] # (species, compartments, timepoints)
        else: # self.data == 'runs'
            return mean(self.results.amounts(), self.results.amounts_axes.index('compartments')) # (runs, species, timepoints)
    
    @cached_property
    def _get_species_amounts_index(self):
        if self.data == 'Compartments':
            return 0 # (species, compartments, timepoints)
        else: # self.data == 'runs'
            return 1 # (runs, species, timepoints)


    @classmethod
    def fromfile(cls, file):
        return cls(results=McssResults(file))

    def __init__(self, results, **traits):
        assert results.num_selected_compartments > 1 or results.num_selected_runs > 1 
        HasTraits.__init__(self, results=results, **traits)
        self.update()

    @on_trait_change('data, sum_species, bins, style, from_timepoint_index, to_timepoint_index')
    def update(self):
        '''
        
        matplotlib:
            hist(x, bins=10, range=None, normed=False, cumulative=False,
                 bottom=None, histtype='bar', align='mid',
                 orientation='vertical', rwidth=None, log=False, **kwargs)
            Compute and draw the histogram of x. The return value is a tuple 
            (n, bins, patches) or ([n0, n1, ...], bins, [patches0, patches1,...]) 
            if the input contains multiple data.
            
            Multiple data can be provided via x as a list of datasets of 
            potentially different length ([x0, x1, ...]), or as a 2-D ndarray in
            which each column is a dataset. Note that the ndarray form is 
            transposed relative to the list form.
        '''
        # 2D
        if self.data == 'Compartments':
            if self.sum_species:
                sum_mean_amounts_over_runs_over_species = sum(self.amounts, self.species_amounts_index)
                data = sum_mean_amounts_over_runs_over_species[:, self.from_timepoint_index]
#                axes = self.update_plot(data)
            else:
#                for si in xrange(self.amounts.shape[0]):
#                    data = self.amounts[si, :, self.from_timepoint_index].T
                data = self.amounts[:, :, self.from_timepoint_index].T # transpose because species and compartments are the wrong way round for axes.hist
#                axes = self.update_plot(data)
                 
        else: # self.data == 'runs'
            if self.sum_species:
                sum_mean_amounts_over_compartments_over_species = sum(self.amounts, self.species_amounts_index)
                data = sum_mean_amounts_over_compartments_over_species[:, self.from_timepoint_index]
#                axes = self.update_plot(data)
            else:
#                for si in xrange(self.amounts.shape[1]):
#                    data = self.amounts[:, si, self.from_timepoint_index]
                data = self.amounts[:, :, self.from_timepoint_index]
#                axes = self.update_plot(data)
        axes = self.update_plot(data)
        
        # 3D
#        self.update_surface()

    style = Enum(['bar', 'step'], desc='type of histogram to plot (larger bin sizes are recommended with step') 

    def _min_max(self, quantities):
        return (np.min(quantities.magnitude), np.max(quantities.magnitude))

    def update_plot(self, data):
        self._figure.clear()
        axes = self._figure.add_subplot(1,1,1)
        axes.grid(True)
        label = [species.name for species in self.results.species]
        hist, bins, patches = axes.hist(data, self.bins, 
           label = ', '.join(label) if self.sum_species else label,
#           range=self._min_max(data) if self.sum_species else self._min_max(self.amounts),
           range=(0, np.max(data.magnitude)) if self.sum_species else self._min_max(self.amounts),
           histtype=self.style, 
           alpha=0.5 if self.style == 'step' else 1, 
        )
#        print data, data.shape
#        print hist
        if not self.sum_species:
            axes.legend()
        if self._figure.canvas is not None:
            self._figure.canvas.draw()
        self._figure.suptitle(self.maketitle().split(' to')[0])
        return axes

    def __figure_default(self):
        return Figure(figsize=(12,10))
    
    def maketitle(self):
        return "Histograms TODO from %.1f to %.1f" % (self.results.timepoints[self.from_timepoint_index], self.results.timepoints[self.to_timepoint_index])#, self.timepoints_display_units)
    
    def update_surface(self):
        slice_ = slice(self.from_timepoint_index, self.to_timepoint_index)
        histograms = self.results.histograms(self.bins, self.data, self.sum_species)
#        print histograms.shape, # (5, 121)
#        print histograms['bin_edges'].shape, # (5, 121, 11) 
#        print histograms['histogram'].shape # (5, 121, 10)
        if self.sum_species:
            bin_edges = histograms['bin_edges'][slice_]
            arrays = histograms['histogram'][slice_]
        else:
            bin_edges = histograms['bin_edges'][:, slice_]
            arrays = histograms['histogram'][:, slice_]
#        print self.sum_species, bin_edges.shape, arrays.shape # False (5, 60, 11) (5, 60, 10)
        self.bin_edges = bin_edges[0]
        self.arrays = arrays
        
    arrays = Array
    
#    @on_trait_change('scene.activated')
    def create_pipeline(self, object, name, old, new):
        
        if name == 'arrays':
            self.view_parameters = self.scene.mlab.view()[:3]
        else:
            self.on_trait_change(self.create_pipeline, 'arrays')
        
        xmin, xmax = self._min_max(sum(self.amounts, self.species_amounts_index)) if self.sum_species else self._min_max(self.amounts) 
        self.extent = [
            xmin, xmax,
            self.from_timepoint_index, self.to_timepoint_index, #TODO replace with actual timepoints
            np.min(self.bin_edges[0]), np.max(self.bin_edges[0]), # invariant, computed in McssResults.histograms
        ]
        
        self.warp_scale = 1 / max([self.extent[-3] - self.extent[-4], self.extent[-1] - self.extent[-2]]) 
        
#        figure=self.scene.mayavi_scene
#        self.scene.mlab.figure(1, bgcolor=(0,0,0))
        self.scene.mlab.clf()

#        print self.arrays.shape
        for i in range(len(self.arrays)):
            self.surfaces.append(self.surf_default(i))
#        scalarbar = self.scene.mlab.scalarbar(self.surfaces[1], str(self.quantities_display_units), "vertical", 5, None, '%.f')
#        scalarbar.title_text_property.set(font_size=4, italic=0, bold=0)
#        scalarbar.label_text_property.set(font_size=4, italic=0, bold=0)#, line_spacing=0.5)
#        scalar_bar_widget = self.surfaces[1].module_manager.scalar_lut_manager.scalar_bar_widget
#        scalar_bar_widget.representation.set(position=[0.827, 0.0524], position2=[0.1557, 0.42])


        title = self.scene.mlab.title(self.maketitle(), size=0.5, height=0.91)#, figure=figure)
        title.x_position = 0.03
        title.actor.width = 0.9

        axes = self.scene.mlab.axes(
            ranges=self.extent, 
            xlabel="amounts (TODO)", 
            ylabel="Time (TODO)", 
            z_axis_visibility=True, 
            zlabel='Frequency')#self.quantities_display_units
        axes.label_text_property.set(italic=0, bold=0)
        axes.axes.number_of_labels = 3
            
        self.scene.scene_editor.isometric_view() # recenter
        self.scene.mlab.view(*self.view_parameters) # restore previous perspective
    
    view_parameters = Tuple(Float, Float, Float)
    def _view_parameters_default(self):
        return -44.890778452007545, 86.466712805369198, 98.476018229363234
    
    reset_view = Button
    def _reset_view_fired(self):
        self.scene.mlab.view(*self._view_parameters_default())
    
    def surf_default(self, arrayindex):
        array = self.arrays[arrayindex].T
#        surf = self.scene.mlab.surf(
#            array,
#            warp_scale=self.warp_scale,
#            opacity=0.5,
#        )
        surf = self.scene.mlab.barchart(
            array,
#            extent=self.extent,
            auto_scale=True,
#            lateral_scale=0.8,
#            figure=figure
#            reset_zoom=True,
            scale_factor=self.warp_scale,
        )

#        lut = surf.module_manager.scalar_lut_manager.lut.table.to_array()
#        if arrayindex == 0:
#            lut = black_to_green_lut_table
#        elif arrayindex == 1:
#            lut = black_to_red_lut_table
#        surf.module_manager.scalar_lut_manager.lut.table = lut
#        self.scene.mlab.draw()

        return surf

    
    def traits_view(self):
        basename = os.path.basename(self.results.filename)
        view = View(
            HSplit(
                Item('_figure',
                    show_label=False,
                    editor=MatplotlibFigureEditor(
                        toolbar=True,
                        toolbar_above=False,
                    ),
                ),
#                Item('scene', 
#                    show_label=False, 
#                    editor=SceneEditor(scene_class=MayaviScene)
#                ),
            ),
            HGroup(
                Item('data', 
#                    label='',
                    enabled_when="object.results.num_selected_compartments > 1 and object.results.num_selected_runs > 1"    
                ),
                'sum_species',
                'bins',
                'style',
            ),
#            Item('play', show_label=False), #TODO QTimer.timeout()
            Item('from_timepoint_index', 
                label='Timepoint index',
                editor=RangeEditor(
                    mode='slider',
                    low=0,
                    high=self.max_timepoint_index-1,
                ),
            ),
            Item('reset_view', show_label=False),
            width=800, height=600,
            resizable=True,
            title="%s histograms" % basename,
            id='Histograms',
        )
        return view


# from histograms2.HistogramWidget.HistogramWidget.onDraw
#        self.axes.set_title(self.title)
#        
#        self.axes.grid(self.showGridCheckBox.isChecked())
#        
#        self.axes.set_yscale('log' if self.logScaleCheckBox.isChecked() else 'linear',
#                             basey=float(self.logBaseComboBox.currentText()))
#
#        self.axes.hist(self.data,
#                       bins=self.binsSlider.value(),
#                       cumulative=False,
#                       histtype='bar', #'barstacked','step','stepfilled',
#                       log=False)
#        
#        self.canvas.draw()



def test():
    Histograms.fromfile('../../../examples/tutorial-autoregulation/autoregulation_simulation.h5').configure_traits()


if __name__ == '__main__':
    test()
    