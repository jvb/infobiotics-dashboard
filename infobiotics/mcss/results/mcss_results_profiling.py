from __future__ import division
import numpy as np
import tables

class MockMcssResults():

    def _allocate_array(self, shape, failed_message):
        '''
        >>> million = 1000 * 1000
        >>> results = _allocate_array(million, million, million), 'Should raise a MemoryError')
        '''
        print 'allocating', shape, 'array (%s datapoints)' % np.prod(shape), '...',
        try:
            array = np.zeros(shape, np.float64)
        except MemoryError, e:
            print 'failed'
            exit('failed')
#            raise e
        print 'succeeded'
        return array

    def amounts(self):
        results = self._allocate_array(
            (
                len(self.run_indices),
                len(self.species_indices),
                len(self.compartment_indices),
                len(self.timepoints)
            ),
            'Could not allocate memory for amounts.\n' \
            'Try selecting fewer runs, a shorter time window or a bigger time interval multipler.'
        )
        if results is None:
            return
        h5 = tables.openFile(self.filename)


#        self.test_io(h5)
#        self.test_io_loop(h5)
#        h5.close()
#        return
##        np.testing.assert_equal(np.array([1,2]), np.array([2,3]))
        results = self._extract_amounts_new(h5, results, self.start, self.stop)
#        new = self._extract_amounts_new(h5, results, self.start, self.stop)
#        cur = self._extract_amounts(h5, results, self.start, self.stop)
#        np.testing.assert_equal(new, cur)
#        results = cur
        
        h5.close()
        return results

#    @profile # 73.7609 s
    def _extract_amounts(self, h5, destination_array, start, stop):
        for ri, r in enumerate(self.run_indices):
            parent_run = '/run%s' % (r + 1)
            amounts = h5.getNode(parent_run, 'amounts')
            amounts_shape = amounts.shape
            print 'amounts', amounts_shape, 'array (%s datapoints)' % np.prod(amounts_shape)

#            # naive
#            # some timepoints for each run for each species for each compartment                     
#            for si, s in enumerate(self.species_indices):
#                for ci, c in enumerate(self.compartment_indices):
#                    print 'run %s/%s, species %s/%s, compartment %s/%s' % (r + 1, len(self.run_indices), s + 1, len(self.species_indices), c + 1, len(self.compartment_indices)) 
#                    destination_array[ri, si, ci, :] = amounts[s, c, start:stop:self.step]
#            # est. 16 h!


            # pre-extract some timepoints of all species and all compartments
            slice_shape = (amounts_shape[0], amounts_shape[1], len(xrange(start, stop, self.step)))
            print 'slicing', slice_shape, 'array (%s datapoints)' % np.prod(slice_shape)
#            slice_size = np.prod(slice_shape)
#            if slice_size > 1000000: 
#                print 'aborted'
#                exit('aborted')
            slice = amounts[:, :, start:stop:self.step]
            assert slice_shape == slice.shape

            # current
            for si, s in enumerate(self.species_indices):
                for ci, c in enumerate(self.compartment_indices):
#                    print 'run %s/%s, species %s/%s, compartment %s/%s' % (r + 1, len(self.run_indices), s + 1, len(self.species_indices), c + 1, len(self.compartment_indices)) 
                    destination_array[ri, si, ci, :] = slice[s, c, :]
            # 73.536 s

#            # current with swapped species and compartments for loops
#            for ci, c in enumerate(self.compartment_indices):
#                for si, s in enumerate(self.species_indices):
##                    print 'run %s/%s, species %s/%s, compartment %s/%s' % (r + 1, len(self.run_indices), s + 1, len(self.species_indices), c + 1, len(self.compartment_indices)) 
#                    destination_array[ri, si, ci, :] = slice[s, c, :]
#            # 73.7609 s
            
#            #TODO direct with boolean array

        return destination_array
            
    
    
#    @profile # 73.0053 s
    def _extract_amounts_new(self, h5, destination_array, start, stop):
        species_and_compartments_index_array = np.array([self.species_indices, self.compartment_indices])
        timepoints_slice = slice(start, stop, self.step)
        for ri, r in enumerate(self.run_indices):
            parent_run = '/run%s' % (r + 1)
            amounts = h5.getNode(parent_run, 'amounts')
            amounts_shape = amounts.shape
            print 'amounts', amounts_shape, 'array (%s datapoints)' % np.prod(amounts_shape)
            
#            # direct with index array
#            destination_array[ri] = amounts[np.array([self.species_indices, self.compartment_indices, xrange(start, stop, self.step)])]
#            # reformatted
##            destination_array[ri] = amounts[np.array([
##                self.species_indices, 
##                self.compartment_indices, 
##                xrange(start, stop, self.step) # timepoints
##            ])]

#            destination_array[ri] = amounts[species_and_compartments_index_array, start:stop:self.step]
            destination_array[ri] = amounts[species_and_compartments_index_array, timepoints_slice]
        
        return destination_array


#    @profile
    def test_io(self, h5):
        h5.getNode('/run1', 'amounts')[1,1,1]
        
#    @profile
    def test_io_loop(self, h5):
        for r in self.run_indices:
            h5.getNode('/run%s' % (r + 1), 'amounts')[1,1,1]


    
    def __init__(self, filename):
        self.filename = filename
#        self.run_indices = range(10)
#        self.species_indices = range(58)
#        self.compartment_indices = range(10000)
#        self.timepoints = range(36001)
#        self.start = 0
#        self.stop = 36001
#        self.step = 1

#print 'profiling 10 run, 58 species, 10000 compartment, 36001 timepoint model'

def test(runs, species, compartments, timepoints):
    results = MockMcssResults('/home/jvb/tmp/quorumsensing-wt-experiment01.h5')
#    #jvb@weasel ~/data/simulations $ h5dump -H -p quorumsensing-wt-experiment01.h5 | grep COMPRESSION | grep -v DEFLATE | cut -d ' ' -f 14-15
#    dumped_and_cutted = '''
#        134037100 (623.128:1
#        133998225 (623.309:1
#        134008786 (623.260:1
#        134112930 (622.776:1
#        134072249 (622.965:1
#        133998539 (623.308:1
#        134040052 (623.115:1
#        134106337 (622.807:1
#        134133986 (622.678:1
#        134045612 (623.089:1
#    '''
#    bytes = sum(int(d[0]) * float(d[1][1:8]) for d in [l.split() for l in dumped_and_cutted.strip().split('\n')])
#    kb = bytes / 1024
#    mb = kb / 1024
#    gb = mb / 1024
#    tb = gb / 1024
#    print tb, gb, mb, kb, bytes
#    exit()
    results.run_indices = xrange(runs)
    results.species_indices = xrange(species)
    results.compartment_indices = xrange(compartments)
    results.timepoints = xrange(timepoints)
    results.start = 0
    results.stop = timepoints
    results.step = 1
    return results.amounts()
    
test(10, 10, 10, 10)
