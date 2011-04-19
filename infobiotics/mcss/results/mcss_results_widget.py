import sip
from infobiotics.mcss.results import mcss_results
from infobiotics.commons.quantities.units.time import time_units
sip.setapi('QString', 2)

from enthought.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'qt4'

from enthought.traits.api import HasTraits, Range, String
from enthought.traits.ui.api import View, VGroup, HGroup, Item
from infobiotics.mcss.results.spatial_plots import Surface, SpatialPlotsWindow

from PyQt4.QtCore import QSettings, QVariant, QDir, QFileInfo, SIGNAL, Qt
from PyQt4.QtGui import QWidget, QListWidgetItem, QItemSelectionModel, QFileDialog, QMessageBox

from infobiotics.commons import colours
from infobiotics.commons.qt4 import *#wait_cursor, disable_widgets, enable_widgets, hide_widgets, show_widgets, uncheck_widgets, clear_widgets, centre_window

from ui_mcss_results_widget import Ui_McssResultsWidget

from random import randint
import os

import xlwt

import numpy as np


from simulation import load_h5
from simulation_list_widget_item import SimulationListWidgetItem
from species import Species


from mcss_results import McssResults

# for QSettings
import infobiotics
import sys
from PyQt4.QtGui import qApp
# must use qApp not QApplication(sys.argv) when mixing with TraitsUI
if qApp is None:
    import sys
    from PyQt4.QtGui import QApplication
    app = QApplication(sys.argv) # must keep reference too
qApp.setOrganizationDomain('www.infobiotics.org')
qApp.setOrganizationName('Infobiotics')
qApp.setApplicationName('Infobiotics Dashboard')
qApp.setApplicationVersion(infobiotics.version)

class McssResultsWidget(QWidget):
    """Extract and plot data from mcss (version > 0.0.19) simulations"""

    def __init__(self, filename=None):
        """Setup widgets, connect signals to slots and attempt load."""
        self.settings_group = "McssResultsWidget"
        QWidget.__init__(self) # initialize base class

        self.ui = Ui_McssResultsWidget()
        self.ui.setupUi(self)

        self.ui.compartments_list_widget.setToolTip('')

        self.connect(self.ui.load_button, SIGNAL("clicked()"), self.load)

        self.ui.runs_list_widget.connect_all_selected_check_box(self.ui.select_all_runs_check_box)
        self.ui.species_list_widget.connect_all_selected_check_box(self.ui.select_all_species_check_box)
        self.ui.compartments_list_widget.connect_all_selected_check_box(self.ui.select_all_compartments_check_box)

        self.ui.species_list_widget.connect_filter_line_edit(self.ui.filter_species_line_edit)
        self.ui.compartments_list_widget.connect_filter_line_edit(self.ui.filter_compartments_line_edit)

        self.connect(self.ui.runs_list_widget, SIGNAL("itemSelectionChanged()"), self.update_ui)
        self.connect(self.ui.species_list_widget, SIGNAL("itemSelectionChanged()"), self.update_ui)
        self.connect(self.ui.compartments_list_widget, SIGNAL("itemSelectionChanged()"), self.update_ui)

        self.connect(self.ui.random_runs_spin_box, SIGNAL("valueChanged(int)"), self.select_random_runs)
        self.connect(self.ui.random_runs_spin_box, SIGNAL("valueChanged(int)"),
            lambda: (
                self.ui.select_all_runs_check_box.setChecked(False)
                    if self.ui.random_runs_spin_box.value() < self.ui.random_runs_spin_box.maximum()
                        else self.ui.select_all_runs_check_box.setChecked(True)
            )
        )

        # make sure from is always less than to and that to is always more than from
        self.connect(self.ui.from_spin_box, SIGNAL("valueChanged(double)"), self.ui.to_spin_box.set_minimum)
        self.connect(self.ui.to_spin_box, SIGNAL("valueChanged(double)"), self.ui.from_spin_box.set_maximum)

        self.quantities_display_type_changed(self.ui.quantities_display_type_combo_box.currentText())
        self.connect(self.ui.quantities_display_type_combo_box, SIGNAL('currentIndexChanged(QString)'), self.quantities_display_type_changed)

        self.connect(self.ui.calculate_button, SIGNAL('clicked()'), self.calculate)

        self.connect(self.ui.plot_histogram_button, SIGNAL("clicked()"), self.histogram)
        self.connect(self.ui.export_data_as_button, SIGNAL("clicked()"), self.export_data_as)
        self.connect(self.ui.plot_timeseries_button, SIGNAL("clicked()"), self.plot)
        self.connect(self.ui.visualise_population_button, SIGNAL("clicked()"), self.surfacePlot)

        self.load_settings()

        self.loaded = False # used by load to determine whether to fail silently and keep widgets enabled 
        self.loaded = self.load(filename)
        if not self.loaded:
            self.close()

        self.update_ui()

    def closeEvent(self, event):
