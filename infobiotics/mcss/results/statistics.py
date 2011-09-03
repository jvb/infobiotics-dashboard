from __future__ import division

def ci_factor(num_samples, ci_degree=0.95):
    assert 0 <= ci_degree <= 1
    import math
#    from scipy.special import stdtrit
#    return stdtrit(num_samples - 1, 1.0 - (1.0 - ci_degree) / 2.0) / math.sqrt(num_samples)
    from infobiotics.thirdparty.statistics import InverseStudentT
    return InverseStudentT(num_samples - 1, 1.0 - (1.0 - ci_degree) / 2.0) / math.sqrt(num_samples)
