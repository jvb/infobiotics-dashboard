from infobiotics.shared.api import \
    ExperimentHandler, ExperimentView, Item, Instance, HasTraits, Property
from infobiotics.mcss.api import McssExperiment, McssProgressHandler

class McssExperimentHandler(ExperimentHandler):

    _progress_handler = McssProgressHandler()

    experiment = McssExperiment()

    traits_view = ExperimentView(
        Item('_cwd', label='Working directory', tooltip='Relative paths will be relative to this directory.'),
    )
    
    
if __name__ == '__main__':
    handler = McssExperimentHandler()
    print handler._progress_handler
    print handler.experiment
    print handler.experiment.parameters