#        shared.settings.save_window_size_and_position(self, self.settings_group)
        self.save_settings()
        event.accept()

    def load_settings(self):
        settings = QSettings()
        settings.beginGroup(self.settings_group)
        self.current_directory = unicode(settings.value('current_directory', QVariant(QDir.currentPath())).toString())
        #TODO load options and units
        settings.endGroup()

    def save_settings(self):
        settings = QSettings()
        settings.beginGroup(self.settings_group)
        settings.setValue("current_directory", QVariant(unicode(self.current_directory)))
        #TODO save options and units
        
#        # save filename specific options and units
#        settings.setValue(self.filename)
        
        settings.endGroup()

    def load(self, filename=None):
        
#        if getattr(self, 'filename', '') != '':
#            self.save_settings()
        
        if filename is None:
            filename = QFileDialog.getOpenFileName(self,
                                                   self.tr("Open HDF5 simulation data file"),
                                                   self.current_directory,
                                                   self.tr("HDF5 data files (*.h5 *.hdf5);;All files (*)"))
            if filename == '':
                if self.loaded:
                    return
                else:
                    self.load_failed()
                    return False

        self.current_directory = QFileInfo(filename).absolutePath()
#        filename = unicode(filename) # must convert QString into unicode
        simulation = None
        try:
            simulation = load_h5(filename)
        except IOError, e:
#            QMessageBox.warning(self, "Error", "There was an error reading %s\n%s" % (filename, e))
            if os.path.exists('mcss-error.log'):
                error_log = open("mcss-error.log", 'r')
                error_message = error_log.read()
                error_log.close()
                os.remove('mcss-error.log')
                QMessageBox.warning(self, "Error", "Unable to execute model:\n\n%s" % (error_message.replace('error: ', '', 1)))
            else:
                QMessageBox.warning(self, "Error", str(e).replace('`', ''))
        except AttributeError, e:
            e = e + "\nDid you use a old version of mcss (<0.0.19)?"
            QMessageBox.warning(self, "Error", str(e).replace('`', ''))
        if simulation == None:
            if self.loaded:
                return # continue with previously loaded file
            else:
                self.load_failed()
                return False

        self.simulation = simulation
        self.filename = filename

        self.load_succeeded()
        return True


    def load_failed(self):
        ''' Hides, clears, unchecks and disables relevant widgets. '''
        
        ui = self.ui

        hide_widgets(
            ui.runs_selected_and_total_label,
            ui.species_selected_and_total_label,
            ui.compartments_selected_and_total_label,
            
            ui.timepoints_data_units_combo_box,
            ui.timepoints_display_units_combo_box,
            
            ui._data_group_box,
#            ui.quantities_data_units_combo_box,
#            ui.quantities_display_type_combo_box,
##            ui.molecules_display_units_label,
#            ui.moles_display_units_combo_box,
#            ui.concentrations_display_units_combo_box,
            
#            ui.volumes_data_units_combo_box,
#            ui.volumes_display_units_combo_box,
            ui.volumes_widget,

#            ui._actions_layout, # not possible because QLayouts don't have a setVisible method
        )

        clear_widgets(
            ui.file_name_line_edit,
            ui.runs_list_widget,
            ui.species_list_widget,
            ui.compartments_list_widget,
        )

        uncheck_widgets(
            ui.select_all_runs_check_box,
            ui.select_all_species_check_box,
            ui.select_all_compartments_check_box,
        )
                
        disable_widgets(
            ui.file_name_line_edit,
            
            ui.select_all_runs_check_box,
            ui.runs_list_widget,
            ui.random_runs_spin_box,
            ui.random_runs_label,

            ui.select_all_species_check_box,
            ui.species_list_widget,
            ui.filter_species_line_edit,
#            ui.sort_species_check_box,
            
            ui.compartments_list_widget,
            ui.select_all_compartments_check_box,
            ui.filter_compartments_line_edit,
#            ui.sort_compartments_check_box,
            
            ui.to_spin_box,
            ui.from_spin_box,
            ui.every_spin_box,
            
            ui.average_over_selected_runs_check_box,
            ui.calculate_button,
            
            ui.export_data_as_button,
            ui.plot_timeseries_button,
            ui.plot_histogram_button,
            ui.visualise_population_button,
        )
        
        ui.load_button.setFocus(Qt.OtherFocusReason)


    def quantities_display_type_changed(self, text):
        if text == 'molecules': #FIXME replace with substance_display units?
            hide_widgets(self.ui.concentrations_display_units_combo_box, self.ui.moles_display_units_combo_box)
            show_widgets(self.ui.molecules_display_units_label)
        elif text == 'concentrations':
            hide_widgets(self.ui.molecules_display_units_label, self.ui.moles_display_units_combo_box)
            show_widgets(self.ui.concentrations_display_units_combo_box)
        elif text == 'moles':
            hide_widgets(self.ui.molecules_display_units_label, self.ui.concentrations_display_units_combo_box)
            show_widgets(self.ui.moles_display_units_combo_box)
        
        
    def load_succeeded(self):
        ''' Configures, populates, enables, checks and shows relevant widgets. '''

        simulation = self.simulation
        filename = self.filename
        ui = self.ui

        fileinfo = QFileInfo(filename)
        ui.file_name_line_edit.setText(fileinfo.absoluteFilePath())
        
        from_ = int(0)
        to = int(simulation.max_time)
        interval = simulation.log_interval
        
        ui.from_spin_box.setRange(from_, to)
        ui.from_spin_box.setValue(from_)
        ui.from_spin_box.set_interval(interval)

        ui.to_spin_box.setRange(from_, to)
        ui.to_spin_box.setValue(to)
        ui.to_spin_box.set_interval(interval)

        ui.every_spin_box.setRange(1, simulation._runs_list[0].number_of_timepoints)
        ui.every_spin_box.setValue(ui.every_spin_box.minimum())

        ui.log_interval_label.setText(str(interval))

        # list widgets
        clear_widgets(
            ui.runs_list_widget,
            ui.species_list_widget,
            ui.compartments_list_widget,
        )
        for i in simulation._runs_list:
#            print i, ui.runs_list_widget
            SimulationListWidgetItem(i, ui.runs_list_widget)
        for i in simulation._species_list:
            SimulationListWidgetItem(i, ui.species_list_widget)
        for i in simulation._runs_list[0]._compartments_list: #TODO can't rely on run1 alone if _compartments_list divide
            SimulationListWidgetItem(i, ui.compartments_list_widget)
        
        # runs
        runs = ui.runs_list_widget.count()
        ui.random_runs_spin_box.setRange(1, runs)
        if runs > 1:
            enable_widgets(
                ui.random_runs_spin_box,
                ui.random_runs_label,
                ui.average_over_selected_runs_check_box,
            )
        if runs == 1:
            ui.runs_list_widget.selectAll() # should check select_all_runs_check_box automatically
        else:
            enable_widgets(ui.select_all_runs_check_box)

        # species
        species = self.ui.species_list_widget.count()
        if species == 1:
            self.ui.species_list_widget.selectAll()
        else:
            enable_widgets(ui.select_all_species_check_box)


        # compartments
        compartments = self.ui.compartments_list_widget.count()
        if compartments == 1:
            self.ui.compartments_list_widget.selectAll()
        else:
            enable_widgets(ui.select_all_compartments_check_box)
        
        # timepoints
        # choosing some sensible defaults for 'every' to reduce initial number of data points
#        timepoints_data_units = self.ui.timepoints_data_units_combo_box.currentText() 
#        if timepoints_data_units in ('seconds', 'minutes') and to >= 300: # 5 minutes in seconds or 5 hours in minutes
#            self.ui.every_spin_box.setValue(60 // float(self.ui.log_interval_label.text()))
#        elif timepoints_data_units in ('hours') and to >= 168: # a week in hours -> days
#            self.ui.every_spin_box.setValue(24)
#        elif timepoints_data_units in ('days'):
#            if to < 30:
#                self.ui.every_spin_box.setValue(7)
#            elif 30 < to <= 365:
#                self.ui.every_spin_box.setValue(30)
##        else:
##            self.ui.every_spin_box.setValue(to // 100) 

        # volumes
#        i = self.ui.quantities_display_type_combo_box.findText('concentrations')
#        if i != -1:
#            self.ui.quantities_display_type_combo_box.removeItem(i)
        show_widgets(ui.volumes_widget)
        if self.simulation.log_volumes == 1:
#            self.ui.quantities_display_type_combo_box.insertItem(1, 'concentrations')
            self.volumes_list_widget_item = QListWidgetItem('Volumes', ui.species_list_widget)
#            show_widgets(ui.volumes_widget)
            hide_widgets(ui.volume_spin_box)
            show_widgets(ui.in_label)
        else:
#            hide_widgets(ui.volumes_widget)
            hide_widgets(ui.in_label)
            show_widgets(ui.volume_spin_box) #TODO switch on quantities_display_type_combo_box.currrentItem() == 'concentrations'  
        
