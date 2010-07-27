from enthought.traits.api import HasTraits, Instance, Str, Button 
from enthought.traits.ui.api import View, VGroup, HGroup, Item, Spring, HSplit, CodeEditor
from matplotlib.figure import Figure
from infobiotics.commons.traits.ui.qt4.matplotlib_figure_editor import MPLFigureEditor
from infobiotics.commons.matplotlib_ import MatplotlibFigureSize, resize_and_save_matplotlib_figure

class POptimizerResults(HasTraits):
    figure = Instance(Figure, ())
    title = Str
    best_model = Str
    experiment = Instance('POptimizerExperiment')
    
    def traits_view(self):
        return View(
            HSplit(
                VGroup(
                    HGroup(
                        Item(label='Best model found:'),
                        Spring(),
                        Item('experiment', show_label=False),
                        Spring(),
                        Item('save_resized', show_label=False),
                    ),
                    Item('best_model', 
                        show_label=False, 
                        style='custom', 
                        editor=CodeEditor(show_line_numbers=False)),
                ),
                Item('figure',
                    show_label=False,
                    editor=MPLFigureEditor(
#                            toolbar=True
                    ),
                ),
                show_border=True,
            ),
            resizable=True,
            scrollable=True,
            title=self.title,
            id='POptimizerResults',
        )
        
    save_resized = Button
    def _save_resized_fired(self):
        resize_and_save_matplotlib_figure(self.figure)

    def _experiment_changed(self):
        if self.experiment is None:
            return
        try:    
            import os
            params_file = os.path.split(self.experiment._params_file)[1]
            self.title = params_file
            
            with open('bestPsystem_Run0.txt') as f:
                best_model = f.read() 
            
            self.best_model=best_model

            target_file = self.experiment.target_file
        
            import numpy as np
            target = np.loadtxt(target_file, skiprows=1)
            f = open(target_file)
            species = f.readline().split()[1:]
            f.close()
            time = target[:,0] # x_axis
            
            output = np.loadtxt('outputdata.txt', skiprows=1, usecols=range(1, 3 * len(species), 3))
        
            
            fig = self.figure
            ax = fig.add_subplot(111)
            ax.set_title(params_file)
            ax.set_xlabel('time')
            ax.set_ylabel('molecules')
            ax.grid(True)
            
            for i in range(len(species)):
                ax.plot(time, target[:,i+1], label='%s (target)' % species[i])
                ax.plot(time, output[:,i], label='%s (optimised)' % species[i])    
        
            ax.legend(loc='best')
            
        except Exception, e:
            print e
            

if __name__ == '__main__':
    from infobiotics.poptimizer.poptimizer_experiment import POptimizerExperiment
    experiment = POptimizerExperiment('../../../examples/NAR-poptimizer/NAR_optimization.params')
    POptimizerResults(experiment=experiment).configure_traits()
