from __future__ import division

import sys
from random import randint
import os

import infobiotics # must be before traits imports

# settings
from PyQt4.QtGui import qApp
# must use qApp not QApplication(sys.argv) when mixing with TraitsUI
if qApp is None:
    from PyQt4.QtGui import QApplication
    app = QApplication(sys.argv) # must keep reference too
qApp.setOrganizationDomain('www.infobiotics.org')
qApp.setOrganizationName('Infobiotics')
qApp.setApplicationName('Infobiotics Dashboard')
qApp.setApplicationVersion(infobiotics.version)

from PyQt4.QtCore import Qt #@UnusedImport
from PyQt4.QtCore import QSettings, QVariant, QDir, QFileInfo, SIGNAL, SLOT, QString
from PyQt4.QtGui import QWidget, QListWidgetItem, QItemSelectionModel, QFileDialog, QMessageBox

from infobiotics.commons.qt4 import *#@UnusedWildImport

from enthought.traits.api import HasTraits, Range, String #@UnresolvedImport
from enthought.traits.ui.api import View, VGroup, HGroup, Item #@UnresolvedImport

import numpy as np

from quantities.quantity import Quantity

from infobiotics.commons.quantities.units.volume import volume_units
from infobiotics.commons.files import readable

from infobiotics.mcss.results import mcss_results
from mcss_results import McssResults

from infobiotics.mcss.results.spatial_plots import Surface, SpatialPlotsWindow, RedVsGreen

from simulation import load_h5

from simulation_list_widget_item import SimulationListWidgetItem

from ui_mcss_results_widget import Ui_McssResultsWidget


class McssResultsWidget(QWidget):
    '''Extract and plot data from mcss simulations'''
    
    def __init__(self, filename=None):
        '''Setup widgets, connect signals to slots and attempt load.'''
        self.filename = None

        QWidget.__init__(self)
        self.ui = Ui_McssResultsWidget()
        self.ui.setupUi(self) # QPixmap: It is not safe to use pixmaps outside the GUI thread

        self.connect_signals_to_slots()

        self._file_name_line_edit_text_orig = self.ui.file_name_line_edit.text() # remember text from Ui_McssResultsWidget

#        self._geometry_orig = self.geometry() # remember geometry from Ui_McssResultsWidget
        self.restore_geometry()
        
        self.restore_current_directory()
        
        self.loaded = False # used by load to determine whether to fail silently and keep widgets enabled 
        if filename:
            self.load(filename)
        if not self.loaded:
            self.load_failed()
            
        self.update_ui()

    def connect_signals_to_slots(self):
        self.connect(self.ui.load_button, SIGNAL("clicked()"), self.load)

        self.ui.runs_list_widget.connect_all_selected_check_box(self.ui.select_all_runs_check_box)
        self.ui.species_list_widget.connect_all_selected_check_box(self.ui.select_all_species_check_box)
        self.ui.compartments_list_widget.connect_all_selected_check_box(self.ui.select_all_compartments_check_box)
        # using ListWidget methods
        self.ui.species_list_widget.connect_filter_line_edit(self.ui.filter_species_line_edit)
        self.ui.compartments_list_widget.connect_filter_line_edit(self.ui.filter_compartments_line_edit)

        for widget in self.ui.runs_list_widget, self.ui.species_list_widget, self.ui.compartments_list_widget:
            self.connect(widget, SIGNAL('itemSelectionChanged()'), self.update_ui)
            self.connect(widget, SIGNAL('itemSelectionChanged()'), self.update_datapoints_label)
        # numtimepoints
        self.connect(self.ui.every_spin_box, SIGNAL('valueChanged(int)'), self.update_datapoints_label)
        self.connect(self.ui.from_spin_box, SIGNAL('valueChanged(double)'), self.update_datapoints_label)
        self.connect(self.ui.to_spin_box, SIGNAL('valueChanged(double)'), self.update_datapoints_label)
        self.connect(self.ui.average_over_selected_runs_check_box, SIGNAL('toggled(bool)'), self.update_datapoints_label)

        for function in self.select_random_runs, lambda: (
            self.ui.select_all_runs_check_box.setChecked(False)
                if self.ui.random_runs_spin_box.value() < self.ui.random_runs_spin_box.maximum()
                    else self.ui.select_all_runs_check_box.setChecked(True)
        ):
            self.connect(self.ui.random_runs_spin_box, SIGNAL('valueChanged(int)'), function)

        # ensure from < to
        self.connect(self.ui.from_spin_box, SIGNAL("valueChanged(double)"), self.ui.to_spin_box.set_minimum)
        self.connect(self.ui.to_spin_box, SIGNAL("valueChanged(double)"), self.ui.from_spin_box.set_maximum)

        self.quantities_display_type_changed(self.ui.quantities_display_type_combo_box.currentText()) # ui update
        self.connect(self.ui.quantities_display_type_combo_box, SIGNAL('currentIndexChanged(QString)'), self.quantities_display_type_changed)

        self.connect(self.ui.plot_histogram_button, SIGNAL("clicked()"), self.histogram)
        self.connect(self.ui.export_data_as_button, SIGNAL("clicked()"), self.export_data_as)
        self.connect(self.ui.plot_timeseries_button, SIGNAL("clicked()"), self.plot)
        self.connect(self.ui.visualise_population_button, SIGNAL("clicked()"), self.surfacePlot)

        self.connect(self.ui.calculate_button, SIGNAL('clicked()'), self.calculate)
        #TODO implement multi-dimensional calculation plotter
        self.ui.calculate_button.setVisible(False) # hide buttons that don't work


    def closeEvent(self, event):
        self.save_settings()
        if self.loaded:
            self.save_geometry()

        if hasattr(self, '_timeseries_plot_uis'):
            for ui in self._timeseries_plot_uis:
                ui.dispose()
        event.accept()


    __settings_group = 'McssResultsWidget'

