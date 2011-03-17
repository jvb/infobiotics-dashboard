import unittest2 as unittest

import numpy as np
from numpy.testing import assert_array_almost_equal

from mcss_postprocess import mcss_postprocess

from infobiotics.mcss.results.mcss_results import McssResults
import infobiotics.mcss.results.mcss_results as mcss_results

class TestMcssResults(unittest.TestCase):

#    def test(self):
#        pass

    def setUp(self):        
        self.results = McssResults('NAR_simulation.h5')
        self.assertEqual(len(self.results.species_indices), 4)
        self.assertEqual(len(self.results.run_indices), 200)
        self.assertEqual(len(self.results.compartment_indices), 1)
        self.assertEqual(len(self.results._timepoints), 601)
#        self.results.amounts()
#        self.results.amounts(quantities_display_type='concentrations')
#        print self.results.amounts(quantities_display_type='concentrations',
#                                   quantities_display_units='attomolar',
#                                   volume=1)

    def _test_concentrations(self):
        file_name = 'germination_09.h5'
        results = McssResults(file_name)
        
        # germination_09.h5 seems to have quantities in *moles and volumes in litres 
#        results.volumes_data_units = 'microlitres' # breaks it
        results.quantities_data_units = 'micromoles'
        amounts = results.amounts(
            quantities_display_type='concentrations',
            quantities_display_units='micromolar'
        )
        
        # concentration of SIG1 in compartment 27 [0,28] of run 1
        assert_array_almost_equal(
            mcss_postprocess('-l -x -C 27 -t 1 -s SIG1', file_name)[2][0],
            amounts[0, 27, 27].magnitude,
            verbose=True
        )

        # concentration of all species in all compartments of run 1 

        # concentrations
        m = mcss_postprocess('-l -x -t 1', file_name)[2]
        
        # molecules
#        m = mcss_postprocess('-l -t 1', file_name)[2]
#        results.quantities_data_units = 'molecules'
#        amounts = results.amounts(
#            quantities_display_type='molecules',
#            quantities_display_units='molecules'
#        )
        
#        # mcss-postprocess prints all compartments sorted by x,y coordinate 
#        # *not* index
#
#        # in germination_09.h5 [0,0] has index 1 and [0,1] has index 0
#        # also [0,25] has index 38
#
#        # swap data for compartments with indices 0 and 1
#        m0 = np.copy(m[40 * 0:40 * 1])
#        m1 = np.copy(m[40 * 1:40 * 2])
#        m[40 * 0:40 * 1] = m1
#        m[40 * 1:40 * 2] = m0
#
#        # move data for compartment with index 38 at position 25 to 38 and 
#        # everything else down to 25
#        m25 = np.copy(m[40 * 25:40 * 26])
#        m26to38 = np.copy(m[40 * 26:])#40 * 39)
#        m[40 * 25:40 * 38] = m26to38 
#        m[40 * 38:40 * 39] = m25 
#
        m = fix_mcss_postprocess_germination_09_h5_output(m, 40)

        ri = 0
#        si = 1
#        ci = 25
#        assert_array_almost_equal(m[(40 * ci) + si], amounts[ri, si, ci].magnitude)
##        for i in range(len(m[(40 * ci) + si])):
##            print m[(40 * ci) + si][i] - amounts[ri, si, ci][i].magnitude
##        exit()

        for ci in range(39):
            for si in range(40):
#                print si, ci
                assert_array_almost_equal(
                    amounts[ri, si, ci].magnitude,
                    m[(40 * ci) + si],
                    verbose=True
                )
            
    def _test_functions_of_concentrations(self):
        functions = (
            mcss_results.mean,
            mcss_results.std,
        )
        file_name = 'germination_09.h5'
        results = McssResults(file_name)
        results.quantities_data_units = 'micromoles'
        f = self.results.get_functions_over_runs(
            functions,
#            quantities_display_type='concentrations',
#            quantities_display_units='micromolar',
#            volume=1
        )
        
        
        
