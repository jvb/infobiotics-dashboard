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


class Histograms(HasTraits):
    
    bins = Int(10)
    data = Enum(['Compartments', 'Runs'])
    sum_species = Bool(False)
#    quanitities_display_units

    from_timepoint_index = Int
    
    def _from_timepoint_index(self):
        return len(self.results.timepoints) - 1
    
    to_timepoint_index = Int # 3D only

    results = Instance(McssResults)
    amounts = Property(Array, depends_on='data')

#    scene = Instance(MlabSceneModel)
    
    @classmethod
    def fromfile(cls, file):
        return cls(results=McssResults(file))

    def __init__(self, results, **traits):
        HasTraits.__init__(self, results=results, **traits)

    @cached_property
    def _get_amounts(self):
        if self.data == 'compartments':
            return self.results.functions_of_amounts_over_runs(mean)[0] # (species, compartments, timepoints)
        else: # self.data == 'runs'
            return mean(self.results.amounts(), self.results.amounts_axes.index('compartments')) # (runs, species, timepoints)
            
    def update_plot(self, data):
        self._figure.clear()
        axes = self._figure.add_subplot(1,1,1)
        axes.grid(True)
        hist, bins, patches = axes.hist(data, self.bins)
        self._figure.canvas.draw()
        return axes        
            
    @on_trait_change('bins, data, sum_species, from_timepoint_index, to_timepoint_index')
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
        if self.data == 'compartments':
            if self.sum_species:
                sum_mean_amounts_over_runs_over_species = sum(self.amounts, 0)
                data = sum_mean_amounts_over_runs_over_species[:, self.from_timepoint_index]
                axes = self.update_plot(data)
            else:
                numspecies = self.amounts.shape[0]
#                for si in xrange(numspecies):
#                    data = self.amounts[si, :, self.from_timepoint_index]
#                data = self.amounts[:, :, self.from_timepoint_index]
                data = self.amounts[:, :, self.from_timepoint_index].T
                axes = self.update_plot(data)
                 
        else: # self.data == 'runs'
            if self.sum_species:
                sum_mean_amounts_over_compartments_over_species = sum(self.amounts, 1)
                data = sum_mean_amounts_over_compartments_over_species[:, self.from_timepoint_index]
                axes = self.update_plot(data)
            
            else:
#                for si in xrange(numspecies):
#                    data = self.amounts[:, si, self.from_timepoint_index]
#                data = self.amounts[:, :, self.from_timepoint_index].T # transpose because runs and species are the wrong way round
                data = self.amounts[:, :, self.from_timepoint_index]
                axes = self.update_plot(data)
    
    
    _figure = Instance(Figure)
    
    def __figure_default(self):
        return Figure(figsize=(12,10))
    
    def traits_view(self):    
        view = View(
            Item('_figure',
                show_label=False,
                editor=MatplotlibFigureEditor(
                    toolbar=True,
                    toolbar_above=False,
                ),
            ),
            HGroup(
                'bins',
                'data',
                'sum_species',
                'from_timepoint_index',
            ),
            width=800, height=600,
            resizable=True,
            title='TODO',#self.window_title
            id='Histograms',
        )
        return view


def test():
#    results = McssResults('../../../examples/mcss/models/module1.h5')
    Histograms.fromfile('../../../examples/mcss/models/module1.h5').configure_traits()

if __name__ == '__main__':
    test()    