#    def settings(self, *settings_group): #TODO need to endGroup() explicitly!
#        settings = QSettings()
#        if settings_group:
#            settings.beginGroup('/'.join((self.__settings_group, ) + settings_group))
#        else:
#            settings.beginGroup(self.__settings_group)
#        return settings

    def _settings_group(self, *settings_groups):
        if settings_groups:
            return '/'.join((self.__settings_group,) + settings_groups)
        return self.__settings_group 
        
    def save_geometry(self):
        settings = QSettings()
        settings.beginGroup(self._settings_group())
        settings.setValue('geometry', self.geometry())
        settings.endGroup()
        
    def restore_geometry(self):
        settings = QSettings()
        settings.beginGroup(self._settings_group())
        self.setGeometry(settings.value('geometry', self.geometry()).toRect())
        settings.endGroup()
        
    def save_current_directory(self):
        settings = QSettings()
        settings.beginGroup(self._settings_group())
        settings.setValue('current_directory', QVariant(unicode(self.current_directory)))
        settings.endGroup()
        
    def restore_current_directory(self):
        settings = QSettings()
        settings.beginGroup(self._settings_group())
        self.current_directory = unicode(settings.value('current_directory', QVariant(QDir.currentPath())).toString())
        settings.endGroup()

#    def previous(self): #TODO
#        settings = QSettings()
#        settings.beginGroup(self._settings_group())
#        previous = unicode(settings.value('previous').toString())
#        return previous


    def save_settings(self):
        '''Save simulation settings and current filename as previous (not geometry or current directory)'''
        if not self.filename:
            return
        
        settings = QSettings()
        
        settings.beginGroup(self._settings_group())
        settings.setValue('previous', QVariant(self.filename))
        settings.endGroup() # vital
        
        settings.beginGroup(self._settings_group(self.filename))
        settings.setValue('units', QVariant(self.units_dict()))
        settings.setValue('from', QVariant(self.ui.from_spin_box.value()))
        settings.setValue('to', QVariant(self.ui.to_spin_box.value()))
        settings.setValue('every', QVariant(self.ui.every_spin_box.value()))
        settings.setValue('averaging', QVariant(self.ui.average_over_selected_runs_check_box.checkState()))
        settings.setValue('all_runs', QVariant(self.ui.select_all_runs_check_box.checkState()))
        settings.setValue('all_species', QVariant(self.ui.select_all_species_check_box.checkState()))
        settings.setValue('all_compartments', QVariant(self.ui.select_all_compartments_check_box.checkState()))
        settings.setValue('runs', QVariant([modelIndex.row() for modelIndex in self.ui.runs_list_widget.selectedIndexes()]))
        settings.setValue('species', QVariant([modelIndex.row() for modelIndex in self.ui.species_list_widget.selectedIndexes()]))
        settings.setValue('compartments', QVariant([modelIndex.row() for modelIndex in self.ui.compartments_list_widget.selectedIndexes()]))
        settings.setValue('species_filter', QVariant(self.ui.filter_species_line_edit.text()))
        settings.setValue('compartments_filter', QVariant(self.ui.filter_compartments_line_edit.text()))
        settings.setValue('volume', QVariant(self.ui.volume_spin_box.value()))
        settings.endGroup()


    def load_settings(self):
        '''Restore simulation settings (not geometry or current directory)'''
        if not (self.filename and readable(self.filename)):
            return

        settings = QSettings()
        
        settings.beginGroup(self._settings_group(self.filename))

        units = settings.value('units').toPyObject()
        if units:
            units = dict((unicode(key), unicode(value)) for key, value in units.items())
            self.set_units(**units)
        
        def restore_selection(checkboxsetting, checkbox, listwidgetsetting, listwidget):
            checked, ok = settings.value(checkboxsetting, QVariant(Qt.Unchecked)).toInt()
            if checked:
                checkbox.setCheckState(checked)
            else:
                rows = settings.value(listwidgetsetting).toPyObject()
                if rows is None or len(rows) > 100:
                    rows = []
                for row in rows: 
                    if not isinstance(row, int):
                        row, ok = row.toInt()
                    else:
                        ok = True
                    if ok:
                        listwidget.select(row)

        restore_selection('all_species', self.ui.select_all_species_check_box, 'species', self.ui.species_list_widget)
        restore_selection('all_compartments', self.ui.select_all_compartments_check_box, 'compartments', self.ui.compartments_list_widget)

        restore_selection('all_runs', self.ui.select_all_runs_check_box, 'runs', self.ui.runs_list_widget)
        if self.ui.runs_list_widget.count() == 1:
            self.ui.runs_list_widget.selectAll()

        self.ui.filter_species_line_edit.setText(settings.value('species_filter', '').toString())
        
        self.ui.filter_compartments_line_edit.setText(settings.value('compartments_filter', '').toString())

        from_, ok = settings.value('from', 0.0).toDouble()
        if ok: 
            self.ui.from_spin_box.setValue(from_)