#        # compare mean and std of each species in only compartment of all runs at each timepoint
#        for i in range(0, 4):
#            # mean
#            assert_array_almost_equal(
#                mcss_postprocess('-l')[2][i * 3], # 2 is outputs, 0 is 1st output array
#                f[0, i, 0, :].magnitude,
#                verbose=True
#            )
#            # std
#            assert_array_almost_equal(
#                mcss_postprocess('-l')[2][i * 3 + 1], # 2 is outputs, 0 is 1st output array
#                f[1, i, 0, :].magnitude,
#                verbose=True
#            )        
            
    def _test_McssResults_get_functions_over_runs(self):
        
#        print self.results.amounts().shape
#        print np.mean(self.results.amounts(), axis=0)

        functions = (
            mcss_results.mean,
            mcss_results.std,
        )
        f = self.results.get_functions_over_runs(functions)
        
        m = mcss_postprocess('-l')[2]
        
        # compare mean and std of each species in only compartment of all runs at each timepoint
        
        for i in range(0, 4):
            # mean
            assert_array_almost_equal(
                m[i * 3], # 2 is outputs, 0 is 1st output array
                f[0, i, 0, :].magnitude,
                verbose=True
            )
            # std
            assert_array_almost_equal(
                m[i * 3 + 1], # 2 is outputs, 0 is 1st output array
                f[1, i, 0, :].magnitude,
                verbose=True
            )        
    
    def _test_McssResults(self):
        amounts = self.results.amounts()
        self.assertEqual(amounts.shape, (200, 4, 1, 601))

        # sum of all species in only compartment of run 1 at each timepoint
        assert_array_almost_equal(
            mcss_postprocess('-a -l -S 0,1,2,3 -t 1')[2][0], # 2 is outputs, 0 is 1st output array
            np.sum(np.sum(amounts[0], 1), 0).magnitude,
        )        
#        # as above but for all runs individually # takes a while
#        for r in results.run_indices:
#            assert_array_almost_equal(
#                mcss_postprocess('-a -l -S 0,1,2,3 -t %s' % (r + 1))[2][0], # 2 is outputs, 0 is 1st output array
#                np.sum(np.sum(amounts[r], 1), 0).magnitude,
#            )    


    def _test_functions_of_values_over_axis_sum(self):
        amounts = self.results.amounts()

        #TODO move amounts_axes from McssResults to mcss_results?
#        array_axes = McssResults.amounts_axes # ('runs', 'species', 'compartments', 'timepoints')
        array_axes = ('runs', 'species', 'compartments', 'timepoints')

        # as above using functions_of_values_over_axis with sum function
        functions = (
            lambda array, axis: np.sum(array, axis),
        )
        f = mcss_results.functions_of_values_over_axis(amounts, array_axes, 'species', functions)
        assert_array_almost_equal(
            mcss_postprocess('-a -l -S 0,1,2,3 -t 1')[2][0], # 2 is outputs, 0 is 1st output array
            f[0, 0, 0, :].magnitude, #np.sum(np.sum(amounts[0], 1), 0)
            verbose=True
        )
        assert_array_almost_equal(
            np.sum(np.sum(amounts[0], 1), 0),
            f[0, 0, 0, :], #np.sum(np.sum(amounts[0], 1), 0)
            verbose=True
        )
        
    def _test_functions_of_values_over_axis_mean_and_std(self): #TODO extend to c_i
        amounts = self.results.amounts()

        # mean and std
        functions = (
            mcss_results.mean,
            mcss_results.std,
        )
        array_axes = ('runs', 'species', 'compartments', 'timepoints')
        f = mcss_results.functions_of_values_over_axis(amounts, array_axes, 'runs', functions)
        # compare mean of 1st species in only compartment of all runs at each timepoint
        self.assertTrue(
            np.array_equal(
                mcss_postprocess('-l')[2][0], # 2 is outputs, 0 is 1st output array
                f[0, 0, 0, :],
            ),
        )
        # compare std of 1st species in only compartment of all runs at each timepoint
        assert_array_almost_equal(
            mcss_postprocess('-l')[2][1], # 2 is outputs, 0 is 1st output array
            f[1, 0, 0, :].magnitude,
            verbose=True
        )
        # compare mean and std of each species in only compartment of all runs at each timepoint
        for i in range(0, 4):
            # mean
            assert_array_almost_equal(
                mcss_postprocess('-l')[2][i * 3], # 2 is outputs, 0 is 1st output array
                f[0, i, 0, :].magnitude,
                verbose=True
            )
            # std
            assert_array_almost_equal(
                mcss_postprocess('-l')[2][i * 3 + 1], # 2 is outputs, 0 is 1st output array
                f[1, i, 0, :].magnitude,
                verbose=True
            )
        

