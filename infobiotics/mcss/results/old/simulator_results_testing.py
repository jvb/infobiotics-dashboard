#def test():
##    w = SimulationResultsDialog(filename='/home/jvb/dashboard/examples/NAR-poptimizer/NAR_output.h5')
##    w = SimulationResultsDialog(filename='/home/jvb/phd/eclipse/infobiotics/dashboard/tests/NAR-ok/simulation.h5')
#    w = SimulationResultsDialog(filename='/home/jvb/dashboard/examples/autoregulation/autoregulation_simulation.h5')
#
#    if w.loaded:
##        w.ui.species_list_widget.selectAll()
##        w.ui.species_list_widget.setCurrentItem(w.ui.species_list_widget.findItems("proteinGFP", Qt.MatchExactly)[0])
##        for item in w.ui.species_list_widget.findItems("protein1*", Qt.MatchWildcard): item.setSelected(True)
#
##        w.ui.compartments_list_widget.selectAll()
##        w.ui.compartments_list_widget.setCurrentItem(w.ui.compartments_list_widget.item(0))
#
##        w.ui.runs_list_widget.setCurrentItem(w.ui.runs_list_widget.item(0))
#
#        for widget in (w.ui.species_list_widget, w.ui.compartments_list_widget, w.ui.runs_list_widget):
#            widget.item(0).setSelected(True)
#            widget.item(widget.count() - 1).setSelected(True)
#
#        w.ui.average_over_selected_runs_check_box.setChecked(False)
#
####        w.ui.visualise_population_button.click()
#
###        w.plot()
###        w.plotsPreviewDialog.ui.plotsListWidget.selectAll() #TODO rename
###        w.plotsPreviewDialog.combine()
#
##        w.export_data_as('test.csv')    # write_csv
##        w.export_data_as('test.txt')   # write_csv
##        w.export_data_as('test', open_after_save=False)        # write_csv
##        w.export_data_as('test.xls')    # write_xls
#        w.export_data_as('test.npz')    # write_npz
#
##    centre_window(w)
##    w.show()
#
#
#def test_SimulatorResults_export_data_as():
##    w = SimulationResultsDialog(filename='/home/jvb/dashboard/examples/modules/module1.h5')
#    w = SimulationResultsDialog(filename='/home/jvb/dashboard/examples/autoregulation/autoregulation_simulation.h5')
#    for widget in (w.ui.species_list_widget, w.ui.compartments_list_widget, w.ui.runs_list_widget):
#        widget.item(0).setSelected(True)
#        widget.item(widget.count() - 1).setSelected(True)
#    w.ui.average_over_selected_runs_check_box.setChecked(False)
##    w.export_data_as('test.csv')    # write_csv
#    w.export_data_as('test.xls')    # write_xls
##    w.export_data_as('test.npz')    # write_npz
#
#
#def test_volumes():
#    w = main()
#    w.ui.runs_list_widget.select(0)
#    w.ui.species_list_widget.select(-1)
#    w.ui.species_list_widget.select(-2)
#    w.ui.compartments_list_widget.select(-1)
#    w.ui.compartments_list_widget.select(-2)
#    w.every = 100
#    p = w.plot()
##    p.ui.plotsListWidget.selectAll()
##    p.combine()
    

#def profile_SimulatorResults_get_amounts():
#    results = SimulatorResults(
#        '/home/jvb/dashboard/examples/germination_09.h5',
#        None,
#    )
#    get_amounts = profile(results.get_amounts)
#    amounts = get_amounts()
#    print amounts
#    exit()
