from infobiotics.mcss.results.mcss_results_widget import McssResultsWidget, main, centre_window
app, argv = main.begin_traits()
if len(argv) > 2:
    print "usage: mcss_results.sh {h5file}"
    main.end(1)
if len(argv) == 1:
    w = McssResultsWidget()
elif len(argv) == 2:
    w = McssResultsWidget(filename=argv[1])
centre_window(w)
w.show()
main.end_with_qt_event_loop()
    