#        check_widgets(
#            ui.select_all_runs_check_box,
#            ui.select_all_species_check_box,
#            ui.select_all_compartments_check_box,
#        )
                
        enable_widgets(
            ui.file_name_line_edit,
            
#            ui.select_all_runs_check_box,
            ui.runs_list_widget,
#            ui.random_runs_spin_box,
#            ui.random_runs_label,

            ui.select_all_species_check_box,
            ui.species_list_widget,
            ui.filter_species_line_edit,
#            ui.sort_species_check_box,
            
            ui.compartments_list_widget,
            ui.select_all_compartments_check_box,
            ui.filter_compartments_line_edit,
#            ui.sort_compartments_check_box,
            
            ui.to_spin_box,
            ui.from_spin_box,
            ui.every_spin_box,
            
#            ui.average_over_selected_runs_check_box,
#            ui.calculate_button,
            
#            ui.export_data_as_button,
#            ui.plot_timeseries_button,
#            ui.plot_histogram_button,
#            ui.visualise_population_button,
        )

        show_widgets(
            ui.runs_selected_and_total_label,
            ui.species_selected_and_total_label,
            ui.compartments_selected_and_total_label,
            
            ui.timepoints_data_units_combo_box,
            ui.timepoints_display_units_combo_box,
            
            ui.quantities_data_units_combo_box,
            ui.quantities_display_type_combo_box,
#            ui.molecules_display_units_label,
#            ui.moles_display_units_combo_box,
#            ui.concentrations_display_units_combo_box,
            
#            ui.volumes_data_units_combo_box,
#            ui.volumes_display_units_combo_box,
#            ui.volumes_widget,
        )

        self.ui.species_list_widget.setFocus(Qt.OtherFocusReason)


    def update_ui(self):
        ''' Called at the end of __init__ and whenever runs/species/compartments
        list_widget's item selection changes in order to disable/enable actions. '''
        
        num_selected_runs = len(self.ui.runs_list_widget.selectedItems())
        self.ui.runs_selected_and_total_label.setText('%s/%s' % (num_selected_runs, self.ui.runs_list_widget.count()))
        
        num_selected_species = len(self.ui.species_list_widget.selectedItems())
        self.ui.species_selected_and_total_label.setText('%s/%s' % (num_selected_species, self.ui.species_list_widget.count()))

        num_selected_compartments = len(self.ui.compartments_list_widget.selectedItems())
        self.ui.compartments_selected_and_total_label.setText('%s/%s' % (num_selected_compartments, self.ui.compartments_list_widget.count()))

        # enable/disable actions
        if num_selected_runs == 0 or num_selected_species == 0 or num_selected_compartments == 0:
            disable_widgets(
                self.ui.calculate_button,
                self.ui.export_data_as_button,
                self.ui.plot_timeseries_button,
                self.ui.visualise_population_button,
                self.ui.plot_histogram_button,
            )
        else:
            enable_widgets(
                self.ui.export_data_as_button,
                self.ui.plot_timeseries_button,
                self.ui.plot_histogram_button,
            )
#            if num_selected_runs == 1 and num_selected_species >= 1 and num_selected_compartments > 1:
            if num_selected_species >= 1 and num_selected_compartments > 1:
                enable_widgets(self.ui.visualise_population_button)
            else:
                disable_widgets(self.ui.visualise_population_button)
            if num_selected_runs > 1:
                enable_widgets(self.ui.calculate_button)


    # slots

    def select_random_runs(self, runs):
        list = self.ui.runs_list_widget
        list.clearSelection()
        randoms = set()
        while len(randoms) < runs:
            randoms.add(list.item(randint(0, list.count())))
        for i in randoms:
            list.setCurrentItem(i, QItemSelectionModel.Select)


    # accessors
    
    def selected_species(self):
        ''' Return selected species after removing volumes. '''
        selected_species = self.ui.species_list_widget.selectedItems()
        if self.simulation.log_volumes and self.volumes_list_widget_item in selected_species:
            selected_species.remove(self.volumes_list_widget_item)
            self.volumes_selected = True
        else:
            self.volumes_selected = False
        return selected_species
    
    # compound accessors

    def selected_items(self):
        ''' Usage: runs, species, compartments = selected_items() '''
        runs = self.ui.runs_list_widget.selectedItems()
        species = self.selected_species()
        compartments = self.ui.compartments_list_widget.selectedItems()
        return runs, species, compartments

    def selected_items_amount_indices(self):
        ''' Usage: run_indices, species_indices, compartment_indices = self.selected_items_amount_indices() 
            
        Use for ri, r in enumerate(run_indices): for selected results
         
        '''
        runs, species, compartments = self.selected_items()
        run_indices = [item.amounts_index for item in runs]
        species_indices = [item.amounts_index for item in species]
        compartment_indices = [item.amounts_index for item in compartments]
        return run_indices, species_indices, compartment_indices

    def options(self):
        ''' Usage: from_, to, every, averaging = self.options() '''
        from_ = self.ui.from_spin_box.value()
        to = self.ui.to_spin_box.value()
        every = self.ui.every_spin_box.value()
        averaging = self.ui.average_over_selected_runs_check_box.isChecked()
        return from_, to, every, averaging

    def volume(self):
        return self.ui.volume_spin_box.value()

    def units(self): 
        ''' Usage: timepoints_data_units, timepoints_display_units, 
        quantities_data_units, quantities_display_type, 
        quantities_display_units, volume, volumes_data_units, 
        volumes_display_units = self.units()
        #TODO return a dictionary rather than a tuple, then we can just do **units 
        
        '''
        timepoints_data_units = str(self.ui.timepoints_data_units_combo_box.currentText())
        timepoints_display_units = str(self.ui.timepoints_display_units_combo_box.currentText())
        quantities_data_units = str(self.ui.quantities_data_units_combo_box.currentText())
        quantities_display_type = str(self.ui.quantities_display_type_combo_box.currentText())
        if quantities_display_type == 'molecules':
            quantities_display_units = 'molecules'
        elif quantities_display_type == 'concentrations':
            quantities_display_units = str(self.ui.concentrations_display_units_combo_box.currentText())
        elif quantities_display_type == 'moles':
            quantities_display_units = str(self.ui.moles_display_units_combo_box.currentText())
        volume = self.ui.volume_spin_box.value()
        volumes_data_units = str(self.ui.volumes_data_units_combo_box.currentText()) 
        volumes_display_units = str(self.ui.volumes_display_units_combo_box.currentText())
        return timepoints_data_units, timepoints_display_units, quantities_data_units, quantities_display_type, quantities_display_units, volume, volumes_data_units, volumes_display_units 

    def units_dict(self):
        units = {}
        units['timepoints_data_units'] = self.ui.timepoints_data_units_combo_box.currentText()
        units['timepoints_display_units'] = self.ui.timepoints_display_units_combo_box.currentText()
        units['quantities_data_units'] = self.ui.quantities_data_units_combo_box.currentText()
        quantities_display_type = self.ui.quantities_display_type_combo_box.currentText()
        units['quantities_display_type'] = quantities_display_type
        if quantities_display_type == 'molecules':
            quantities_display_units = 'molecules'
        elif quantities_display_type == 'concentrations':
            quantities_display_units = self.ui.concentrations_display_units_combo_box.currentText()
        elif quantities_display_type == 'moles':
            quantities_display_units = self.ui.moles_display_units_combo_box.currentText()
        units['quantities_display_units'] = quantities_display_units
