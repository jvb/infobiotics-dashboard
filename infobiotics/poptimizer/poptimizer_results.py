from __future__ import with_statement
import infobiotics
from enthought.traits.api import HasTraits, Instance, Str, Button, Any 
from enthought.traits.ui.api import View, VGroup, HGroup, Item, Spring, HSplit, CodeEditor
from matplotlib.figure import Figure
from infobiotics.commons.traits.ui.qt4.matplotlib_figure_editor import MatplotlibFigureEditor
from poptimizer_experiment import POptimizerExperiment

#import logging
#logger = logging.getLogger(__file__)
#logger.addHandler(logging.StreamHandler())
#logger.setLevel(logging.ERROR)
from infobiotics.commons.api import logging
logger = logging.getLogger(__name__)

class POptimizerResults(HasTraits):
    figure = Instance(Figure, ())
    title = Str
    best_model = Str
    experiment = Any#Instance(POptimizerExperiment)
    def _experiment_default(self):
        return None

    edit_experiment = Button
    def _edit_experiment_fired(self):
        self.experiment.edit()
    
    def traits_view(self):
        return View(
            HSplit(
                VGroup(
                    HGroup(
                        Item(label='Best model found:'),
                        Spring(),
                        Item('edit_experiment', show_label=False, enabled_when='object.experiment is not None'),
                    ),
                    Item('best_model',
                        show_label=False,
                        style='custom',
                        editor=CodeEditor(show_line_numbers=False)),
                ),
                Item('figure',
                    show_label=False,
                    editor=MatplotlibFigureEditor(),
                ),
                show_border=True,
            ),
            resizable=True,
            scrollable=True,
            title=self.title,
            id='POptimizerResults',
        )
        
    def _experiment_changed(self):
        if self.experiment is None:
            return
        try:    
            import os.path
            params_file = os.path.split(self.experiment._params_file)[1]
            directory = self.experiment.directory_
            self.title = params_file
            
            with open(os.path.join(directory, 'bestPsystem_Run0.txt')) as f:
                best_model = f.read() 
            
            self.best_model = best_model

            target_file = os.path.join(directory, self.experiment.target_file) + '1.txt'
        
            f = open(target_file)
            species = f.readline().split()[1:]
            f.close()

            import numpy as np
            target = np.loadtxt(target_file, skiprows=1)
            time = target[:, 0] # x_axis
            
            output = np.loadtxt(os.path.join(directory, 'outputdata.txt'), skiprows=1, usecols=range(1, 3 * len(species), 3))
            
#            # combined plot
#            ax = self.figure.add_subplot(111)
#            ax.set_title(params_file)
#            ax.set_xlabel('time')
#            ax.set_ylabel('molecules')
#            ax.grid(True)
#            for i in range(len(species)):
#                ax.plot(time, target[:,i+1], label='%s (target)' % species[i])
#                ax.plot(time, output[:,i], label='%s (optimised)' % species[i])    
#            ax.legend(loc='best')

            # stacked plot
            rows = len(species)
            cols = 1
            for i in range(rows):
                if i == 0:
                    shax = self.figure.add_subplot(rows, cols, 1)
                    ax = shax
                    ax.set_title(params_file)
#                    shax.set_xlabel("time")
                else:
                    ax = self.figure.add_subplot(rows, cols, i + 1, sharex=shax)                
                if i == (rows - 1):
                    ax.set_xlabel("time")
                ax.grid(True)
                ax.set_ylabel('molecules')
                ax.plot(time, target[:, i + 1], label='%s (target)' % species[i])
                ax.plot(time, output[:, i], label='%s (optimised)' % species[i])    
                ax.legend(loc='best')
            
        except Exception, e:
            logger.error(e)
            

if __name__ == '__main__':
    experiment = POptimizerExperiment('../../examples/poptimizer/fourinitial/four_initial_inputpara.params')
    POptimizerResults(experiment=experiment).configure_traits()