#    def test_functions_of_values_over_axis(self):
#        from mcss_results import functions_of_values_over_axis
#        import numpy as np
#        array = np.zeros((1, 2, 3, 4))
#        array_axes = ('runs', 'species', 'compartments', 'timepoints')
#        axis = 'runs'
#        functions = (
#            lambda array, axis: np.mean(array, axis),
#            lambda array, axis: np.std(array, axis, ddof=1)
#        )
#        self.assertEqual(
#            functions_of_values_over_axis(
#                array,
#                array_axes,
#                axis,
#                functions
#            ).shape,
#            (2, 2, 3, 4)
#        )
##        def functions_of_values_over_axis_shape(array=array, array_axes=array_axes, axis=axis, functions=functions):
##            return functions_of_values_over_axis(
##                array,
##                array_axes,
##                axis,
##                functions
##            ).shape
##        for i, axis in enumerate(array_axes):
##            self.assertEqual(
##                functions_of_values_over_axis_shape(axis=axis),
##                tuple([len(functions)] + [len(array) for j, ax in enumerate(array_axes) if not ax == axis]))#(2, 2, 3, 4))
#        from mcss_results import McssResults
#        array = McssResults('/home/jvb/phd/eclipse/infobiotics/dashboard/examples/infobiotics-examples-20110208/quickstart-NAR/NAR_simulation.h5').amounts()
#
#    def test_functions_of_values_over_axis_generator(self):
#        from mcss_results import functions_of_values_over_axis_generator
#
#    def test_functions_of_values_over_successive_axes(self):
#        from mcss_results import functions_of_values_over_successive_axes
#
#    def test_McssResults_allocate_array(self):
#        pass
#
#    def test_McssResults_timepoints(self):
#        pass
#

    def test_McssResults_volumes(self):
        results = McssResults('germination_09.h5') 
        
        # one run
        volumes = results.volumes()
        m = mcss_postprocess('-w -t1', 'germination_09.h5')[2]
        
        m = fix_mcss_postprocess_germination_09_h5_output(m, 1)
        
        assert_array_almost_equal(
            m,
            volumes[0].magnitude,
            verbose=True
        )

        # mean of all runs
        functions = (mcss_results.mean, mcss_results.std)
        volumes = mcss_results.functions_of_values_over_axis(volumes, ('runs', 'compartments', 'timepoints'), 'runs', functions)
        m = mcss_postprocess('-w', 'germination_09.h5')[2]
        m = fix_mcss_postprocess_germination_09_h5_output(m, 3)
        assert_array_almost_equal(
            volumes[0].magnitude,
            m[::3],
            verbose=True
        )
        assert_array_almost_equal(
            volumes[1].magnitude,
            m[1::3],
            verbose=True
        )


def fix_mcss_postprocess_germination_09_h5_output(m, step=1):
    # mcss-postprocess prints all compartments sorted by x,y coordinate 
    # *not* index

    # in germination_09.h5 [0,0] has index 1 and [0,1] has index 0
    # also [0,25] has index 38

    # swap data for compartments with indices 0 and 1
    m0 = np.copy(m[step * 0:step * 1])
    m1 = np.copy(m[step * 1:step * 2])
    m[step * 0:step * 1] = m1
    m[step * 1:step * 2] = m0

    # move data for compartment with index 38 at position 25 to 38 and 
    # everything else down to 25
    m25 = np.copy(m[step * 25:step * 26])
    m26to38 = np.copy(m[step * 26:])#step * 39)
    m[step * 25:step * 38] = m26to38 
    m[step * 38:step * 39] = m25         
    
    return m



#    def test_McssResults_amounts(self):
#        pass
#
#    def test_McssResults_get_surfaces(self):
#        pass
    

if __name__ == '__main__':
    unittest.main()