#        units['volume'] = self.ui.volume_spin_box.value()
        units['volumes_data_units'] = self.ui.volumes_data_units_combo_box.currentText()
        units['volumes_display_units'] = self.ui.volumes_display_units_combo_box.currentText()
        return units

    def selected_items_results(self, type=float):
        ''' Usage:
            results = self.selected_items_results()
        '''
        run_indices, species_indices, compartment_indices = self.selected_items_amount_indices()
        from_, to, every, _ = self.options()
#        timepoints_data_units, _, quantities_data_units, _, _, _, volumes_data_units, _ = self.units()
        return McssResults(
            filename=self.filename,
            simulation=self.simulation,
            type=type,
            from_=from_,
            to=to,
            step=every,
            run_indices=run_indices,
            species_indices=species_indices,
            compartment_indices=compartment_indices,
            parent=self,
#            timepoints_data_units=timepoints_data_units,
#            quantities_data_units=quantities_data_units,
#            volumes_data_units=volumes_data_units,
            **self.units_dict()
        )


    # actions slots
    
    def calculate(self): #TODO do something useful with array like PModelCheckerResults
        from axes_order_traits import AxesOrder
        ao = AxesOrder()
        result = ao.edit_traits(kind='modal')
        if result:
            axes = [axis.name.lower() for axis in ao.order]
            functions = [axis.function for axis in ao.order]
            
            results = self.selected_items_results()
            array, axes = results.functions_over_successive_axes(axes, functions)

    def histogram(self):
        raise NotImplementedError
#
##        runs, species, compartments = self.selected_items()
##        run_indices, species_indices, compartment_indices = self.selected_items_amount_indices()
#        _, _, _, averaging = self.options()
#        results = self.selected_items_results()
#        _, timepoints_display_units, _, quantities_display_type, quantities_display_units, volume, _, _ = self.units()
#
#        #TODO volumes like plot()
#        if averaging:
#            timepoints, results = results.get_amounts_mean_over_runs()
#            mean_index = 0
#        else:
#            timepoints, results = results.amounts(
#                timepoints_display_units=timepoints_display_units,
#                quantities_display_type=quantities_display_type,
#                quantities_display_units=quantities_display_units,
#                volume=volume if self.simulation.log_volumes != 1 else None,
#            )
#        if len(results) == 0:
#            return
#    
#        print timepoints
#        print results


    # remember these within this instance
    csv_precision = 3
    csv_delimiter = ','
    @wait_cursor
    #FIXME migrate export functionality to McssResults 
    def export_data_as(self, file_name='',
        open_after_save=True, copy_file_name_to_clipboard=True,
        csv_precision=None, csv_delimiter=None,
        #TODO custom titles here?
    ):
        ''' Write selected data to a file in csv, xls or npz format.
        
        (Over?)use of inner functions here can result in crytic exceptions, e.g.
            "UnboundLocalError: local variable 'x' referenced before assignment"
        The actual reason for these errors is that variables inside inner 
        functions are immutable, see:           
            http: // stackoverflow.com / questions / 1414304 / local - functions - in - python / 1414320#1414320
        The correct solution is, in this instance, to pass these variables as
        arguments to the inner functions, and the neatest way to do that is as
        default arguments, see write_csv, fix_delimited_string and write_npz. 
        
        '''
        interactive = True if file_name == '' else False
        if interactive:
            file_name = QFileDialog.getSaveFileName(self,
                self.tr("Save selected timeseries data"),
                ".",
                self.tr("Comma-separated values (*.csv *.txt);;Excel spreadsheets (*.xls);;Numpy compressed (*.npz)"))
            if file_name == '':
                return # user cancelled
            file_name = unicode(file_name)

        runs, species, compartments = self.selected_items()
        run_indices, species_indices, compartment_indices = self.selected_items_amount_indices()
        _, _, _, averaging = self.options()
        results = self.selected_items_results()

        #TODO volumes like plot()
        if averaging:
            timepoints, results = results.get_amounts_mean_over_runs()
            mean_index = 0
        else:
            timepoints, results = results.amounts()
        if len(results) == 0:
            return

        header = ['time']# (%s)' % units]
        #TODO move these to method signature?
