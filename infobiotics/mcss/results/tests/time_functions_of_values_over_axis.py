import infobiotics.mcss.results.mcss_results as mcss_results
results = mcss_results.McssResults('NAR_simulation.h5')
for i in range(10):
    mcss_results.functions_of_values_over_axis(results.amounts(), ('runs', 'species', 'compartments', 'timepoints'), 'runs', (mcss_results.mean, mcss_results.std))
#    results.get_functions_over_runs((mcss_results.mean, mcss_results.std))

#from numpy.testing import assert_array_almost_equal
#assert_array_almost_equal(
#    mcss_results.functions_of_values_over_axis(results.amounts(), ('runs', 'species', 'compartments', 'timepoints'), 'runs', (mcss_results.mean, mcss_results.std)),
#    results.get_functions_over_runs((mcss_results.mean, mcss_results.std))
#)

