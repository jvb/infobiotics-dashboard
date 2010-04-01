class MC2ExperimentHandler(PModelCheckerExperimentHandler):

    _progress_handler = MC2ExperimentProgressHandler 

    traits_view = ExperimentView(
        Item('_cwd', label='Working directory', tooltip='Relative paths will be relative to this directory.'),
    )