#        averaging_header_item = '%s in %s mean of %s runs'
        def averaging_header_item(s, c, r):
            return '%s in %s mean of %s runs' % (s, c, r) if r != 1 else '%s in %s mean of %s run' % (s, c, r)
        header_item = '%s in %s of run %s'
#        def header_item(s, c, r):
#            return '%s in %s of run %s' % (s, c, r)

        def write_csv(csv_precision=csv_precision, csv_delimiter=csv_delimiter, results=results):
            # load default or remembered values
            if csv_precision is None:
                csv_precision = self.csv_precision
            if csv_delimiter is None:
                csv_delimiter = self.csv_delimiter

            if interactive:
                class CSVConfig(HasTraits):
                    precision = Range(0, 18, desc='the number of decimal places to use for floating point values')
                    delimiter = String(minlen=1, maxlen=1, desc="a single character used to delimit fields, e.g. ',', '|', ' ', ';' or '\t' (tab)")
                    view = View(
                        VGroup(
                            HGroup(
                               Item('precision'),
                               Item(label='decimal places'),
                            ),
                            Item('delimiter'),
                            show_border=False,
                        ),
                        buttons=['OK'],
                    )
                csv_config = CSVConfig(precision=csv_precision, delimiter=csv_delimiter)
                ui = csv_config.edit_traits(kind='modal')
                if ui.result:
                    # use and remember option values
                    csv_precision = self.csv_precision = csv_config.precision
                    csv_delimiter = self.csv_delimiter = csv_config.delimiter

            # data
            if averaging:
                indices = [(ci, si) for ci, c in enumerate(compartments) for si, s in enumerate(species)]
                results = tuple((results[mean_index][si, ci] for ci, si in indices))
                fmt = '%%.%sf' % csv_precision
            else:
                indices = [(ri, ci, si) for ri, r in enumerate(runs) for ci, c in enumerate(compartments) for si, s in enumerate(species)]
                results = tuple((results[ri][si, ci, :] for ri, ci, si in indices))
                d = '%d,' * len(results); fmt = ['%.3f'] + d.split(',')[:-1] # timepoints must be floats, levels are ints
            timepoints_and_levels = (timepoints,) + results
            # http://www.scipy.org/Numpy_Example_List#head-786f6bde962f7d1bcb92272b3654bc7cecef0f32
            np.savetxt(file_name, np.transpose(timepoints_and_levels), fmt=fmt, delimiter=csv_delimiter)
            # transpose converts the tuple of 1D arrays to columns

            # header

            # try for similar non-delimiter
            if csv_delimiter == ',':
                non_delimiter = ';'
            elif csv_delimiter == ' ':
                non_delimiter = '_'
            else:
                non_delimiter = ' '

            # ordered list of other potential non-delimiters
            delimiters = list(' _-,;:+&|/?!#\t')

            def fix_delimited_string(s, non_delimiter=non_delimiter):
                ''' Usage: fix_delimited_string(header_item(s.text(), c.text(), r.text()))) '''
                if str(csv_delimiter) in s:
                    i = 0
                    while str(non_delimiter) in s:
                        try:
                            if str(delimiters[i]) not in s:
                                non_delimiter = delimiters[i]
                                break
                        except IndexError:
                            raise ValueError('All potential non-delimiters (%s) found in string "%s"' % (delimiters, s))
                        i += 1
                    return s.replace(csv_delimiter, non_delimiter)
                return s

            header[0] = fix_delimited_string(header[0])
            if averaging:
                for c in compartments:
                    for s in species:
#                        header.append(fix_delimited_string(averaging_header_item % (s.text(), c.text(), len(runs))))
                        header.append(fix_delimited_string(averaging_header_item(s.text(), c.text(), len(runs))))
            else:
                for r in runs:
                    for c in compartments:
                        for s in species:
                            header.append(fix_delimited_string(header_item % (s.text(), c.text(), r.text())))
#                            header.append(fix_delimited_string(header_item(s.text(), c.text(), r.text())))
            # write header at beginning of file
            from infobiotics.commons.files import prepend_line_to_file
            prepend_line_to_file(csv_delimiter.join(header), file_name)

        def write_xls():
            ''' https: // secure.simplistix.co.uk / svn / xlwt / trunk / README.html '''
            wb = xlwt.Workbook()
            try:
                ws = wb.add_sheet(os.path.basename(self.simulation.model_input_file)[:31])
            except:
                ws = wb.add_sheet('McssResults')
            ws.write(0, 0, header[0])
            for ti in range(len(timepoints)):
                ws.write(1 + ti, 0, timepoints[ti])
            if averaging:
                for ci, c in enumerate(compartments):
                    for si, s in enumerate(species):
                        y = 1 + si + (ci * len(species))
