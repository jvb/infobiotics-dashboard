#!/usr/bin/env python

import infobiotics
import mcss_results  
from PyQt4 import QtGui
import numpy as np
import matplotlib.pyplot as plt

results = mcss_results.McssResults('tests/NAR_simulation.h5')

amounts = results.amounts()

timepoints = results.timepoints
step = len(timepoints) // 20

plt.figure()

colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
for ci in results.compartment_indices:
    for i, si in enumerate(results.species_indices):
        mean = mcss_results.mean(amounts[:, si, ci, :], 0)
        std = mcss_results.std(amounts[:, si, ci, :], 0)
        plt.plot(timepoints, mean, color=colors[i])
        plt.errorbar(timepoints[::step], mean[::step], yerr=std[::step], linestyle='None', color=colors[i])

plt.show()
QtGui.qApp.exec_()
