import subprocess
import numpy as np

def mcss_postprocess(args, file_name='NAR_simulation.h5'):
    p = subprocess.Popen(['mcss-postprocess'] + args.split() + [file_name], stdout=subprocess.PIPE)
    for i, line in enumerate(p.stdout):
        if i == 0:
            header = line.strip().split()
            timepoints = []
            output = [[] for _ in range(len(header) - 1)]
        else:
            for j, o in enumerate(line.strip().split()):
                if j == 0:
                    timepoints.append(o)
                else:
                    output[j - 1].append(float(o))
    #print header
    #print timepoints
    #for o in output:
    #    print o
    return header, np.array(timepoints), np.array(output)

#print mcss_postprocess('-a -l -S 0,1,2,3 -t 1')
