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

class Histograms(HasTraits):
    
    data = Enum(['Compartments', 'Runs'])
    sum_species = Bool(False)
    bins = Range(2,100,10)
#    quanitities_display_units = Enum(...) #TODO

    results = Instance(McssResults)

#    min_timepoint_index = Int#(0)
#    max_timepoint_index = Int
#    from_timepoint_index = Range('min_timepoint_index', 'max_timepoint_index')#'to_timepoint_index') # infinite recursion
#    to_timepoint_index = Range('from_timepoint_index', 'max_timepoint_index') # 3D only
    from_timepoint_index = Int
    to_timepoint_index = Int

    amounts = Property(Array, depends_on='data')
    species_amounts_index = Property(Int, depends_on='data')

    _figure = Instance(Figure)
#    _scene = Instance(MlabSceneModel)


    @classmethod
    def fromfile(cls, file):
        return cls(results=McssResults(file))

    def __init__(self, results, **traits):
        assert results.num_selected_compartments > 1 or results.num_selected_runs > 1 
        HasTraits.__init__(self, results=results, **traits)
        self.max_timepoint_index = len(self.results.timepoints) - 1
        self.from_timepoint_index = self.max_timepoint_index // 2
        self.to_timepoint_index = self.max_timepoint_index
#        self.add_trait('from_timepoint_index', Range(0, max_timepoint_index, max_timepoint_index // 2))
#        self.add_trait('to_timepoint_index', Range(0, max_timepoint_index, max_timepoint_index))
        self.update()

    @on_trait_change('bins, data, sum_species, from_timepoint_index, to_timepoint_index, style')
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
                sum_mean_amounts_over_runs_over_species = sum(self.amounts, 0)
                data = sum_mean_amounts_over_runs_over_species[:, self.from_timepoint_index]
#                axes = self.update_plot(data)
            else:
#                for si in xrange(self.amounts.shape[0]):
#                    data = self.amounts[si, :, self.from_timepoint_index].T
                data = self.amounts[:, :, self.from_timepoint_index].T # transpose because species and compartments are the wrong way round for axes.hist
#                axes = self.update_plot(data)
                 
        else: # self.data == 'runs'
            if self.sum_species:
                sum_mean_amounts_over_compartments_over_species = sum(self.amounts, 1)
                data = sum_mean_amounts_over_compartments_over_species[:, self.from_timepoint_index]
#                axes = self.update_plot(data)
            else:
#                for si in xrange(self.amounts.shape[1]):
#                    data = self.amounts[:, si, self.from_timepoint_index]
                data = self.amounts[:, :, self.from_timepoint_index]
#                axes = self.update_plot(data)
        axes = self.update_plot(data)

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
           range=self._min_max(data) if self.sum_species else self._min_max(self.amounts),
           histtype=self.style, 
           alpha=0.5 if self.style == 'step' else 1, 
        )
#        print data, data.shape
        print hist#, hist.shape
        axes.legend()
        if self._figure.canvas is not None:
            self._figure.canvas.draw()
        return axes
    

    def __figure_default(self):
        return Figure(figsize=(12,10))


    def _min_timepoint_index_default(self):
        return 0

    def _max_timepoint_index_default(self):
        return len(self.results.timepoints) - 1


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

    
    def traits_view(self):
        basename = os.path.basename(self.results.filename)
        view = View(
            Item('_figure',
                show_label=False,
                editor=MatplotlibFigureEditor(
                    toolbar=True,
                    toolbar_above=False,
                ),
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
            Item('from_timepoint_index', 
                label='Timepoint index',
                editor=RangeEditor(
                    mode='slider',
                    low=0,
                    high=self.max_timepoint_index,
                ),
            ),
            width=800, height=600,
            resizable=True,
            title="%s histograms" % basename,
            id='Histograms',
        )
        return view


def test():
    Histograms.fromfile('../../../examples/tutorial-autoregulation/autoregulation_simulation.h5').configure_traits()


if __name__ == '__main__':
    test()
    