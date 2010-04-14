from infobiotics.mcss.api import McssParams, McssExperiment

if __name__ == '__main__':
    
#    parameters = McssParams()
#    parameters.configure_traits()
##    parameters.configure()
    
    experiment = McssExperiment()
#    experiment.configure_traits()
#    experiment.configure()
    if experiment.load('tests/mcss/models/module1.params.malformed'): experiment.configure()