#                        ws.write(0, y, averaging_header_item % (s.text(), c.text(), len(runs)))
                        ws.write(0, y, averaging_header_item(s.text(), c.text(), len(runs)))
                        for ti in range(len(timepoints)):
                            ws.write(1 + ti, y, results[mean_index][si, ci, ti])
            else:
                for ri, r in enumerate(runs):
                    for ci, c in enumerate(compartments):
                        for si, s in enumerate(species):
                            y = 1 + si + (ci * len(species)) + (ri * len(species) * len(compartments))
                            ws.write(0, y, header_item % (s.text(), c.text(), r.text()))
                            for ti in range(len(timepoints)):
                                ws.write(1 + ti, y, results[ri][si, ci, ti])
            wb.save(file_name)

        def write_npz(species_indices=species_indices, compartment_indices=compartment_indices):
            # convert QString to str #TODO is this now unncessary with QString api version 2?
            species_names = [str(s.text()) for s in species]
            compartment_labels_and_positions = [str(c.text()) for c in compartments]
            run_numbers = [str(r.text()) for r in runs]
            kwargs = dict(
                run_indices=np.array(run_indices),
                run_numbers=run_numbers,
                species_indices=species_indices,
                species_names=species_names,
                compartment_indices=compartment_indices,
                compartment_labels_and_positions=compartment_labels_and_positions,
                timepoints=timepoints,
                model_file_name=os.path.basename(self.simulation.model_input_file),
                data_file_name=os.path.basename(self.simulation.data_file),
            )
            if averaging:
                kwargs['means'] = results[mean_index]
                kwargs['shape'] = ('species', 'compartment', 'timepoint')
            else:
                kwargs['levels'] = results
                kwargs['shape'] = ('run', 'species', 'compartment', 'timepoint')
            np.savez(file_name, **kwargs)

        if file_name.endswith('.npz'):
            write_npz()
        elif file_name.endswith('.xls'):
            write_xls()
        else:
            write_csv()#csv_precision, csv_delimiter) # done using default values

        if copy_file_name_to_clipboard:
            from infobiotics.commons.qt4 import copy_to_clipboard
            copy_to_clipboard(file_name)

        if open_after_save:
#            if file_name.endswith('.csv') or file_name.endswith('.xls'):
            from infobiotics.commons.qt4 import open_file
            open_file(file_name)

        return file_name

    #TODO 
    @wait_cursor
    def surfacePlot(self):
        results = self.selected_items_results()
        surfaces = results.surfaces()
        runs = surfaces.shape[0]
        surfaces = mcss_results.mean(surfaces, 0) # do mean across all runs
        if surfaces is None:
            return
        (xmin, xmax), (ymin, ymax) = results.xy_min_max()
        surfaces_ = []
        species = self.selected_species()
        for si, s in enumerate(species):
#            surface = surfaces[0, si] # if we haven't taken the mean
            surface = surfaces[si] # if we've taken the mean
            zmax = np.max(surface)
#            if zmax == 0: print "%s never amounts to anything." % s.name
            extent = [xmin, xmax, ymin, ymax, 0, zmax]
#            warp_scale = 'auto' # doesn't work
            warp_scale = (1 / zmax) * 10 #FIXME 10 is magic number
            surface = Surface(surface, warp_scale, extent, s.text() if runs == 1 else s.text() + ' (mean)', self.units_dict()['quantities_display_units'], results.timepoints)
            surfaces_.append(surface)
        self.spatial_plots_window = SpatialPlotsWindow(surfaces_, self)
        self.spatial_plots_window.show()


    @wait_cursor
    def plot(self): #TODO move most of this to McssResults
        '''Plot selected data. '''

