import numpy as np
def npz_info(files):
    for file_name in files:
        f = np.load(file_name)
        
        model_file_name = f['model_file_name']
        data_file_name = f['data_file_name']
        run_indices = f['run_indices']
        run_numbers = f['run_numbers']
        species_indices = f['species_indices']
        species_names = f['species_names']
        compartment_indices = f['compartment_indices']
        compartment_labels_and_positions = f['compartment_labels_and_positions']
        timepoints = f['timepoints']
        shape = f['shape']
            
        if 'levels' in f.files:
            levels_string = 'levels'
        else:
            levels_string = 'means'
        levels = f[levels_string]
    
        print
        summary = ', '.join([str(s) + ' ' + shape[i] + ('s' if not shape[i].endswith('s') else '') for i, s in enumerate(levels.shape)])
        print "%s: %s from simulation '%s' of model '%s'" % (file_name, summary, data_file_name, model_file_name) 
        print
        print '%s species (index, name, original index)' % (len(species_indices),)
        print '\n'.join(['\t'.join((str(i), s, str(species_indices[i]))) for i, s in enumerate(species_names)])
        print
        print '%s compartments (index, label and position, original index)' % (len(compartment_indices),)
        print '\n'.join(['\t'.join((str(i), c, str(compartment_indices[i]))) for i, c in enumerate(compartment_labels_and_positions)])
        print
        print '%s timepoints from %s to %s every %s' % (len(timepoints), timepoints[0], timepoints[-1], (timepoints[1] - timepoints[0]))
        print
        if len(run_indices) == 1:
            print '1 run (run number %s)' % run_numbers[0]  
        else:
            if levels_string == 'levels':
                print '%s runs' % len(run_indices) + ' (index, run number)'
                print '\n'.join(['\t'.join((str(i), r)) for i, r in enumerate(run_numbers)])
            else:
                print '%s runs used to calculate mean (%s)' % (len(run_indices), ','.join(run_numbers))
        print    
        print "'%s.npy' is a %s-dimensional array of shape %s=(%s)" % (levels_string, len(shape), levels.shape, ', '.join(shape))
        print
        if levels_string == 'levels':
            if len(run_indices) == 1:
                example_function = '''# example function
def get_timeseries(species_index, compartment_index):
    import numpy as np
    f = np.load('%s')
    return f['%s'][0, species_index, compartment_index, :]
''' % (file_name, levels_string)
            else:
                example_function = '''# example function
def get_timeseries(run_index, species_index, compartment_index):
    import numpy as np
    f = np.load('%s')
    return f['%s'][run_index, species_index, compartment_index, :]
''' % (file_name, levels_string)
        else:
            example_function = '''# example function
def get_timeseries(species_index, compartment_index):
    import numpy as np
    f = np.load('%s')
    f['%s'][species_index, compartment_index, :]
''' % (file_name, levels_string)
        print example_function


if __name__ == '__main__':
    import sys, os.path
#    sys.argv.insert(1, 'levels.npz')
    sys.argv.insert(1, 'levels.npz')
    if len(sys.argv) < 2:
        print 'Usage: python %s file.npz [another.npz]' % os.path.basename(sys.argv[0])
        sys.exit(2)
#    from infobiotics.dashboard.plugins.simulator_results.npz_info import npz_info
    npz_info(sys.argv[1:])