#        to, ok = settings.value('to', None).toDouble()
#        if ok:
#            self.ui.to_spin_box.setValue(to)
        every, ok = settings.value('every', QVariant(1)).toInt()
        if ok:
            self.ui.every_spin_box.setValue(every)

        checked, ok = settings.value('averaging', Qt.Checked).toInt() 
        if ok:
            self.ui.average_over_selected_runs_check_box.setCheckState(checked)

        volume, ok = settings.value('volume', QVariant(0.01)).toDouble()
        if ok:
            self.ui.volume_spin_box.setValue(volume)

        settings.endGroup()


    def load(self, filename=None):

        # save settings for current file before possibly loading a new one
        self.save_settings()
        
        # save current directory before possibly find a new one
        self.save_current_directory()
        
        if filename is None:
            filename = QFileDialog.getOpenFileName(
               self,
               self.tr("Open HDF5 simulation data file"),
               self.current_directory,
               self.tr("HDF5 data files (*.h5 *.hdf5);;All files (*)")
            )
            if filename == '':
                if self.loaded:
                    return
                else:
                    self.load_failed()
                    return False

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
            QMessageBox.warning(self, QString("Error"), QString(str(e).replace('`', '') + "\nDid you use a old version of mcss (<0.0.19)?"))
        if simulation == None:
            if self.loaded:
                return # continue with previously loaded file
            else:
                self.load_failed()
                return False

        # set new simulation, filename and current directory
        self.simulation = simulation
        self.filename = filename
        self.current_directory = QFileInfo(filename).absolutePath()
        
        # save new current directory
        self.save_current_directory()
        
        self.loaded = True
        self.load_succeeded()

        # load settings for new filename
        self.load_settings()
        
        return True


    def load_failed(self):
        '''Hides, clears, unchecks and disables relevant widgets'''
        
        hide_widgets(
#            self.ui._timepoints_group_box,
#            self.ui._runs_group_box,
#            self.ui._species_group_box,
#            self.ui._compartments_group_box,
#            self.ui._data_group_box,
#            
            self.ui.runs_selected_and_total_label,
            self.ui.species_selected_and_total_label,
            self.ui.compartments_selected_and_total_label,
            
            self.ui.timepoints_data_units_combo_box,
            self.ui.timepoints_display_units_combo_box,
            
            self.ui._data_group_box,
#            self.ui.quantities_data_units_combo_box,
#            self.ui.quantities_display_type_combo_box,
##            self.ui.molecules_display_units_label,
#            self.ui.moles_display_units_combo_box,
#            self.ui.concentrations_display_units_combo_box,
            
#            self.ui.volumes_data_units_combo_box,
#            self.ui.volumes_display_units_combo_box,
            self.ui.volumes_widget,
#
#            self.ui.actionsWidget,
        )

        clear_widgets(
#            self.ui.file_name_line_edit,
            self.ui.runs_list_widget,
            self.ui.species_list_widget,
            self.ui.compartments_list_widget,
        )

        self.ui.file_name_line_edit.setText(self._file_name_line_edit_text_orig)

        uncheck_widgets(
            self.ui.select_all_runs_check_box,
            self.ui.select_all_species_check_box,
            self.ui.select_all_compartments_check_box,
        )
                
        disable_widgets(
            self.ui.file_name_line_edit,
            
            self.ui.select_all_runs_check_box,
            self.ui.runs_list_widget,
            self.ui.random_runs_spin_box,
            self.ui.random_runs_label,

            self.ui.select_all_species_check_box,
            self.ui.species_list_widget,
            self.ui.filter_species_line_edit,
#            self.ui.sort_species_check_box,
            
            self.ui.compartments_list_widget,
            self.ui.select_all_compartments_check_box,
            self.ui.filter_compartments_line_edit,
#            self.ui.sort_compartments_check_box,
            
            self.ui.to_spin_box,
            self.ui.from_spin_box,
            self.ui.every_spin_box,
            
            self.ui.average_over_selected_runs_check_box,
            self.ui.calculate_button,
            
            self.ui.export_data_as_button,
            self.ui.plot_timeseries_button,
            self.ui.plot_histogram_button,
            self.ui.visualise_population_button,
        )
        
        self.ui.load_button.setFocus(Qt.OtherFocusReason)

