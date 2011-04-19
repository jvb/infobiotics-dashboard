#!/usr/bin/env python

# http://www.py2exe.org/index.cgi/MatPlotLib
import matplotlib
matplotlib.use('qt4agg') # overrule configuration
import pylab #TODO remove?

import infobiotics.dashboard.run as run
run.main()
