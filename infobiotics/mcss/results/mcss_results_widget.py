from __future__ import division

import infobiotics
from quantities.quantity import Quantity

from enthought.traits.api import HasTraits, Range, String
from enthought.traits.ui.api import View, VGroup, HGroup, Item

from infobiotics.mcss.results.spatial_plots import Surface, SpatialPlotsWindow,\
    RedVsGreen

from PyQt4.QtCore import QSettings, QVariant, QDir, QFileInfo, SIGNAL, Qt, QString
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

from infobiotics.mcss.results import mcss_results
from mcss_results import McssResults
from infobiotics.commons.quantities.units.time import time_units
from infobiotics.commons.quantities.units.volume import volume_units

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
    '''Extract and plot data from mcss simulations'''
    
    __settings_group = "McssResultsWidget"

    def __init__(self, filename=None):
        '''Setup widgets, connect signals to slots and attempt load.'''
        QWidget.__init__(self) # initialize base class

        self.ui = Ui_McssResultsWidget()
        self.ui.setupUi(self) # QPixmap: It is not safe to use pixmaps outside the GUI thread

        self.ui.calculate_button.setVisible(False) # hide buttons that don't work #TODO make it work

#        self.ui.compartments_list_widget.setToolTip('')

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
        if hasattr(self, 'timeseries_plot'):
            self.timeseries_plot.dispose()
#        shared.settings.save_window_size_and_position(self, self.__settings_group)
        self.save_settings()
        event.accept()

    def load_settings(self):
        settings = QSettings()
        settings.beginGroup(self.__settings_group)
        self.current_directory = unicode(settings.value('current_directory', QVariant(QDir.currentPath())).toString())
        #TODO load options and units
        settings.endGroup()

    def save_settings(self):
        settings = QSettings()
        settings.beginGroup(self.__settings_group)
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

#        if sip.getapi('QString') == 1:
        filename = unicode(filename) # must convert QString into unicode

        simulation = None
        try:
            simulation = load_h5(filename)
        except IOError, e:
#            QMessageBox.warning(self, QString("Error"), QString("There was an error reading %s\n%s") % (filename, e))
            if os.path.exists('mcss-error.log'):
                error_log = open("mcss-error.log", 'r')
                error_message = error_log.read()
                error_log.close()
                os.remove('mcss-error.log')
                QMessageBox.warning(self, QString("Error"), QString("Unable to execute model:\n\n%s") % (error_message.replace('error: ', '', 1)))
            else:
                QMessageBox.warning(self, QString("Error"), QString(str(e).replace('`', '')))
        except AttributeError, e:
            QMessageBox.warning(self, QString("Error"), QString(str(e).replace('`', '')+ "\nDid you use a old version of mcss (<0.0.19)?"))
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
            SimulationListWidgetItem(i, ui.runs_list_widget)
        for i in simulation._species_list:
            SimulationListWidgetItem(i, ui.species_list_widget)
        for i in simulation._runs_list[0]._compartments_list: #FIXME can't rely on run1 alone if compartments divide
            SimulationListWidgetItem(i, ui.compartments_list_widget)
        
        # runs
        runs = ui.runs_list_widget.count()
        ui.random_runs_spin_box.setRange(1, runs)
        if runs == 1:
            ui.runs_list_widget.selectAll() # should check select_all_runs_check_box automatically
            hide_widgets(
                ui._runs_group_box,
                ui.average_over_selected_runs_check_box,
            )
            ui.average_over_selected_runs_check_box.setChecked(False)
        else: # runs > 1
            show_widgets(
                ui._runs_group_box,         
                ui.average_over_selected_runs_check_box,
            )
