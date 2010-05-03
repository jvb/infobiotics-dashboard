import time
import sys


class FlushFile(object):
    """Write-only flushing wrapper for file-type objects."""
    def __init__(self, f):
        self.f = f
    def write(self, x):
        self.f.write(x)
        self.f.flush()

# Replace stdout with an automatically flushing version
#sys.stdout = FlushFile(sys.__stdout__)


lines = [
'initialization',
'0 3729.08 Plac(X=LacI) PluxR(X=FP) PR(X=LuxR) PR(X=LacI)',
'1 3729.08 Plac(X=LacI) PluxR(X=FP) PR(X=LuxR) PR(X=LacI),'
'2 3723.83 PR(X=LacI) Plac(X=LuxR) PluxR(X=LuxR) Plac(X=FP)',
'3 3632.36 PR(X=LacI) Plac(X=LuxR) PluxR(X=LacI) PluxR(X=LuxR) Plac(X=FP)',
'4 3632.36 PR(X=LacI) Plac(X=LuxR) PluxR(X=LacI) PluxR(X=LuxR) Plac(X=FP)',
'5 3476.43 PR(X=LacI) Plac(X=LuxR) PluxR(X=LacI) PluxR(X=LuxR) Plac(X=FP)',
'6 3360.36 PR(X=LacI) PluxR(X=LacI) Plac(X=FP)',
'7 3360.36 PR(X=LacI) PluxR(X=LacI) Plac(X=FP)',
'8 3360.36 PR(X=LacI) PluxR(X=LacI) Plac(X=FP)',
'9 3360.36 PR(X=LacI) PluxR(X=LacI) Plac(X=FP)',
'simulatefinalmodel',          
]

#if __name__ == '__main__':
#    print '__main__'

for i in range(0, len(lines)):
    time.sleep(1)
    print lines[i]
#    sys.stdout.flush()