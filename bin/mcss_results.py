'''
#!/bin/bash
python ../infobiotics/dashboard/plugins/simulator_results/simulator_results $*
'''
from infobiotics.dashboard.plugins.simulator_results.simulator_results import SimulationResultsDialog, main, centre_window
app, argv = main.begin_traits()
if len(argv) > 2:
    print "usage: mcss_results.sh {h5file}"
    main.end(1)
if len(argv) == 1:
    w = SimulationResultsDialog()
elif len(argv) == 2:
    w = SimulationResultsDialog(filename=argv[1])
centre_window(w)
w.show()
main.end_with_qt_event_loop()
    