#            enable_widgets(
#                ui.random_runs_spin_box,
#                ui.random_runs_label,
#                ui.average_over_selected_runs_check_box,
#            )
#            enable_widgets(ui.select_all_runs_check_box)
            ui.average_over_selected_runs_check_box.setChecked(True) # check average over runs

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
        if self.simulation.log_volumes in ('true', 1):
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
            )
            if num_selected_species >= 1 and num_selected_compartments > 1:
                enable_widgets(self.ui.visualise_population_button)
            else:
                disable_widgets(self.ui.visualise_population_button)
            
            if num_selected_runs > 1 or num_selected_compartments > 1:
                enable_widgets(self.ui.plot_histogram_button)
                self.ui.plot_histogram_button.setToolTip("Plot distributions of species in runs or compartments")
            else:
                self.ui.plot_histogram_button.setToolTip("To enable select two or more runs or compartments")
            
            if num_selected_runs > 1:
                enable_widgets(self.ui.calculate_button)


            #TODO show numdatapoints with warning if too high

            results = self.selected_items_results()
            _, _, _, averaging = self.options()
            numtimeseries = results.len_timeseries(True, self.volumes_selected, averaging) 
            numtimepoints = results.num_timepoints * numtimeseries
            
            numsurfaces = results.num_selected_species

            (xmin, xmax), (ymin, ymax) = results.xy_min_max()
            numsurfacetimepoints = numsurfaces * ((xmax - xmin) + 1) * ((ymax - ymin) + 1) * results.num_timepoints 
            
#            print '%s timeseries' % numtimeseries, '(%s timepoints)' % numtimepoints
#            print '%s surfaces' % numsurfaces, '(%s timepoints)' % numsurfacetimepoints
#            print 


            # no more than 6 surfaces
            if num_selected_species <= 6 and num_selected_compartments >= 4:
                enable_widgets(self.ui.visualise_population_button)
                self.ui.visualise_population_button.setToolTip("Animate species levels as a surface over the lattice")
            else:
                self.ui.visualise_population_button.setToolTip("To enable select more than 4 compartments and fewer than 7 species")
                
#            # no more than 10 timeseries (per species)
#            if num_selected_compartments > 10:
#                disable_widgets(self.ui.plot_timeseries_button)
#            else:
#                enable_widgets(self.ui.plot_timeseries_button)


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
        '''Return selected species after removing volumes.'''
        selected_species = self.ui.species_list_widget.selectedItems()
        if self.simulation.log_volumes in ('true', 1) and self.volumes_list_widget_item in selected_species:
            selected_species.remove(self.volumes_list_widget_item)
            self.volumes_selected = True
        else:
            self.volumes_selected = False
        return selected_species
    
    # compound accessors

    def selected_items(self):
        '''Usage: runs, species, compartments = selected_items()'''
        runs = self.ui.runs_list_widget.selectedItems()
        species = self.selected_species()
        compartments = self.ui.compartments_list_widget.selectedItems()
        return runs, species, compartments

    def selected_items_amount_indices(self):
        '''Usage: run_indices, species_indices, compartment_indices = self.selected_items_amount_indices() 
            
        Use for ri, r in enumerate(run_indices): for selected results
         
        '''
        runs, species, compartments = self.selected_items()
        run_indices = [item.amounts_index for item in runs]
        species_indices = [item.amounts_index for item in species]
        compartment_indices = [item.amounts_index for item in compartments]
        return run_indices, species_indices, compartment_indices

    def options(self):
        '''Usage: from_, to, every, averaging = self.options()'''
        from_ = self.ui.from_spin_box.value()
        to = self.ui.to_spin_box.value()
        every = self.ui.every_spin_box.value()
        averaging = self.ui.average_over_selected_runs_check_box.isChecked()
        return from_, to, every, averaging

    def volume(self):
        return self.ui.volume_spin_box.value()

    def units_dict(self):
        '''McssResults(..., **self.units_dict())'''
        units = {}
        units['timepoints_data_units'] = str(self.ui.timepoints_data_units_combo_box.currentText())
        units['timepoints_display_units'] = str(self.ui.timepoints_display_units_combo_box.currentText())
        units['quantities_data_units'] = str(self.ui.quantities_data_units_combo_box.currentText())
        quantities_display_type = str(self.ui.quantities_display_type_combo_box.currentText())
        units['quantities_display_type'] = str(quantities_display_type)
        if quantities_display_type == 'molecules':
            quantities_display_units = 'molecules'
        elif quantities_display_type == 'concentrations':
            quantities_display_units = str(self.ui.concentrations_display_units_combo_box.currentText())
        elif quantities_display_type == 'moles':
            quantities_display_units = str(self.ui.moles_display_units_combo_box.currentText())
        units['quantities_display_units'] = str(quantities_display_units)
        units['volumes_data_units'] = str(self.ui.volumes_data_units_combo_box.currentText())
        units['volumes_display_units'] = str(self.ui.volumes_display_units_combo_box.currentText())
        return units

    def selected_items_results(self, type=float):
        ''' Usage:
            results = self.selected_items_results()
        '''
        run_indices, species_indices, compartment_indices = self.selected_items_amount_indices()
        from_, to, every, _ = self.options()
        units_dict = self.units_dict()
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
            default_volume=Quantity(self.ui.volume_spin_box.value(), volume_units[units_dict['volumes_data_units']]),
            **units_dict
        )


    # actions slots
    
    def calculate(self): #TODO do something useful with array like PModelCheckerResults
        from axes_order_traits import AxesOrder
        ao = AxesOrder()
        result = ao.edit_traits(kind='modal').result
        if result:
            axes = [axis.name.lower() for axis in ao.order]
            functions = [axis.function for axis in ao.order]
            
            results = self.selected_items_results()
            array, axes = results.functions_over_successive_axes(axes, functions)
            #TODO
        

    def histogram(self):