#        self.resize(350,32)
        
        
    def load_succeeded(self):
        ''' Configures, populates, enables, checks and shows relevant widgets. '''

        simulation = self.simulation

        fileinfo = QFileInfo(self.filename)
        self.ui.file_name_line_edit.setText(fileinfo.absoluteFilePath())
        
        from_ = int(0)
        to = int(simulation.max_time)
        interval = simulation.log_interval
        
        self.ui.from_spin_box.setRange(from_, to)
        self.ui.from_spin_box.setValue(from_)
        self.ui.from_spin_box.set_interval(interval)

        self.ui.to_spin_box.setRange(from_, to)
        self.ui.to_spin_box.setValue(to)
        self.ui.to_spin_box.set_interval(interval)

        self.ui.every_spin_box.setRange(1, simulation._runs_list[0].number_of_timepoints)
        self.ui.every_spin_box.setValue(self.ui.every_spin_box.minimum())

        self.ui.log_interval_label.setText(str(interval))

        # list widgets
        clear_widgets(
            self.ui.runs_list_widget,
            self.ui.species_list_widget,
            self.ui.compartments_list_widget,
        )
        for i in simulation._runs_list:
            SimulationListWidgetItem(i, self.ui.runs_list_widget)
        for i in simulation._species_list:
            SimulationListWidgetItem(i, self.ui.species_list_widget)
        for i in simulation._runs_list[0]._compartments_list: #FIXME can't rely on run1 alone if compartments divide
            SimulationListWidgetItem(i, self.ui.compartments_list_widget)

        show_widgets(
#            self.ui._timepoints_group_box,
#            self.ui._runs_group_box,
#            self.ui._species_group_box,
#            self.ui._compartments_group_box,
            self.ui._data_group_box,
        )
        
        # runs
        runs = self.ui.runs_list_widget.count()
        self.ui.random_runs_spin_box.setRange(1, runs)
        if runs == 1:
            self.ui.runs_list_widget.selectAll() # should check select_all_runs_check_box automatically
            hide_widgets(
                self.ui._runs_group_box,
                self.ui.average_over_selected_runs_check_box,
            )
            self.ui.average_over_selected_runs_check_box.setChecked(False) # so we don't do the mean of 1 run
        else: # runs > 1
            show_widgets(
                self.ui._runs_group_box,
                self.ui.average_over_selected_runs_check_box,
            )
            enable_widgets(
                self.ui.select_all_runs_check_box,
                self.ui.runs_list_widget,
                self.ui.random_runs_spin_box,
                self.ui.random_runs_label,
                self.ui.average_over_selected_runs_check_box,
            )
            self.ui.average_over_selected_runs_check_box.setChecked(True) # check average over runs

        # species
        species = self.ui.species_list_widget.count()
        if species == 1:
            self.ui.species_list_widget.selectAll()
        else:
            enable_widgets(self.ui.select_all_species_check_box)


        # compartments
        compartments = self.ui.compartments_list_widget.count()
        if compartments == 1:
            self.ui.compartments_list_widget.selectAll()
        else:
            enable_widgets(self.ui.select_all_compartments_check_box)
        
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
        show_widgets(self.ui.volumes_widget)
        if self.simulation.log_volumes in ('true', 1):