#        # old 
#        runs, species, compartments = self.selected_items()
##        run_indices, species_indices, compartment_indices = self.selected_items_amount_indices()
#        _, _, _, averaging = self.options()
#        timepoints_data_units, timepoints_display_units, quantities_data_units, quantities_display_type, quantities_display_units, volume, volumes_data_units, volumes_display_units = self.units()
#        results = self.selected_items_results()
#
#        if averaging:
##            timepoints, amounts = results.get_amounts_mean_over_runs()
#            timepoints, amounts = results.get_functions_over_runs((mcss_results.mean, mcss_results.std))
#            mean_index = 0
#            std_index = 1
##            if self.volumes_selected:
##                timepoints, volumes = results.get_volumes_mean_over_runs() #TODO
#        else:
##            timepoints = results.timepoints(timepoints_display_units=timepoints_display_units)
#            timepoints = results.timepoints
#            timepoints.units = time_units[timepoints_display_units]
#            amounts = results.amounts(
#                quantities_display_type=quantities_display_type,
#                quantities_display_units=quantities_display_units,
#                volume=volume if self.simulation.log_volumes != 1 else None,
#            )
#            if self.volumes_selected:
#                _, volumes = results.get_volumes(
#                    volumes_display_units=volumes_display_units,
#                )
#        if len(amounts) == 0 and (self.volumes_selected and len(volumes) == 0):
#            return
#        from timeseries import Timeseries
#        timeseries = []
#
#        volumes_species = Species(
#            index=None, #TODO hack
#            name='Volumes',
#            simulation=self.simulation,
#        )
#
#        if averaging:
##            raise NotImplementedError
#            for ci, c in enumerate(compartments):
#                for si, s in enumerate(species):
#                    timeseries.append(
#                        Timeseries(
#                            runs=[run.data for run in runs],
#                            species=s.data,
#                            compartment=c.data,
#                            timepoints=timepoints,
#                            timepoints_units=timepoints_display_units,
#                            values_type='Concentration' if quantities_display_type == 'concentrations' else 'Amount',
#                            values=amounts[ri, si, ci, :], #FIXME ri should be fi
#                            values_units=quantities_display_units,
#                            _colour=colours.colour(si),
#                        )                                          
#                    )
#                if self.volumes_selected:
#                    timeseries.append(
#                        Timeseries(
#                            runs=[run.data for run in runs],
#                            species=volumes_species,
#                            compartment=c.data,
#                            timepoints=timepoints,
#                            timepoints_units=timepoints_display_units,
#                            values_type='Volume',
#                            values=volumes[ri, ci, :], #FIXME don't know what ri should be
#                            values_units=volumes_display_units,
#                            _colour=colours.colour(len(species) + ci),
#                        )                                          
#                    )
#        else:
#            for ri, r in enumerate(runs):
#                for ci, c in enumerate(compartments):
#                    for si, s in enumerate(species):
#                        timeseries.append(
#                            Timeseries(
#                                run=r.data,
#                                species=s.data,
#                                compartment=c.data,
#                                timepoints=timepoints,
#                                timepoints_units=timepoints_display_units,
#                                values_type='Concentration' if quantities_display_type == 'concentrations' else 'Amount',
#                                values=amounts[ri, si, ci, :],
#                                values_units=quantities_display_units,
#                                _colour=colours.colour(si),
#                            )
#                        )
#                        
#                    if self.volumes_selected:
#                        timeseries.append(
#                            Timeseries(
#                                run=r.data,
#                                species=volumes_species,
#                                compartment=c.data,
#                                timepoints=timepoints,
#                                timepoints_units=timepoints_display_units,
#                                values_type='Volume',
#                                values=volumes[ri, ci, :],
#                                values_units=volumes_display_units,
#                                _colour=colours.colour(len(species) + ci),
#                            )                                          
#                        )
            
        results = self.selected_items_results()
        print results.timeseries_information()
        timeseries = results.timeseries(
            amounts=True,
            volumes=True if results.has_volumes else False,
            mean_over_runs=True if self.ui.average_over_selected_runs_check_box.isChecked() else False,
        )
#        timeseries = results.timeseries(amounts=True, volumes=False, mean_over_runs=True)
#        timeseries = results.timeseries(amounts=False, volumes=True, mean_over_runs=True)
#        timeseries = results.timeseries(amounts=True, volumes=True, mean_over_runs=False) 
#        timeseries = results.timeseries(amounts=True, volumes=False, mean_over_runs=False)
#        timeseries = results.timeseries(amounts=False, volumes=True, mean_over_runs=False)
        
        from timeseries_plot import TimeseriesPlot
        TimeseriesPlot(
            timeseries=timeseries,
            window_title='Timeseries Plot(s) for %s' % self.filename,
        ).edit_traits()


def main():
    argv = qApp.arguments()
#    argv.insert(1, '/home/jvb/phd/eclipse/infobiotics/dashboard/examples/infobiotics-examples-20110208/quickstart-NAR/NAR_simulation.h5')
#    argv.insert(1, '/home/jvb/phd/eclipse/infobiotics/dashboard-mcss_results/infobiotics/mcss/results/tests/germination_09.h5') # has volumes dataset
    argv.insert(1, '/home/jvb/phd/eclipse/infobiotics/dashboard-mcss_results/infobiotics/mcss/results/tests/NAR_simulation.h5') # has no volumes dataset
    if len(argv) > 2:
        print 'usage: python mcss_results_widget.py {h5file}'#TODO mcss-results {h5file}'
        sys.exit(2)
    if len(argv) == 1:
#        shared.settings.register_infobiotics_settings()
        w = McssResultsWidget()
    elif len(argv) == 2:
        w = McssResultsWidget(filename=argv[1])
    centre_window(w)
    w.show()
    return w
#    shared.settings.restore_window_size_and_position(w)


if __name__ == "__main__":
    main()
#    test()
#    test_McssResults_export_data_as()
#    test_volumes()
#    profile_McssResults_get_amounts()
    exit(qApp.exec_())