#        raise NotImplementedError
        from histograms import Histogram
        results = self.selected_items_results()
        Histogram.fromresults(results).configure_traits()


    csv_precision = mcss_results.McssResults.csv_precision
    csv_delimiter = mcss_results.McssResults.csv_delimiter

    @wait_cursor
    def export_data_as(self, 
        open_after_save=True, copy_filename_to_clipboard=True,
        csv_precision=None, csv_delimiter=None,
#        amounts=True, 
#        volumes=False, #TODO 
#        ci_degree=None, #TODO
    ):
        '''Write selected data to a file in csv, xls or npz format.'''
        
        filename = QFileDialog.getSaveFileName(self,
            self.tr("Save selected timeseries data"),
            ".",
            self.tr("All supported types (*.csv *.txt *.xls *.npz);;Comma-separated values (*.csv *.txt);;Excel spreadsheets (*.xls);;Numpy compressed (*.npz)"))
        if filename == '':
            return # user cancelled
        filename = unicode(filename)

        if filename.lower().endswith('.csv'):
            if csv_precision is None:
                csv_precision = self.csv_precision
            if csv_delimiter is None:
                csv_delimiter = self.csv_delimiter

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

        _, _, _, averaging = self.options()
        results = self.selected_items_results()

        results.export_timeseries(filename, amounts=True, volumes=False, individualruns=not averaging, csv_precision=csv_precision, csv_delimiter=csv_delimiter)

        if copy_filename_to_clipboard:
            from infobiotics.commons.qt4 import copy_to_clipboard
            copy_to_clipboard(filename)

        if open_after_save:
            if filename.endswith('.csv') or filename.endswith('.xls'):
                from infobiotics.commons.qt4 import open_file
                open_file(filename)

        return filename

            
    @wait_cursor
    def plot(self, **kwargs):
        '''Plot selected data. '''
        results = self.selected_items_results()
#        print results.timeseries_information()
        self.timeseries_plot = results.timeseries_plot(parent=self, mean_over_runs=True if self.ui.average_over_selected_runs_check_box.isChecked() else False, **kwargs) 
        widget = self.timeseries_plot.control
        widget.setWindowFlags(Qt.CustomizeWindowHint|Qt.WindowMinMaxButtonsHint|Qt.WindowCloseButtonHint)
        widget.show()
        

    #TODO 
    @wait_cursor
    def surfacePlot(self):
