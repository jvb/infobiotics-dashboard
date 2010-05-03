
def timeseriesExample():
    '''
    
    '''
    from Traits import McssResults
    
#    McssResults().configure_traits()
    
    filename = ''
    results = McssResults(filename)

    species = []
    runs = []
    
    compartmentNameRegex = ''
    compartments = results.selectedCompartments(nameRegex=compartmentNameRegex)
    
    timeseries = results.timeseries(species, 
                                    compartments, 
                                    runs, 
                                    average_runs=True
                                    )
#    data = timeseries.data()
    data = results.data(species,
                        compartments,
                        runs,
                        format='csv')
    
    print data