#            self.ui.quantities_display_type_combo_box.insertItem(1, 'concentrations')
            self.volumes_list_widget_item = QListWidgetItem('Volumes', self.ui.species_list_widget)
#            show_widgets(self.ui.volumes_widget)
            hide_widgets(self.ui.volume_spin_box)
            show_widgets(self.ui.in_label)
        else:
#            hide_widgets(self.ui.volumes_widget)
            hide_widgets(self.ui.in_label)
            show_widgets(self.ui.volume_spin_box) #TODO switch on quantities_display_type_combo_box.currrentItem() == 'concentrations'  
        
        enable_widgets(
            self.ui.file_name_line_edit,
            
            self.ui.select_all_species_check_box,
            self.ui.species_list_widget,
            self.ui.filter_species_line_edit,
#            self.ui.sort_species_check_box,
            
            self.ui.compartments_list_widget,
            self.ui.select_all_compartments_check_box,
            self.ui.filter_compartments_line_edit,
#            self.ui.sort_compartments_check_box,
            
            self.ui.to_spin_box,
            self.ui.from_spin_box,
            self.ui.every_spin_box,
            
#            self.ui.average_over_selected_runs_check_box,
#            self.ui.calculate_button,
            
#            self.ui.export_data_as_button,
#            self.ui.plot_timeseries_button,
#            self.ui.plot_histogram_button,
#            self.ui.visualise_population_button,
        )

        show_widgets(
            self.ui.runs_selected_and_total_label,
            self.ui.species_selected_and_total_label,
            self.ui.compartments_selected_and_total_label,
            
            self.ui.timepoints_data_units_combo_box,
            self.ui.timepoints_display_units_combo_box,
            
            self.ui.quantities_data_units_combo_box,
            self.ui.quantities_display_type_combo_box,
#            self.ui.molecules_display_units_label,
#            self.ui.moles_display_units_combo_box,
#            self.ui.concentrations_display_units_combo_box,
            
#            self.ui.volumes_data_units_combo_box,
#            self.ui.volumes_display_units_combo_box,
#            self.ui.volumes_widget,
            self.ui.actionsWidget,
        )

        self.ui.species_list_widget.setFocus(Qt.OtherFocusReason)


    # slots

    def quantities_display_type_changed(self, text):
        if text == 'molecules': #TODO replace with substance_display units?
            hide_widgets(self.ui.concentrations_display_units_combo_box, self.ui.moles_display_units_combo_box)
            show_widgets(self.ui.molecules_display_units_label)
        elif text == 'concentrations':
            hide_widgets(self.ui.molecules_display_units_label, self.ui.moles_display_units_combo_box)
            show_widgets(self.ui.concentrations_display_units_combo_box)
        elif text == 'moles':
            hide_widgets(self.ui.molecules_display_units_label, self.ui.concentrations_display_units_combo_box)
            show_widgets(self.ui.moles_display_units_combo_box)
        

    def update_ui(self):
        '''Called at the end of __init__ and whenever runs/species/compartments
        list_widget's item selection changes in order to disable/enable actions
        '''
        
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
#                self.ui.plot_histogram_button,
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
                disable_widgets(self.ui.plot_histogram_button)
                self.ui.plot_histogram_button.setToolTip("To enable select two or more runs or compartments")
            
            if num_selected_runs > 1:
                enable_widgets(self.ui.calculate_button)

            # no more than 6 surfaces
            if num_selected_species <= 6 and num_selected_compartments >= 4:
                enable_widgets(self.ui.visualise_population_button)
                self.ui.visualise_population_button.setToolTip("Animate species levels as a surface over the lattice")
            else:
                disable_widgets(self.ui.visualise_population_button)
                self.ui.visualise_population_button.setToolTip("To enable select more than 4 compartments and fewer than 7 species")
                
