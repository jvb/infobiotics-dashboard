import subprocess
import numpy as np

def mcss_postprocess(args, file_name='../../../../examples/quickstart-NAR/NAR_simulation.h5'):
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

cidegree = 0.95
from math import sqrt
_, timepoints, run1 = mcss_postprocess('-l -S 1 -t 1')
run1 = run1[0]
run2 = mcss_postprocess('-l -S 1 -t 2')[2][0]
runs_std = mcss_postprocess('-l -S 1')[2][1]
runs_ppf = mcss_postprocess('-l -S 1')[2][2]
#print run1, run2, runs_std, runs_ppf
print run1.shape, run2.shape, runs_std.shape, runs_ppf.shape
#print stdtrit(runs)

num_runs = 2
#cifactor = gsl_cdf_tdist_Pinv(1.0 - (1.0 - cidegree) / 2.0, num_runs - 1) / sqrt(num_runs)
from infobiotics.mcss.results.statistics import InverseStudentT
cifactor_InverseStudentT = InverseStudentT(num_runs - 1, 1.0 - (1.0 - cidegree) / 2.0) / sqrt(num_runs)
from scipy.special import stdtrit
cifactor_stdrit = stdtrit(num_runs - 1, 1.0 - (1.0 - cidegree) / 2.0) / sqrt(num_runs)
#print cifactor_InverseStudentT - cifactor_stdrit 
ppf = (cifactor_InverseStudentT * runs_std)
#ppf = (cifactor_stdrit * runs_std)
print ppf - runs_ppf