#        return self.redVsGreenPlot()
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
            #TODO mean of X runs
            surface = Surface(surface, warp_scale, extent, s.text() if runs == 1 else s.text() + ' (mean)', self.units_dict()['quantities_display_units'], results.timepoints)
            surfaces_.append(surface)
        self.spatial_plots_window = SpatialPlotsWindow(surfaces_, self)
        try:
            self.spatial_plots_window.show()
        except RuntimeError, e:
            QMessageBox.critical(
                self, 
                QString('Surface plotting failed'), 
                QString(str(e))
            )

    @wait_cursor
    def redVsGreenPlot(self): #TODO button
        results = self.selected_items_results()
        surfaces = results.surfaces()
        runs = surfaces.shape[0]
        surfaces = mcss_results.mean(surfaces, 0) # do mean across all runs
        
        xymultiplier = 1
        tmultiplier = 1

#        # pattern formation
#        xymultiplier = 5
#        tmultiplier = 11
        
#        # pulse inverter
#        xymultiplier = 3
#        tmultiplier = 8
        
        surfaces = np.array([interpolate(surfaces[i], xymultiplier, tmultiplier) for i in range(len(surfaces))])
#        print surfaces.shape
#        print results.timepoints.shape
        
        (xmin, xmax), (ymin, ymax) = results.xy_min_max()
        species = self.selected_species()
        species_names = []
        zmaxs = []
        for si, s in enumerate(species):
            species_names.append(s.text())
            zmax = np.max(surfaces[si])
            zmaxs.append(zmax)
        extent = np.array([xmin, xmax, ymin, ymax, 0, np.max(zmaxs)])
        surface = RedVsGreen(
            surfaces, 
            extent, 
            species_names, 
            self.units_dict()['quantities_display_units'], 
            np.linspace(results.timepoints[0], results.timepoints[-1], len(results.timepoints) * tmultiplier), 
            self.units_dict()['timepoints_display_units'], 
            suffix=' (mean)' if runs > 1 else '') #TODO mean of X runs
        self.spatial_plots_window = SpatialPlotsWindow([surface], self)
        try:
            self.spatial_plots_window.show()
        except RuntimeError, e:
            QMessageBox.critical(
                self, 
                QString('Surface plotting failed'), 
                QString(str(e))
            )


from scipy import mgrid, ndimage

def interpolate(surfacearray, xymultiplier, tmultiplier, order=1):
    '''Interpolates an array of surfaces where surfacearray.shape = (x, y, t) 
    and surface at time t = surfacearray[:, :, t]
    
    xymultipler and tmultiplier must be integers greater than 1
    
    order must be an integer in the range 0-5
    
    '''
    xmax, ymax, tmax = surfacearray.shape 
    interpolated = np.ndarray((xmax * xymultiplier, ymax* xymultiplier, tmax * tmultiplier))
    numx, numy, numt = (complex(i) for i in interpolated.shape) 
    coords = mgrid[0:xmax-1:numx, 0:ymax-1:numy, 0:tmax-1:numt]
    interpolated = ndimage.map_coordinates(surfacearray, coords, order=1)        
    return interpolated



def main(filename=None):
    '''see spatial_splot.test for how to automate selections, etc.'''
#    argv = qApp.arguments()
    argv = sys.argv
    
    if filename is not None:
        self = McssResultsWidget(filename=filename)
    else:
        if len(argv) > 2:
            print 'usage: python mcss_results_widget.py {h5file}'#TODO mcss-results {h5file}'
            sys.exit(2)
        if len(argv) == 1:
    #        shared.settings.register_infobiotics_settings()
            self = McssResultsWidget()
        elif len(argv) == 2:
            self = McssResultsWidget(filename=argv[1])
    centre_window(self)
    self.show()

    self.raise_()
    qApp.processEvents()
    
#    self.raise_()
#    qApp.processEvents()
    
#    shared.settings.restore_window_size_and_position(self)

#    return self
    exit(qApp.exec_())


if __name__ == "__main__":
    main()
#    exit(qApp.exec_())