#            #TODO no more than 10 timeseries (per species)
#            if num_selected_compartments > 10:
#                disable_widgets(self.ui.plot_timeseries_button)
#            else:
#                enable_widgets(self.ui.plot_timeseries_button)


    def update_datapoints_label(self):
        num_runs = len(self.ui.runs_list_widget.selectedItems())
        num_species = len(self.ui.species_list_widget.selectedItems())
        num_compartments = len(self.ui.compartments_list_widget.selectedItems())
        volumes = self.volumes_selected()
        mean_over_runs = self.mean_over_runs()
        amounts = True

        # adapted from McssResults.num_timeseries
        numtimeseries = 0
        if num_runs > 1 and mean_over_runs:
            if amounts and volumes:
                numtimeseries = (num_species * num_compartments) + num_compartments
            elif amounts:
                numtimeseries = num_species * num_compartments
            elif volumes:
                numtimeseries = num_compartments
        else:
            if amounts and volumes:
                numtimeseries = (num_runs * num_species * num_compartments) + (num_runs * num_compartments)
            elif amounts:
                numtimeseries = num_runs * num_species * num_compartments
            elif volumes:
                numtimeseries = num_runs * num_compartments

        every = int(self.ui.every_spin_box.value())
        if not every:
            return # avoid divide by zero
        start = int(self.ui.from_spin_box.value() // every)
        stop = int(self.ui.to_spin_box.value() // every) + 1
        
        numtimepoints = (stop - start // every)
        numdatapoints = numtimepoints * numtimeseries

        def convert_bytes(bytes):
            '''Taken from http://www.5dollarwhitebox.org/drupal/node/84'''
            # also http://code.activestate.com/recipes/577081-humanized-representation-of-a-number-of-bytes/
            bytes = float(bytes)
            if bytes >= 1099511627776:
                terabytes = bytes / 1099511627776
                size = '%.2fT' % terabytes
            elif bytes >= 1073741824:
                gigabytes = bytes / 1073741824
                size = '%.2fG' % gigabytes
            elif bytes >= 1048576:
                megabytes = bytes / 1048576
                size = '%.2fM' % megabytes
            elif bytes >= 1024:
                kilobytes = bytes / 1024
                size = '%.2fK' % kilobytes
            else:
                size = '%.2fb' % bytes
            return size

        bytes_per_datapoint = 8 if mcss_results.dtypedefault == np.float64 else 4 # np.float32

        text = ''
        if num_species <= 6 and num_compartments >= 4:

            def xy_min_max():
                x_positions = [c.data.x_position for c in self.ui.compartments_list_widget.selectedItems()]
                y_positions = [c.data.y_position for c in self.ui.compartments_list_widget.selectedItems()]
                return (min(x_positions), max(x_positions)), (min(y_positions), max(y_positions))
            
            numsurfaces = num_species
            (xmin, xmax), (ymin, ymax) = xy_min_max()
            numsurfacedatapoints = int(numsurfaces * ((xmax - xmin) + 1) * ((ymax - ymin) + 1) * numtimepoints) 

#            text += '%s surfaces (<=%s)' % (numsurfaces, numsurfacedatapoints)#convert_bytes(numsurfacedatapoints * bytes_per_datapoint))
            text += '%s surfaces (<=%s)' % (numsurfaces, convert_bytes(numsurfacedatapoints * bytes_per_datapoint))
        if text:
            text += ', '
#        text += '%s timeseries (%s)' % (numtimeseries, numdatapoints)#convert_bytes(numdatapoints * bytes_per_datapoint))
        text += '%s timeseries (%s)' % (numtimeseries, convert_bytes(numdatapoints * bytes_per_datapoint))
        self.ui.datapoints_label.setText(text)
        
        if numdatapoints * bytes_per_datapoint > (1073741824 / 2): # 1/2 gigabyte
            self.ui.datapoints_label.setStyleSheet("QLabel { color : red; }")
        else:
            self.ui.datapoints_label.setStyleSheet("QLabel { color : black; }")

        #TODO show numdatapoints with warning if too high


    def select_random_runs(self, runs):
        list = self.ui.runs_list_widget
        list.clearSelection()
        randoms = set()
        if runs == list.count():
            self.ui.select_all_runs_check_box.setChecked(True)
            return
        while len(randoms) <= runs:
            randoms.add(list.item(randint(0, list.count()))) # I wonder how many false hits this generates
        for i in randoms:
            list.setCurrentItem(i, QItemSelectionModel.Select)


    # accessors
    
    def volumes_selected(self):
        try:
            return True if hasattr(self, 'volumes_list_widget_item') and self.volumes_list_widget_item.isSelected() else False
        except RuntimeError:
            del self.volumes_list_widget_item
            return False
    
    def selected_species(self):
        '''Return selected species after removing volumes.'''
        selected_species = self.ui.species_list_widget.selectedItems()
#        if self.simulation.log_volumes in ('true', 1) and self.volumes_list_widget_item in selected_species:
        if self.volumes_selected():
            selected_species.remove(self.volumes_list_widget_item)
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
        averaging = self.mean_over_runs()
        return from_, to, every, averaging

    def mean_over_runs(self):
        return self.ui.average_over_selected_runs_check_box.isChecked()

    def volume(self):
        return self.ui.volume_spin_box.value()

    def set_units(self, **units):
        flags = Qt.MatchExactly | Qt.MatchCaseSensitive
        for key, value in units.items():
            if key == 'timepoints_data_units':
                index = self.ui.timepoints_data_units_combo_box.findText(value, flags)
                if index != -1:
                    self.ui.timepoints_data_units_combo_box.setCurrentIndex(index)

            if key == 'timepoints_display_units':
                index = self.ui.timepoints_display_units_combo_box.findText(value, flags)
                if index != -1:
                    self.ui.timepoints_display_units_combo_box.setCurrentIndex(index)
            
            if key == 'quantities_data_units':
                index = self.ui.quantities_data_units_combo_box.findText(value, flags)
                if index != -1:
                    self.ui.quantities_data_units_combo_box.setCurrentIndex(index)
            
            if key == 'quantities_display_type':
                index = self.ui.quantities_display_type_combo_box.findText(value, flags)
                if index != -1:
                    self.ui.quantities_display_type_combo_box.setCurrentIndex(index)
                quantities_display_type = value
                if 'quantities_display_units' in units:
                    quantities_display_units = units['quantities_display_units']
                    if quantities_display_type == 'concentrations':
                        index = self.ui.concentrations_display_units_combo_box.findText(quantities_display_units, flags)
                        if index != -1:
                            self.ui.concentrations_display_units_combo_box.setCurrentIndex(index)
                    elif quantities_display_type == 'moles':
                        index = self.ui.moles_display_units_combo_box.findText(quantities_display_units, flags)
                        if index != -1:
                            self.ui.moles_display_units_combo_box.setCurrentIndex(index)
#                    elif quantities_display_type == 'molecules':
#                        pass

            if key == 'volumes_data_units':
                index = self.ui.volumes_data_units_combo_box.findText(value, flags)
                if index != -1:
                    self.ui.volumes_data_units_combo_box.setCurrentIndex(index)
            
            if key == 'volumes_display_units':
                index = self.ui.volumes_display_units_combo_box.findText(value, flags)
                if index != -1:
                    self.ui.volumes_display_units_combo_box.setCurrentIndex(index)

    def units_dict(self):
        '''McssResults(..., **self.units_dict())'''
        units = {}
        units['timepoints_data_units'] = unicode(self.ui.timepoints_data_units_combo_box.currentText())
        units['timepoints_display_units'] = unicode(self.ui.timepoints_display_units_combo_box.currentText())
        units['quantities_data_units'] = unicode(self.ui.quantities_data_units_combo_box.currentText())
        quantities_display_type = unicode(self.ui.quantities_display_type_combo_box.currentText())
        units['quantities_display_type'] = unicode(quantities_display_type)
        if quantities_display_type == 'molecules':
            quantities_display_units = 'molecules'
        elif quantities_display_type == 'concentrations':
            quantities_display_units = unicode(self.ui.concentrations_display_units_combo_box.currentText())
        elif quantities_display_type == 'moles':
            quantities_display_units = unicode(self.ui.moles_display_units_combo_box.currentText())
        units['quantities_display_units'] = unicode(quantities_display_units)
        units['volumes_data_units'] = unicode(self.ui.volumes_data_units_combo_box.currentText())
        units['volumes_display_units'] = unicode(self.ui.volumes_display_units_combo_box.currentText())
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
        from histograms import Histogram
        results = self.selected_items_results()
        units = self.units_dict()
        histogram = Histogram.fromresults(
            results,
            timepoints_display_units=units['timepoints_display_units'],
            quantities_display_units=units['quantities_display_units'],
            bins=10,
        )
        histogram.edit_traits()


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
            self.current_directory,
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
        '''Plot timeseries from selection'''
        results = self.selected_items_results()
        self.timeseries_plot = results.timeseries_plot(
            mean_over_runs=self.mean_over_runs(),
            volumes=self.volumes_selected(),
            **kwargs
        ) 
        
        ui = self.timeseries_plot.edit_traits(kind='live')

        # self._timeseries_plot_uis is used in self.closeEvent to close open windows
        if not hasattr(self, '_timeseries_plots_uis'):
            self._timeseries_plot_uis = [ui]
        else:
            self._timeseries_plot_uis.append(ui)

        widget = ui.control
        
        #TODO works?
        widget.setAttribute(Qt.WA_DeleteOnClose)
        widget.connect(self, SIGNAL("destroyed(QObject*)"), SLOT("close()"))
        
        widget.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
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
    interpolated = np.ndarray((xmax * xymultiplier, ymax * xymultiplier, tmax * tmultiplier))
    numx, numy, numt = (complex(i) for i in interpolated.shape) 
    coords = mgrid[0:xmax - 1:numx, 0:ymax - 1:numy, 0:tmax - 1:numt]
    interpolated = ndimage.map_coordinates(surfacearray, coords, order=1)        
    return interpolated



def main(filename=None):
    # see spatial_splot.test for how to automate selections, etc
    
    argv = sys.argv#qApp.arguments()
    
    if filename is not None:
        self = McssResultsWidget(filename=filename)
    else:
        if len(argv) > 2:
            print 'usage: python mcss_results_widget.py {h5file}'#TODO mcss-results {h5file}'
            sys.exit(2)
        if len(argv) == 1:
            self = McssResultsWidget()
        elif len(argv) == 2:
            filename = argv[1]
            self = McssResultsWidget(filename)
    centre_window(self)
    self.show()
    if not self.loaded:
        self.load()
#        self.loaded = self.load()


    self.raise_()
    qApp.processEvents()
    
#    return self
    exit(qApp.exec_())


if __name__ == "__main__":
    main()
#    exit(qApp.exec_())
