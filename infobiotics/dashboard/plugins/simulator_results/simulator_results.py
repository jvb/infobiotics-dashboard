#from PlotsListWidget import PlotsListWidget
from PyQt4.QtCore import QSettings, QVariant, QDir, QSettings, QObject, QString, \
    QSize, QFileInfo, SIGNAL, SLOT, QTimer, Qt
from PyQt4.QtGui import QWidget, QApplication, QHBoxLayout, QVBoxLayout, QWidget, \
    QHBoxLayout, QVBoxLayout, QListWidget, QListWidgetItem, QItemSelectionModel, \
    QPushButton, QBrush, QColor, QFileDialog, QMessageBox, QSpinBox, QPixmap, \
    QSizePolicy, QAbstractItemView, QListView, QIcon, QDoubleSpinBox, qApp, \
    QGridLayout, QLabel, QSlider, qApp, \
    QApplication # must use qApp not QApplication(sys.argv) when mixing with TraitsUI
from enthought.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'qt4'
from enthought.mayavi.core.pipeline_base import PipelineBase
from enthought.mayavi.core.ui.mayavi_scene import MayaviScene
from enthought.mayavi.tools.mlab_scene_model import MlabSceneModel
from enthought.traits.api import HasTraits, Instance, Str, Button, Instance, \
    HasTraits, Range, on_trait_change, String, Bool
from enthought.traits.ui.api import View, Item, HGroup, View, VGroup, Spring
from enthought.tvtk.pyface.scene_editor import SceneEditor
from infobiotics.commons import colours
from infobiotics.commons.matplotlib.matplotlib_figure_size import resize_and_save_matplotlib_figure
from infobiotics.commons.qt4 import centre_window, disable_widgets, enable_widgets, hide_widgets, show_widgets, uncheck_widgets, check_widgets, clear_widgets
from infobiotics.commons.traits.ui.qt4.matplotlib_figure_editor import \
    MatplotlibFigureEditor
from matplotlib import font_manager
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from random import randint
from ui_player_control_widget import Ui_ControlsWidget
from ui_plots_preview_dialog import Ui_PlotsPreviewDialog
from ui_simulation_results_dialog import Ui_SimulationResultsDialog
import bisect
import cStringIO as StringIO
import decimal
import infobiotics
import math
import numpy as np
import os
import tables
import xlwt


# for QSettings
if qApp is None:
    import sys
    app = QApplication(sys.argv)
qApp.setOrganizationDomain('www.infobiotics.org')
qApp.setOrganizationName('Infobiotics')
qApp.setApplicationName('Infobiotics Dashboard')
qApp.setApplicationVersion(infobiotics.version)


def load_h5(h5_file):
    """Read mcss-produced hdf5 file, creating objects for datasets, exposing 
       attributes as properties and objects as public variables.
       AttributeErrors should be caught by the loading class."""

    h5 = tables.openFile(h5_file) # get file handle

    simulation = Simulation(h5.root._v_attrs) # create simulation objects

    # rule objects in Simulation._rules_list
    # ruleset objects Simulation._ruleset_list
    # propensities in Simulation._propensities_list
    # reactions in Simulation._reactions_list
    
    # volumes to be done in SimulationResultsDialog
    
    # positions not used yet

    if simulation.log_type.lower() != 'levels':
        return # give up

    # when reading from disk to memory taking the whole slice of each column is very fast
    species_indices = h5.root.species_information.cols.species_index[:]
    species_names = h5.root.species_information.cols.species_name[:]
    simulation._species_list = [
        Species(
            species_indices[i],
            species_names[i],
            simulation,
        ) for i in range(simulation.number_of_species)
    ]

    # create run objects and compartment objects within runs
    for i in range(1, int(simulation.number_of_runs) + 1):
        try:
            node = h5.root._f_getChild('run%s' % i)
            run = Run(node._v_attrs, i, simulation)
        except tables.exceptions.NoSuchNodeError, error:
            # Couldn't find run i, so overwrite number_of_runs with i - 1
            h5.close()
            h5 = tables.openFile(h5_file, 'r+')
            h5.root._v_attrs.number_of_runs = i - 1
            simulation.number_of_runs = h5.root._v_attrs.number_of_runs
            break

        # just create compartments once on the first run #TODO maybe change this when dealing with volumes 
        if i == 1:
            cols = node.compartment_information.cols # table columns accessor
            compartment_indices = cols.compartment_index[:]
            compartment_ids = cols.compartment_id[:]
            compartment_names = cols.compartment_name[:]
            compartment_x_positions = cols.compartment_x_position[:]
            compartment_y_positions = cols.compartment_y_position[:]
#            compartment_z_positions = cols.compartment_z_position[:] # not written
            compartment_template_indices = cols.compartment_template_index[:]
#            compartment_creation_time = cols.compartment_creation_time[:] # not used
#            compartment_destruction_time = cols.compartment_destruction_time[:] # not used

            compartments_list = [ # doesn't need to be global
                Compartment(
                    compartment_indices[i],
                    compartment_ids[i],
                    compartment_names[i],
                    compartment_x_positions[i],
                    compartment_y_positions[i],
#                    compartment_z_positions[i], # not written
                    compartment_template_indices[i],
#                    compartment_creation_time[i], # not used
#                    compartment_destruction_time[i], # not used
                    run,
                    run._simulation,
                ) for i in range(0, len(compartment_indices))
            ]
        run._compartments_list = compartments_list

        simulation._runs_list.append(run)

    h5.close()
    return simulation


class Simulation(object):
    """An mcss simulation dataset as a Python object."""

    def __init__(self, attributes):
#        self._propensities_list = []
#        self._reactions_list = []
#        self._rules_list = []
#        self._rulesets_list = []
        self._runs_list = []
        self._species_list = []

#        for key, value in attributes.iteritems():
#            setattr(self, key, value)
        self.data_file = attributes.data_file
#        self.division_direction = attributes.division_direction
#        self.duplicate_initial_amounts = attributes.duplicate_initial_amounts
#        self.growth_type = attributes.growth_type
#        self.keep_divisions = attributes.keep_divisions
#        self.lattice_x_dimension = attributes.lattice_x_dimension
#        self.lattice_y_dimension = attributes.lattice_y_dimension
#        self.lattice_z_dimension = attributes.lattice_z_dimension
#        self.log_degraded = attributes.log_degraded
        self.log_interval = attributes.log_interval
#        self.log_propensities = attributes.log_propensities
        self.log_type = attributes.log_type
        self.log_volumes = attributes.log_volumes
        self.max_time = attributes.max_time
#        self.mcss_version = attributes.mcss_version
#        self.model_format = attributes.model_format
        self.model_input_file = attributes.model_input_file
#        self.number_of_rule_templates = attributes.number_of_rule_templates
#        self.number_of_rules_in_templates = attributes.number_of_rules_in_templates
        self.number_of_runs = attributes.number_of_runs
        self.number_of_species = attributes.number_of_species
#        self.periodic_x = attributes.periodic_x
#        self.periodic_y = attributes.periodic_y
#        self.periodic_z = attributes.periodic_z
#        self.seed = attributes.seed
#        self.simulation_algorithm = attributes.simulation_algorithm
#        self.simulation_algorithm_name = attributes.simulation_algorithm_name
#        self.simulation_end_time = attributes.simulation_end_time
        self.simulation_start_time = attributes.simulation_start_time
#        self.total_number_of_rules = attributes.total_number_of_rules


class Run(object):
    """An mcss run dataset as a Python object."""

    def __init__(self, attributes, run_number, simulation):
        self._run_number = run_number
        self._simulation = simulation
        self._compartments_list = []
#        self.main_loop_end_time = attributes.main_loop_end_time
#        self.main_loop_start_time = attributes.main_loop_start_time
        self.number_of_compartments = attributes.number_of_compartments
        self.number_of_timepoints = attributes.number_of_timepoints
#        self.preprocess_end_time = attributes.preprocess_end_time
#        self.preprocess_start_time = attributes.preprocess_start_time
#        self.run_end_time = attributes.run_end_time
#        self.run_start_time = attributes.run_start_time
        self.simulated_time = attributes.simulated_time
#        self.total_reactions_simulated = attributes.total_reactions_simulated


class Species(object):
    """An mcss species dataset as a Python object."""

    def __init__(self, index, name, simulation):
        self.index = index
        self.name = name
        self._simulation = simulation


class Compartment(object):
    """An mcss compartment dataset as a Python object."""

#    def __init__(self, index, id, name, x_position, y_position, template_index, creation_time, destruction_time, run, simulation):
    def __init__(self, index, id, name, x_position, y_position, template_index, run, simulation):
#        z_position, 
        self.run = run
        self._simulation = simulation
        self.index = index
        self.id = id
        self.name = name
        self.x_position = x_position
        self.y_position = y_position
#        self.z_position = z_position
        self.template_index = template_index
#        self.creation_time = creation_time
#        self.destruction = destruction_time        

    def coordinates(self):
        return (self.x_position, self.y_position)

    def compartment_name_and_xy_coords(self):
        return "%s (%s,%s)" % (self.name, self.x_position, self.y_position)


class SimulationListWidgetItem(QListWidgetItem):

    def __init__(self, data, parent=None):
        self.data = data

        if isinstance(data, Species):
            text = data.name
            self.amounts_index = data.index
            
        elif isinstance(data, Compartment):
            text = data.compartment_name_and_xy_coords() #TODO fudge
            self.amounts_index = data.index

        elif isinstance(data, Run):
            text = "%s" % (data._run_number)
            self.amounts_index = data._run_number - 1
            # recolour item if run is truncated #TODO useful?
#            if data._run_number == data._simulation_number_of_runs: # last run only
            if data.simulated_time < data._simulation.max_time:
                brush = self.foreground()
                brush.setColor(Qt.red)
                self.setForeground(brush)
                self.setToolTip('Run truncated at %s' % data.simulated_time)

        elif isinstance(data, Simulation):
            text = "%s %s" % (data.model_input_file, data.simulation_start_time)
            self.amounts_index = None

        else:
            raise TypeError("type of data is not recognised")

        QListWidgetItem.__init__(self, text, parent, QListWidgetItem.UserType)
        
        if isinstance(self.amounts_index, int):
            self.setToolTip('%d' % self.amounts_index)


class SimulationResultsDialog(QWidget):
    """Extract and plot data from mcss (version > 0.0.19) simulations"""

    def __init__(self, filename=None):
        """Setup widgets, connect signals to slots and attempt load."""
        self.settings_group = "SimulationResultsDialog"
        QWidget.__init__(self) # initialize base class

        self.ui = Ui_SimulationResultsDialog()
        self.ui.setupUi(self)

        self.ui.compartments_list_widget.setToolTip('')

        self.connect(self.ui.load_button, SIGNAL("clicked()"), self.load)

        self.ui.runs_list_widget.connect_all_selected_check_box(self.ui.select_all_runs_check_box)
        self.ui.species_list_widget.connect_all_selected_check_box(self.ui.select_all_species_check_box)
        self.ui.compartments_list_widget.connect_all_selected_check_box(self.ui.select_all_compartments_check_box)

#        self.ui.species_list_widget.connect_sort_check_box(self.ui.sort_species_check_box)
#        self.ui.compartments_list_widget.connect_sort_check_box(self.ui.sort_compartments_check_box)

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
        #TODO load options
        settings.endGroup()

    def save_settings(self):
        settings = QSettings()
        settings.beginGroup(self.settings_group)
        settings.setValue("current_directory", QVariant(unicode(self.current_directory)))
        #TODO save options
        settings.endGroup()

    def load(self, filename=None):
        if filename is None:
            filename = QFileDialog.getOpenFileName(self,
                                                   self.tr("Open HDF5 simulation data file"),
                                                   self.current_directory,
                                                   self.tr("HDF5 data files (*.h5 *.hdf5);;All files (*)"))
            if filename == QString(""):
                if self.loaded:
                    return
                else:
                    self.load_failed()
                    return False

        self.current_directory = QFileInfo(filename).absolutePath()
        filename = unicode(filename) # must convert QString into unicode
        simulation = None
        try:
            simulation = load_h5(filename)
        except IOError, e:
            QMessageBox.warning(self, "Error", "There was an error reading %s\n%s" % (filename, QString(unicode(e))))
        except AttributeError, e:
            e = QString(unicode(e) + u"\nDid you use a old version of mcss? (<0.0.19)")
            QMessageBox.warning(self, "Error", "There was an error reading %s\n%s" % (filename, e))
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
            
            ui.quantities_data_units_combo_box,
            ui.quantities_display_type_combo_box,
            ui.molecules_display_units_label,
            ui.moles_display_units_combo_box,
            ui.concentrations_display_units_combo_box,
            
#            ui.volumes_data_units_combo_box,
#            ui.volumes_display_units_combo_box,
            ui.volumes_widget,
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
        if text == 'molecules':
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
        ui.every_spin_box.setValue(ui.every_spin_box.minimum()) #TODO make this so if gives roughly one-thousand timepoints

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


        # volumes
        
        i = self.ui.quantities_display_type_combo_box.findText('concentrations')
        if i != -1:
            self.ui.quantities_display_type_combo_box.removeItem(i)
        if self.simulation.log_volumes == 1:
            self.ui.quantities_display_type_combo_box.insertItem(1, 'concentrations')
            QListWidgetItem('Volumes', ui.species_list_widget)
            show_widgets(ui.volumes_widget)
        else:
            hide_widgets(ui.volumes_widget)            
        
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
            if num_selected_runs == 1 and num_selected_species >= 1 and num_selected_compartments > 1:
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
        if self.volumes_list_widget_item in selected_species:
            selected_species.remove(self.volumes_list_widget_item)
            self.volumes_selected = True
        else:
            self.volumes_selected = False
        return selected_species
    
    # compound accessors

    def selected_items(self):
        ''' Usage: 
            runs, species, compartments = selected_items() 
        '''
        runs = self.ui.runs_list_widget.selectedItems()
        species = self.selected_species()
        compartments = self.ui.compartments_list_widget.selectedItems()
        return runs, species, compartments

    def selected_items_amount_indices(self):
        ''' Usage: 
            run_indices, species_indices, compartment_indices = self.selected_items_amount_indices() 
            
        Use for ri, r in enumerate(run_indices): for selected results 
        '''
        runs, species, compartments = self.selected_items()
        run_indices = [item.amounts_index for item in runs]
        species_indices = [item.amounts_index for item in species]
        compartment_indices = [item.amounts_index for item in compartments]
        return run_indices, species_indices, compartment_indices

    def options(self):
        ''' Usage: 
            from_, to, every, averaging = self.options() 
        '''
        from_ = self.ui.from_spin_box.value()
        to = self.ui.to_spin_box.value()
        every = self.ui.every_spin_box.value()
        averaging = self.ui.average_over_selected_runs_check_box.isChecked()
        return from_, to, every, averaging

    def selected_items_results(self, type=float):
        ''' Usage:
            results = self.selected_items_results()
        '''
        run_indices, species_indices, compartment_indices = self.selected_items_amount_indices()
        from_, to, every, _ = self.options()
        return SimulatorResults(
            filename=self.filename,
            simulation=self.simulation,
            type=type,
            beginning=from_,
            end=to,
            every=every,
            run_indices=run_indices,
            species_indices=species_indices,
            compartment_indices=compartment_indices,
            parent=self,
            #TODO pass in units here, with sensible defaults 
        )


    # actions slots

    def histogram(self):
        raise NotImplementedError


    # remember these within this instance
    csv_precision = 3
    csv_delimiter = ','

    from infobiotics.commons.qt4 import wait_cursor
    @wait_cursor
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
            http://stackoverflow.com/questions/1414304/local-functions-in-python/1414320#1414320
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
            timepoints, results = results.get_amounts()
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
                from enthought.traits.api import HasTraits, Range, String
                from enthought.traits.ui.api import View, VGroup, HGroup
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
            ''' https://secure.simplistix.co.uk/svn/xlwt/trunk/README.html '''
            wb = xlwt.Workbook()
            try:
                ws = wb.add_sheet(os.path.basename(self.simulation.model_input_file)[:31])
            except:
                ws = wb.add_sheet('SimulatorResults')
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
            # convert QString to str
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


    @wait_cursor
    def surfacePlot(self):
        results = self.selected_items_results()
        timepoints, results, xmin, xmax, ymin, ymax = results.get_surfaces()
        if len(results) == 0:
            return
        surfaces = []
        species = self.selected_species()
        for si, s in enumerate(species):
            surface = results[si]
            zmax = np.max(surface)
#            if zmax == 0: print "%s never amounts to anything." % s.name
            extent = [xmin, xmax, ymin, ymax, 0, zmax]
#            warp_scale = 'auto' # doesn't work
            warp_scale = (1 / zmax) * 10 #FIXME 10 is magic number
            surface = Surface(surface, warp_scale, extent, s.text(), timepoints)
            surfaces.append(surface)
        self.spatial_plots_window = SpatialPlotsWindow(surfaces, self)
        self.spatial_plots_window.show()


    @wait_cursor
    def plot(self):
        '''Plot selected data. '''

        runs, species, compartments = self.selected_items()
#        run_indices, species_indices, compartment_indices = self.selected_items_amount_indices()
        _, _, _, averaging = self.options()
        results = self.selected_items_results()

        if averaging:
            timepoints, amounts = results.get_amounts_mean_over_runs()
            mean_index = 0
#            if self.volumes_selected:
#                timepoints, volumes = results.get_volumes_mean_over_runs() #TODO
        else:
            timepoints, amounts = results.get_amounts()
            if self.volumes_selected:
                timepoints, volumes = results.get_volumes()
        if len(amounts) == 0 and (self.volumes_selected and len(volumes) == 0):
            return

        plots = []
        if averaging:
            for ci, c in enumerate(compartments):
                for si, s in enumerate(species):
                    plot = Plot(
                        timepoints=timepoints,
                        levels=amounts[mean_index][si, ci],
#                        yerr=errors[si,ci],
                        species=s.data,
                        compartment=c.data,
                        colour=colours.colour(si),
                    )
                    plots.append(plot)

        else:
            for ri, r in enumerate(runs):
                for ci, c in enumerate(compartments):
                    for si, s in enumerate(species):
                        colour = colours.colour(si)
                        plot = Plot(
                            timepoints=timepoints,
                            levels=amounts[ri][si, ci, :],
                            run=r.data,
                            species=s.data,
                            compartment=c.data,
                            colour=colour,
                        )
                        plots.append(plot)
                    if self.volumes_selected:
                        colour = colours.colour(len(species) + 1)
                        plot = VolumePlot(
                            timepoints=timepoints,
                            levels=volumes[ri][ci, :],
                            run=r.data,
                            compartment=c.data,
                            colour=colour,
                        )
                        plots.append(plot)

        if len(plots) > 0:
            self.plotsPreviewDialog = PlotsPreviewDialog(
                runs=len(runs),
                averaging=averaging,
                windowTitle=os.path.basename(self.simulation.model_input_file),
            )
            if self.plotsPreviewDialog.addPlots(plots):
    #            if len(plots) > 8:
    #                self.plotsPreviewDialog.showMaximized()
    #            else:
                centre_window(self.plotsPreviewDialog)
                self.plotsPreviewDialog.show()
                # bring to fore (needed in this order)
                self.plotsPreviewDialog.raise_()
                self.plotsPreviewDialog.activateWindow()
                return self.plotsPreviewDialog
            else:
                self.plotsPreviewDialog.combine()
                self.plotsPreviewDialog.close()

#        # deprecated because Jamie's Ctrl-C signal handling fixes it. But what about crashes?        
#        try:
#            # all of the above
#        except ZeroDivisionError, e:
#            QMessageBox.warning(self, QString(u"Error"),
#                                QString(u'There was a problem processing the simulation data.\n%s\nMaybe the simulation was aborted.\nTry rerunning the simulation and letting it finish.' % e))
#        finally:
#            # reset mouse pointer
#            self.setCursor(Qt.ArrowCursor)


class Plot(object): #rename to timeseries
    def __init__(self, timepoints, levels, colour, species, compartment, run=None, yerr=None, width=5, height=5, dpi=100):
        '''
        
        run == None when averaging over runs
        
        '''
        self.figure = Figure(figsize=(width, height), dpi=dpi)
        self.canvas = FigureCanvasAgg(self.figure) #TODO remove?
        self.timepoints = timepoints
        self.levels = levels
        self.yerr = yerr
        self.run = run
        self.colour = colour
        self.species = species
        self.compartment = compartment
        self.setup()

    def setup(self):
        #self.axes.hold(False) clear every time plot() is called
        self.axes = self.figure.add_subplot(111)
        self.axes.plot(self.timepoints, self.levels, color=self.colour, label=self.label)
        self.axes.set_xlabel('time')# %s' % self.units)
        self.axes.set_ylabel('molecules')
        self.axes.set_title(self.label)
        #self.axes.legend()

    def get_label(self):
        compartment_name_and_xy_coords = self.compartment.compartment_name_and_xy_coords()
        if self.run == None:
            return "%s in %s" % (self.species.name, compartment_name_and_xy_coords)
        else:
            return "%s in %s of run %s" % (self.species.name, compartment_name_and_xy_coords, self.run._run_number)

    label = property(get_label)

#    def least(self):
#        return np.min(self.levels)
#
#    def most(self):
#        return np.max(self.levels)
#
#    def invariant(self):
#        return (True if self.least() == self.most() else False)
#
#    def zeros(self):
#        return (True if self.least() == 0 and self.most() == 0 else False)

    def pixmap(self):
        fileLikeObject = StringIO.StringIO()
        self.png(fileLikeObject)
        pixmap = QPixmap()
        succeeded = pixmap.loadFromData(fileLikeObject.getvalue(), "PNG")
        fileLikeObject.close()
        if succeeded:
            return pixmap
        else:
            return None

    def png(self, filename, dpi=100):
        self.figure.savefig(filename, format='png')

    def eps(self, filename, dpi=300):
        #TODO do something with dpi
        self.figure.savefig(filename, format='eps')


class VolumePlot(Plot):
    def __init__(self, timepoints, levels, colour, compartment, run=None, yerr=None, width=5, height=5, dpi=100):
        class Species(object):
            def __init__(self, name):
                self.name = name
        super(VolumePlot, self).__init__(timepoints, levels, colour, Species(name='Volumes'), compartment, run, yerr, width, height, dpi)
        
    def setup(self):
        self.axes = self.figure.add_subplot(111)
        self.axes.plot(self.timepoints, self.levels, color=self.colour, label=self.label)
        self.axes.set_xlabel('Time')
        self.axes.set_ylabel('Volume')
        self.axes.set_title(self.label)
        
    def get_label(self):
        compartment_name_and_xy_coords = self.compartment.compartment_name_and_xy_coords()
        if self.run == None:
            return "Volume of %s" % compartment_name_and_xy_coords
        else:
            return "Volume of %s in run %s" % (compartment_name_and_xy_coords, self.run._run_number)
    
    label = property(get_label)        
        

# adapted from Pawel's tiling code
def arrange(number):
    """ Returns the smallest rows x columns tuple for a given number of items. """
    rows = math.sqrt(number / math.sqrt(2))
    cols = rows * math.sqrt(2)
    # finds lowest integer combination of rows and columns, thanks Pawel 
    if number <= math.ceil(rows) * math.floor(cols):
        rows = int(math.ceil(rows))
        cols = int(math.floor(cols))
    elif number <= math.floor(rows) * math.ceil(cols):
        rows = int(math.floor(rows))
        cols = int(math.ceil(cols))
    else:
        rows = int(math.ceil(rows))
        cols = int(math.ceil(cols))
    return (rows, cols)


from enthought.traits.api import Bool

class TraitsPlot(HasTraits):
    figure = Instance(Figure, ())
    title = Str('title')
    show_individual_legends = Bool
    show_figure_legend = Bool

    def _show_figure_legend_changed(self, value):
        if value:
            pass#self.figure.legend()
        else:
            self.figure.legend_ = None

    def traits_view(self):
        return View(
            VGroup(
                Item('figure',
                    show_label=False,
                    editor=MatplotlibFigureEditor(
                        toolbar=True
                    ),
                ),
                HGroup(
                    'show_individual_legends',
                    'show_figure_legend',
                    Spring(),
                    Item('save_resized', show_label=False),
                ),
                show_border=True,
            ),
            width=640, height=480,
            resizable=True,
            title=self.title
        )

    save_resized = Button
    def _save_resized_fired(self):
        resize_and_save_matplotlib_figure(self.figure)


class PlotsPreviewDialog(QWidget):

    def __init__(self, runs=1, averaging=False, windowTitle=None, parent=None):
        if parent != None:
            QObject.setParent(self, parent)
        QWidget.__init__(self)
        self._runs_list = runs
        self.averaging = averaging
        self.fontManager = font_manager.FontProperties(size='medium')#'small')
        self.windowTitle = windowTitle
        self.ui = Ui_PlotsPreviewDialog()
        self.ui.setupUi(self)
        self.connect(self.ui.combineButton, SIGNAL("clicked()"), self.combine)
        self.connect(self.ui.stackButton, SIGNAL("clicked()"), self.stack)
        self.connect(self.ui.tileButton, SIGNAL("clicked()"), self.tile)
        self.connect(self.ui.plotsListWidget, SIGNAL("itemSelectionChanged()"), self.update_ui)
        self.update_ui()
#        self.traits_plot_list = [] #TODO remove

    def update_ui(self):
        # disable buttons and create handle lists
        self.items = self.ui.plotsListWidget.selectedItems()
        if len(self.items) == 0:
            self.ui.combineButton.setEnabled(False)
            self.ui.stackButton.setEnabled(False)
            self.ui.tileButton.setEnabled(False)
        else:
            self.ui.combineButton.setEnabled(True) #TODO singles?
            self.ui.stackButton.setEnabled(True)
            self.ui.tileButton.setEnabled(True)
        # lists of handles for figurelegend()
        self.lines = []
        self.errorbars = []

    def addPlots(self, plots):
        self.ui.plotsListWidget.addPlots(plots)
        # select lone plot
        if self.ui.plotsListWidget.count() == 1:
            self.ui.plotsListWidget.selectAll()
            return False
        else:
            self.ui.plotsListWidget.clearSelection()
            return True

    def reset(self):
#        pyplot.close()
        self.traits_plot = TraitsPlot()
#        self.traits_plot_list.append(self.traits_plot) #FIXME keeping a reference seems to cause a Qt crash, but not keeping it will lead to GC, wtf?
#        print self.traits_plot_list #TODO remove and above
        self.figure = self.traits_plot.figure
#        self.axes = None
        self.no_labels = False
        self.labels_and_title()

    def labels_and_title(self):
        species = [item.plot.species for item in self.items]
        compartments = [item.plot.compartment for item in self.items]
        single_species = True if len(set(species)) == 1 else False
        single_compartment = True if len(set(compartments)) == 1 else False
        # check if only 1 species
        single_run = True if self._runs_list == 1 else False
        title = ""
        if single_run:
            if single_species:
                # check if only 1 compartment
                if single_compartment:
                    title = "%s in %s (1 run)" % (item.plot.species.name, item.plot.compartment.compartment_name_and_xy_coords())
                    for item in self.items:
                        item.label = None
                        self.no_labels = True
                else:
                    title = "%s (1 run)" % (item.plot.species.name)
                    for item in self.items:
                        item.label = item.plot.compartment.compartment_name_and_xy_coords()
            else:
                if single_compartment:
                    title = "%s (1 run)" % (item.plot.compartment.compartment_name_and_xy_coords())
                    for item in self.items:
                        item.label = item.plot.species.name
                else:
                    title = "1 run"
                    for item in self.items:
                        item.label = "%s in %s" % (item.plot.species.name, item.plot.compartment.compartment_name_and_xy_coords())
        else:
            if self.averaging:
                if single_species:
                    if single_compartment:
                        title = "%s in %s (mean of %s runs)" % (item.plot.species.name, item.plot.compartment.compartment_name_and_xy_coords(), self._runs_list)
                        for item in self.items:
                            item.label = None
                            self.no_labels = True
                    else:
                        title = "%s (mean of %s runs)" % (item.plot.species.name, self._runs_list)
                        for item in self.items:
                            item.label = "%s" % (item.plot.compartment.compartment_name_and_xy_coords())
                else:
                    if single_compartment:
                        title = "%s (mean of %s runs)" % (item.plot.compartment.compartment_name_and_xy_coords(), self._runs_list)
                        for item in self.items:
                            item.label = "%s" % (item.plot.species.name)
                    else:
                        title = "Mean of %s runs" % (self._runs_list)
                        for item in self.items:
                            item.label = "%s in %s" % (item.plot.species.name, item.plot.compartment.compartment_name_and_xy_coords())
            else:
                if single_species:
                    if single_compartment:
                        title = "%s in %s  (%s runs)" % (item.plot.species.name, item.plot.compartment.compartment_name_and_xy_coords(), self._runs_list)
                        for item in self.items:
                            item.label = "Run %s" % item.plot.run._run_number
                    else:
                        title = "%s (%s runs)" % (item.plot.species.name, self._runs_list)
                        for item in self.items:
                            item.label = "%s (run %s)" % (item.plot.compartment.compartment_name_and_xy_coords(), item.plot.run._run_number)
                else:
                    if single_compartment:
                        title = "%s (%s runs)" % (item.plot.compartment.compartment_name_and_xy_coords(), self._runs_list)
                        for item in self.items:
                            item.label = "%s (run %s)" % (item.plot.species.name, item.plot.run._run_number)
                    else:
                        title = "%s runs" % (self._runs_list)
                        for item in self.items:
                            item.label = "%s in %s (run %s)" % (item.plot.species.name, item.plot.compartment.compartment_name_and_xy_coords(), item.plot.run._run_number)
        # set main title
#        pyplot.suptitle(title)
        self.figure.suptitle(title)        


    def combine(self):
        """different colours for all lines"""
        self.reset()

        # determine if some volumes but not (no volumes or all volumes)
        volumes = 0
        for item in self.items:
            if item.plot.species.name == 'Volumes':
                volumes += 1
        if 0 < volumes < len(self.items):
            some_volumes = True
        else:
            some_volumes = False

        if not some_volumes: # either all volumes or no volumes
            # plot all on 1st y-axis
            for i, item in enumerate(self.items):
#                pyplot.xlabel("time (%s)" % item.plot.units)
#                pyplot.ylabel("molecules")
                self.axes = self.figure.add_subplot(111) #FIXME move this out of loop?
                self.axes.set_xlabel("time")# (%s)" % item.plot.units)
                self.axes.set_ylabel("molecules") #TODO concentration
                colour = colours.colour(i)
                self.line(self.axes, item, colour)
                if self.averaging:
                    self.errorbar(item, colour)
        else:
            # mix, plot species on 1st y-axis and volumes on 2nd y-axis
            not_volumes = [item for item in self.items if item.plot.species.name != 'Volumes']
            volumes = [item for item in self.items if item.plot.species.name == 'Volumes']
            self.axes = self.figure.add_subplot(111)
            self.axes.set_xlabel("time")# (%s)" % item.plot.units)
            self.axes.set_ylabel("molecules")
            for i, item in enumerate(not_volumes):
#                pyplot.xlabel("time (%s)" % item.plot.units)
#                pyplot.ylabel("molecules")
                colour = colours.colour(i)
                self.line(self.axes, item, colour)
                if self.averaging:
                    self.errorbar(item, colour)
            axes = self.axes.twinx()
            for i, item in enumerate(volumes):
                i += len(not_volumes)
#                axes.set_xlabel("time")# (%s)" % item.plot.units)
                axes.set_ylabel("Volumes")
                colour = colours.colour(i)
                self.line(axes, item, colour)
                if self.averaging:
                    self.errorbar(item, colour)
            
        if not self.no_labels: self.legend() #TODO

        self.finalise()


    def stack(self):
        """same colour for each species (legend), _compartments_list title"""
        self.reset()
        rows = len(self.items)
        cols = 1
        for i, item in enumerate(self.items):
            if i == 0:
                self.sharedAxis = self.figure.add_subplot(rows, cols, rows - i)
                self.axes = self.sharedAxis
                self.sharedAxis.set_xlabel("time")# (%s)" % item.plot.units)
                self.line(self.axes, item)
                if self.averaging:
                    self.errorbar(item)
            else:
                self.axes = self.figure.add_subplot(rows, cols, rows - i, sharex=self.sharedAxis)
#                pyplot.setp(self.axes.get_xticklabels(), visible=False) #TODO
                self.line(self.axes, item)
                if self.averaging:
                    self.errorbar(item)
            if len(self.items) < 6: #TODO 6 is a bit arbitary  
                self.axes.set_ylabel("molecules") #TODO change for volumes/concentration
            
            if not self.no_labels: self.legend() #TODO
        
        self.finalise()


    def tile(self):
        """same colours for each species (legend), _compartments_list title"""
        self.reset()
        rows, cols = arrange(len(self.items))
        for i, item in enumerate(self.items):
            self.axes = self.figure.add_subplot(rows, cols, i + 1)
            self.axes.set_xlabel("time")# (%s)" % item.plot.units)
            self.axes.set_ylabel("molecules")
            self.line(self.axes, item)
            if self.averaging:
                self.errorbar(item)

            if not self.no_labels: self.legend() #TODO
        
        self.finalise()

    def line(self, axes, item, colour=None):
        lines = axes.plot(
            item.plot.timepoints,
            item.plot.levels,
            label=item.label,
            color=colour if colour is not None else item.plot.colour,
        )
        self.lines.append((lines[0], item.label))

    def errorbar(self, item, colour=None):
        return #TODO
#        step = int(len(timepoints) / 10)
#        errorbar = pyplot.errorbar( #TODO
#            item.plot.timepoints[::step], 
#            item.plot.levels[::step],
#            yerr=item.plot.yerr[::step],
#            label=None,#item.plot.label
#            color=colour if colour is not None else item.plot.colour,
#            fmt=None, 
#            linestyle=None, 
#            capsize=0
#        )
#        self.errorbars.append(errorbar)

    def legend(self):
#        self.axes.legend(loc=0, prop=self.fontManager)
        pass
#        from infobiotics.commons.matplotlib.draggable_legend import DraggableLegend
##        legend = DraggableLegend(ax.legend())
#        legend = self.axes.legend(loc=0, prop=self.fontManager)
#        print self.traits_plot.figure.canvas
#        legend.canvas = self.traits_plot.figure.canvas
#        DraggableLegend(legend) # fails because legend.figure.canvas is None
        

    def figurelegend(self): #FIXME use this
        """Create a legend for all subplots."""
        lines = [line for line, label in self.lines]
        labels = [label for line, label in self.lines]
        legend = self.figure.legend(lines, labels, loc='right', prop=self.fontManager)
#        legend.draggable(True) #TODO test for new matplotlib version before setting

    def background(self):
        """Change figure background."""
#        pyplot.gcf().set_facecolor("whitesmoke")
        self.figure.set_facecolor("whitesmoke")

    def finalise(self):

        self.figurelegend()

        self.lines = []
        self.errorbars = []

        self.background()

        if self.windowTitle is not None:
            self.traits_plot.title = self.windowTitle

        # http://www.mail-archive.com/pyqt@riverbankcomputing.com/msg16645.html
        from PyQt4.QtCore import QAbstractEventDispatcher 
        if QAbstractEventDispatcher.instance() != 0:
            self.traits_plot.edit_traits()
        else:
            self.traits_plot.configure_traits()
            
            
class SimulatorResults(object):
    """Shared initialisation for all concrete SimulatorResults classes."""
    def __init__(self,
        filename,
        simulation,
        beginning=0,
        end= -1,
        every=1,
        chunk_size=2 ** 20,
        type=float, #decimal.Decimal
        species_indices=None,
        compartment_indices=None,
        run_indices=None,
        parent=None):
        """Check arguments and create variables to be used in calculate()."""
        self.parent = parent
        self.type = type
        if simulation is None:
            self.simulation = load_h5(filename)
        else:
            self.simulation = simulation#load_h5(filename) # why do all that object creation again?
        self.filename = filename
        number_of_timepoints = self.simulation._runs_list[0].number_of_timepoints
        log_interval = self.simulation.log_interval
        max_time = number_of_timepoints * log_interval#= self.simulation.max_time
        timepoints = np.linspace(0, max_time, number_of_timepoints + 1)

        if 0 < beginning < timepoints[-1]:
            # make start the index of the timepoint closest to, and including, beginning
            self.start = bisect.bisect_left(timepoints, math.floor(beginning))
        else:
            # make start the index of the first timepoint
            self.start = 0

        if 0 < end < beginning:
            # shouldn't have to happen because of spinboxes synchronised min/max
            end = -1

        if 0 < end < timepoints[-1]:
            # make finish the index of the timepoint closest to, and including, end
            self.finish = bisect.bisect_right(timepoints, math.ceil(end))
        else:
            # make finish the index of the final timepoint + 1
            self.finish = len(timepoints) #- 1

        if every is not int:
            self.every = int(every)
        else:
            self.every = every
        if every < 1:
            self.every = 1
        if every > self.finish:
            self.every = self.finish - self.start

        self.timepoints = timepoints[self.start:self.finish:self.every]

        if chunk_size is not int:
            self.chunkSize = int(chunk_size)
        else:
            self.chunkSize = chunk_size
        if chunk_size < 1:
            self.chunkSize = 1
        if chunk_size > self.finish:
            self.chunkSize = self.finish - self.start

        if species_indices is None:
            self.species_indices = range(self.simulation.number_of_species)
        else:
            self.species_indices = species_indices
        if compartment_indices is None:
            self.compartment_indices = range(self.simulation._runs_list[0].number_of_compartments)
        else:
            self.compartment_indices = compartment_indices
        if run_indices is None:
            self.run_indices = range(0, self.simulation.number_of_runs)
        else:
            self.run_indices = run_indices

#    quantities_data_units = 'molecules'
#    quantities_data_units = self.ui.quantities_data_units_combo_box.text()

    time_data_units = 'seconds'

    def get_amounts(self, time_display_units=time_data_units, quantities_data_units, quantities_display_type, quantities_display_units, volume_display_units): pass
        timepoints, amounts = self._get_amounts()
        
        
        

#    @profile # use profile(results.get_amounts) instead - won't raise error
    def get_amounts(self):
        ''' Returns a tuple of (timepoints, results) where timepoints is an 1-D
        array of floats and results is a list of 3-D arrays of ints with the 
        shape (species, compartments, timepoint) for each run. '''
        try:
#            results = np.zeros((1000000, 1000000, 1000000)) # should raise a MemoryError
            results = [np.zeros((len(self.species_indices), len(self.compartment_indices), len(self.timepoints)), self.type) for _ in self.run_indices]
        except MemoryError:
            message = 'Could not allocate memory for amounts.\nTry selecting fewer runs, a shorter time window or a bigger time interval multipler.'
            if self.parent is not None:
                QMessageBox.warning('Out of memory', message)
            else:
                print message
            return (self.timepoints, [])
        h5 = tables.openFile(self.filename)
        for ri, r in enumerate(self.run_indices):
            where = '/run%s' % (r + 1)
            amounts = h5.getNode(where, 'amounts')[:, :, self.start:self.finish:self.every]
            for si, s in enumerate(self.species_indices):
                for ci, c in enumerate(self.compartment_indices):
                    results[ri][si, ci, :] = amounts[s, c, :]
#                    results[ri][si, ci, :] = h5.getNode(where, 'amounts')[s, c, self.start:self.finish:self.every]
        h5.close()
        return (self.timepoints, results)


    def get_volumes(self):
        try:
            results = [np.zeros((len(self.compartment_indices), len(self.timepoints)), self.type) for _ in self.run_indices]
        except MemoryError:
            message = 'Could not allocate memory for amounts.\nTry selecting fewer runs, a shorter time window or a bigger time interval multipler.'
            if self.parent is not None:
                QMessageBox.warning('Out of memory', message)
            else:
                print message
            return (self.timepoints, [])
        
        h5 = tables.openFile(self.filename)
        for ri, r in enumerate(self.run_indices):
            where = '/run%s' % (r + 1)
            volumes = h5.getNode(where, 'volumes')[:, self.start:self.finish:self.every]
            for ci, c in enumerate(self.compartment_indices):
                results[ri][ci, :] = volumes[c, :]
        h5.close()
        return (self.timepoints, results)
        
    def get_volumes_mean_over_runs(self):
        raise NotImplementedError
        
        


##import itertools
##axes = ('runs', 'species', 'compartments', 'timepoints')
##for i in range(2, len(axes)):
##    for combo in itertools.combinations(axes, i):
##        print '\tdef get_function_over_' + '_and_'.join(combo) + '(self):', '#', '(' + ', '.join([axis for axis in axes if axis not in combo]) + ')\n\t\tpass'  
#
#    def get_function_over_runs_and_species(self, f): # (compartments, timepoints)
#        'of levels for all species in each compartment at each timepoint for all runs'
#        shape = (10000, 100000)
#        return np.zeros(shape)
#    def get_function_over_runs_and_compartments(self, f): # (species, timepoints)
#        'of levels of each species in all compartments at each timepoint for all runs'
#        shape = (100, 100000)
#        return np.zeros(shape)
#    def get_function_over_runs_and_timepoints(self, f): # (species, compartments)
#        'of levels of each species in each compartment at all timepoints for all runs'
#        shape = (100, 10000)
#        return np.zeros(shape)
#    def get_function_over_species_and_compartments(self, f): # (runs, timepoints)
#        'of levels for all species in all compartments at each timepoint in each run'
#        shape = (1000, 100000)
#        return np.zeros(shape)
#    def get_function_over_species_and_timepoints(self, f): # (runs, compartments)
#        'of levels for all species in each compartment at all timepoints in each run'
#        shape = (1000, 10000)
#        return np.zeros(shape)
#    def get_function_over_compartments_and_timepoints(self, f): # (runs, species)
#        'of levels of each species in all compartments at all timepoints in each run'
#        shape = (1000, 100)
#        return np.zeros(shape)
#    
#    def get_function_over_runs_and_species_and_compartments(self, f): # (timepoints)
#        'of levels for all species in all compartments at each timepoint for all runs'
#        shape = (100000,)
#        return np.zeros(shape)
#    def get_function_over_runs_and_species_and_timepoints(self, f): # (compartments)
#        'of levels for all species in each compartment at all timepoints for all runs'
#        shape = (10000,)
#        return np.zeros(shape)
#    def get_function_over_runs_and_compartments_and_timepoints(self, f): # (species)
#        'of levels of each species in all compartments at all timepoints for all runs'
#        shape = (100,)
#        return np.zeros(shape)
#    def get_function_over_species_and_compartments_and_timepoints(self, f): # (runs)
#        'of levels for all species in all compartments at all timepoints of each run'
#        shape = (1000,)
#        return np.zeros(shape)
#
#
##import itertools
##axes = ('runs', 'species', 'compartments', 'timepoints')
##for i in (1,):
##    for combo in itertools.combinations(axes, i):
##        print '\tdef get_function_over_' + '_and_'.join(combo) + '(self):', '#', '(' + ', '.join([axis for axis in axes if axis not in combo]) + ')\n\t\tpass'  
#    
#    # these methods should apply a function along the over_x axis
#    def get_function_over_runs(self): # (species, compartments, timepoints)
#        'of levels for each species in each compartment at each timepoint for all runs'
#        shape = (100, 10000, 10000)
#        return np.zeros(shape)
#    def get_function_over_species(self): # (runs, compartments, timepoints)
#        'of levels for all species in each compartment at each timepoint for each run'
#        shape = (1000, 10000, 100000)
#        return np.zeros(shape)
#    def get_function_over_compartments(self): # (runs, species, timepoints)
#        'of levels for each species in all compartments at each timepoint for each run'
#        shape = (1000, 100, 100000)
#        return np.zeros(shape)
#    def get_function_over_timepoints(self): # (runs, species, compartments)
#        'of levels for each species in each compartment at all timepoints for each run'
#        shape = (1000, 100, 10000)
#        return np.zeros(shape)
#
##FIXME some of these are equivalent to some of the ones below, the arrays just have an extra dimension for runs where below would return a list of arrays of len(runs) 
#
##axes = ('species', 'compartments', 'timepoints')
##for i in range(1, len(axes)):
##    for combo in itertools.combinations(axes, i):
##        print '\tdef get_levels_over_' + '_and_'.join(combo) + '(self):', '#', '[(' + ', '.join([axis for axis in axes if axis not in combo]) + ')]\n\t\tpass'  
#
#    def get_levels_over_species(self): # [(compartments, timepoints)]
#        'levels for all species in each compartment at each timepoint of each run'
#        shape = (10000, 100000)
#        return [np.zeros(shape) for _ in range(1000)]
#    def get_levels_over_compartments(self): # [(species, timepoints)]
#        'levels of each species in all compartments at each timepoint of each run'
#        shape = (100, 100000)
#        return [np.zeros(shape) for _ in range(1000)]
#    def get_levels_over_timepoints(self): # [(species, compartments)]
#        'levels of each species in each compartment at all timepoints of each run'
#        shape = (100, 10000)
#        return [np.zeros(shape) for _ in range(1000)]
#    
#    def get_levels_over_species_and_compartments(self): # [(timepoints)]
#        'levels for all species in all compartments at each timepoint of each run'
#        shape = (100000,)
#        return [np.zeros(shape) for _ in range(1000)]
#    def get_levels_over_species_and_timepoints(self): # [(compartments)]
#        'levels for all species in each compartment at all timepoints of each run'
#        shape = (10000,)
#        return [np.zeros(shape) for _ in range(1000)]
#    def get_levels_over_compartments_and_timepoints(self): # [(species)]
#        'levels of each species in all compartments for all timepoints of each run'
#        shape = (100)
#        return [np.zeros(shape) for _ in range(1000)]
#
#
#    string_to_method_map = {
#        'of levels for all species in each compartment at each timepoint for all runs':get_function_over_runs_and_species,
#        'of levels of each species in all compartments at each timepoint for all runs':get_function_over_runs_and_compartments,
#        'of levels of each species in each compartment at all timepoints for all runs':get_function_over_runs_and_timepoints,
#        'of levels for all species in all compartments at each timepoint in each run' :get_function_over_species_and_compartments,
#        'of levels for all species in each compartment at all timepoints in each run' :get_function_over_species_and_timepoints,
#        'of levels of each species in all compartments at all timepoints in each run' :get_function_over_compartments_and_timepoints,
#        'of levels for all species in all compartments at each timepoint for all runs':get_function_over_runs_and_species_and_compartments,
#        'of levels for all species in each compartment at all timepoints for all runs':get_function_over_runs_and_species_and_timepoints,
#        'of levels of each species in all compartments at all timepoints for all runs':get_function_over_runs_and_compartments_and_timepoints,
#        'of levels for all species in all compartments at all timepoints of each run' :get_function_over_species_and_compartments_and_timepoints,
#        '':get_function_over_runs,
#        '':get_function_over_species,
#        '':get_function_over_compartments,
#        '':get_function_over_timepoints,
##        '':,
#    }
#
#    def get_results_for_functions_over_axes(self, functions, axes):
#        ''' 
#        results = SimulatorResults.get_results_for_functions_over_axes(SimulatorResults(...), (np.mean, np.sum, np.mean), ('species', 'timepoints', 'runs'))
#        results = SimulatorResults.get_results_for_functions_over_axes(SimulatorResults(...), (np.std, np.mean, np.product), ('compartments', 'runs', 'species'))
#        '''
#        results = levels # start with 4-dimensional (runs, species, compartments, timepoints) array
#        results_axes = ['runs', 'species', 'compartments', 'timepoints'] 
#        for fi, f in enumerate(functions):
#            axis = axes[fi]
#            results = f(results, axis=results_axes.index(axis))
#            results_axes.remove(axis)
#        return results
#
#    string_to_function_map = {
##        'median':,
#        'mean':lambda array: np.mean(array, axis=3),
#        'standard deviation':lambda array: np.std(array, ddof=1, axis=3),
##        'variance':,
##        'sum':lambda array: np.sum(array, axis=2), #TODO 2?
#    }
#
#    '''
#chunked method used from get_functions_over_runs: 
#1. create results array of correct dimensions, handling MemoryError
#2. create 4-dimensional buffer that fits into memory
#3. repeatedly fill and do stats on buffer filling results
#4. do stats on remainder to finish filling results
#5. return results
#
#idea: seperate chunking from stats calculations
#1. for any stats function from string_to_function dict
#2. pass in results array creation function
#3. pass in do stats function
#
#problem: chunked method always chunks on timepoints dimension
#solution1: change to chunk on whatever dimension 
#solution2: don't chunk
#
#code up a couple and see if/where/how they overlap
#    '''
#

    mean = lambda array: np.mean(array, axis=3)
    std = lambda array: np.std(array, ddof=1, axis=3)

    def get_amounts_mean_over_runs(self):
        return self.get_functions_over_runs((lambda array: np.mean(array, axis=3),))
#        return self.get_functions_over_runs((SimulatorResults.mean,))
#        return self.get_functions_over_runs((self.mean,))

    def chunk_generator(self, h5file):
        pass

    def get_functions_over_runs(self, functions):
        ''' Returns a tuple of (timepoints, results) where timepoints is an 1-D
        array of floats and results is a list of 3-D arrays of floats with the 
        shape (species, compartments, timepoint) for each function in 
        functions. '''
        try:
            results = [np.zeros((len(self.species_indices), len(self.compartment_indices), len(self.timepoints)), self.type) for _ in functions]
        except MemoryError:
            message = 'Could not allocate memory for amounts.\nTry selecting fewer runs, a shorter time window or a bigger time interval multipler.'
            if self.parent is not None:
                QMessageBox.warning('Out of memory', message)
            else:
                print message
            return (self.timepoints, [])

        # create large arrays handling failure
        buffer = None
        while buffer == None:
            # allocate buffer (4-dimensional array)
            try:
                buffer = np.zeros((len(self.species_indices),
                                      len(self.compartment_indices),
                                      self.chunkSize,
                                      len(self.run_indices)),
                                      type)
            except MemoryError:
                if self.chunkSize == 0:
                    if self.parent is not None:
                        message = 'Could not allocate memory for chunk.\nTry selecting fewer runs, a shorter time window or a bigger time interval multipler.'
                        QMessageBox.warning('Out of memory', message)
                    else:
                        print message
                        return
                # progressively halve chunkSize until buffer fits into memory
                self.chunkSize = self.chunkSize // 2
                buffer = None
                continue

#            # try to get statistics from data in buffer
#            try:
#                for fi, f in enumerate(functions):
#                    f(buffer)
#            except MemoryError:
#                # progressively halve chunk_size until statistics can be done
#                self.chunk_size = self.chunk_size // 2
#                buffer = None
#                continue

        def iteration(chunk_size):
            """One iteration reads amounts into buffer and applies statistical functions to those amounts."""
            self.amounts_chunk_end = amounts_chunk_start + (chunk_size * self.every)
            for ri, r in enumerate(self.run_indices):
                where = '/run%s' % (r + 1)
                amounts = h5.getNode(where, 'amounts')[:, :, amounts_chunk_start:self.amounts_chunk_end:self.every]
                for si, s in enumerate(self.species_indices):
                    for ci, c in enumerate(self.compartment_indices):
                        buffer[si, ci, :, ri] = amounts[s, c, :] #FIXME works but surely buffer[:, :, :, ri] = amounts[self.species_indices, self.compartment_indices, :] could work too, no?
            self.statChunkEnd = stat_chunk_start + chunk_size
#            print results[1][:,:,stat_chunk_start:self.statChunkEnd]
#            print "amounts.shape: ", amounts.shape, "buffer.shape: ", buffer.shape
#            print "buffer:"
#            print buffer
            for fi, f in enumerate(functions):
                stat = results[fi][:]
                stat[:, :, stat_chunk_start:self.statChunkEnd] = f(buffer)
#                print stat[:,:,stat_chunk_start:self.statChunkEnd], "=", "std(", buffer, ")"

        h5 = tables.openFile(self.filename)

        amounts_chunk_start = self.start
        stat_chunk_start = 0
        # for each whole chunk
        quotient = len(self.timepoints) // self.chunkSize
        for i in range(quotient):
            iteration(self.chunkSize)
            amounts_chunk_start = self.amounts_chunk_end
            stat_chunk_start = self.statChunkEnd

        # and the remaining timepoints           
        remainder = len(self.timepoints) % self.chunkSize
        if remainder > 0:
            buffer = np.zeros((len(self.species_indices),
                               len(self.compartment_indices),
                               remainder,
                               len(self.run_indices)),
                               type)
            iteration(remainder)

        h5.close()
        return (self.timepoints, results)


    def get_surfaces(self):
        ''' Returns a tuple of (timepoints, results) where timepoints is an 1-D
        array of floats and results is a list of 3-D arrays of floats with the 
        shape (x_position, y_position, timepoint) for each species. '''

        selected_compartments = [compartment for compartment in self.simulation._runs_list[self.run_indices[0]]._compartments_list]
        selected_species = [self.simulation._species_list[i] for i in self.species_indices]

        # create 3D array [x,y,t] for amounts data, x and y dimensions should represent total space
        all_compartments = selected_compartments[0].run._compartments_list
        xmax = max([compartment.x_position for compartment in all_compartments])
        xmin = min([compartment.x_position for compartment in all_compartments])
        ymax = max([compartment.y_position for compartment in all_compartments])
        ymin = min([compartment.y_position for compartment in all_compartments])

        h5 = tables.openFile(self.filename)
        results = []
        for si, s in enumerate(selected_species):
            surface = np.zeros(((xmax - xmin) + 1, (ymax - ymin) + 1, len(self.timepoints)), self.type)

            # fill surface with amounts
            for ri, r in enumerate(self.run_indices): # only one for now, see SimulationResultsDialog.update_ui()
                where = '/run%s' % (r + 1)
                try:
                    amounts = h5.getNode(where, 'amounts')[:, :, self.start:self.finish:self.every]
                except MemoryError:
                    message = 'Could not allocate memory for amounts.\nTry selecting fewer species, a shorter time window or a bigger time interval multipler.'
                    if self.parent is not None:
                        QMessageBox.warning('Out of memory', message)
                    else:
                        print message
                    return (self.timepoints, [], None, None, None, None)
                if sum_compartments_at_same_xy_lattice_position:
                    for ci, c in enumerate(selected_compartments):
                        surface[c.x_position, c.y_position, :] = amounts[s.index, c.index, :] + surface[c.x_position, c.y_position, :]
                else:
                    for ci, c in enumerate(selected_compartments):
                        surface[c.x_position, c.y_position, :] = amounts[s.index, c.index, :]
            results.append(surface)
        h5.close()
        return (self.timepoints, results, xmin, xmax, ymin, ymax)

sum_compartments_at_same_xy_lattice_position = True


class SpatialPlotsWindow(QWidget):
    def __init__(self, surfaces, parent=None):
        QWidget.__init__(self)

        self.setAttribute(Qt.WA_DeleteOnClose)

        self.connect(parent, SIGNAL("destroyed(QObject*)"), self.close)
        self.filename = parent.filename

        self.setWindowTitle('Surface plots for %s' % self.filename)

        self.surfaces = surfaces
        h = QHBoxLayout()
        h.setSpacing(0)
        self.widgets = []
        for surface in self.surfaces:
            self.widgets.append(surface.edit_traits().control)
#        for widget in self.widgets:
#            h.addWidget(widget)
        rows, cols = arrange(len(self.surfaces))
#        print rows, cols
        gridLayout = QGridLayout()
        for i, widget in enumerate(self.widgets):
#            print widget
#            print (i // rows), (i % rows)
            gridLayout.addWidget(widget, i // rows, i % rows) #FIXME 
        v = QVBoxLayout()
        v.setSpacing(0)
#        v.addLayout(h)
        v.addLayout(gridLayout)

        compareButton = QPushButton('Compare')
        self.connect(compareButton, SIGNAL('clicked()'), self.createSurfacesListWidget)

        self.controls = SpatialPlotsControlsWidget(surfaces)

        h2 = QHBoxLayout()
        h2.addWidget(self.controls)
        h2.addWidget(compareButton)
        v.addLayout(h2)

        self.setLayout(v)

    def createSurfacesListWidget(self):
        position = self.controls.getPosition()
        self.surfacesListWidget = SurfacesListWidget(self.surfaces, position, self)
        self.surfacesListWidget.show()




class SurfacesListWidget(QWidget):
    def __init__(self, surfaces, position, parent):
        QWidget.__init__(self)
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.parent = parent

        self.surfaces = surfaces
        self.position = position
        #TODO position to time

        self.setWindowTitle('Surfaces at position %s' % self.position)

        self.setupUi()

        self.update_ui()


    def setupUi(self):

        self.listWidget = QListWidget(self)
        self.listWidget.setViewMode(QListWidget.IconMode)
        self.listWidget.setSelectionMode(QListWidget.ExtendedSelection)
        self.listWidget.setSelectionBehavior(QListWidget.SelectItems)
        self.listWidget.setIconSize(QSize(200, 200))
#        self.listWidget.setDragDropMode(QListWidget.InternalMove)
#        self.listWidget.setDragEnabled(True)
        self.listWidget.setUniformItemSizes(True)

        for surface in self.surfaces:
            array = surface.arrayAtPosition(self.position)
            fileLikeObject = StringIO.StringIO()
            save_array_as_image(fileLikeObject, array, format='PNG')
            pixmap = QPixmap()
            succeeded = pixmap.loadFromData(fileLikeObject.getvalue(), "PNG")
            fileLikeObject.close()
            if succeeded:
                pixmap = pixmap.scaledToWidth(100)
                item = QListWidgetItem(surface.species_name, self.listWidget)
                item.setIcon(QIcon(pixmap))
                item.surface = surface

        self.connect(self.listWidget, SIGNAL('itemSelectionChanged()'), self.update_ui)
        self.connect(self.listWidget, SIGNAL('itemDoubleClicked(QListWidgetItem *)'), self.showItem)

        self.overlapPairwiseButton = QPushButton('Overlap pairwise', self)
        self.connect(self.overlapPairwiseButton, SIGNAL('clicked()'), self.overlapPairwise)

        self.v = QVBoxLayout(self)
        self.v.addWidget(self.listWidget)
        self.v.addWidget(self.overlapPairwiseButton)
        # next index for v is 2

        self.secondListWidget = QListWidget(self)
        self.secondListWidget.setViewMode(QListWidget.IconMode)
        self.secondListWidget.setSelectionMode(QListWidget.ExtendedSelection)
        self.secondListWidget.setSelectionBehavior(QListWidget.SelectItems)
        self.secondListWidget.setIconSize(QSize(200, 200))
#        self.secondListWidget.setDragDropMode(QListWidget.InternalMove)
#        self.secondListWidget.setDragEnabled(True)
        self.secondListWidget.setUniformItemSizes(True)

        self.connect(self.secondListWidget, SIGNAL('itemSelectionChanged()'), self.update_ui)
        self.connect(self.secondListWidget, SIGNAL('itemDoubleClicked(QListWidgetItem *)'), self.showItem)
        self.saveSelectedButton = QPushButton('Save selected', self)
        self.connect(self.saveSelectedButton, SIGNAL('clicked()'), self.saveSelected)
        self.saveAllSelectedButton = QPushButton('Save all selected', self)
        self.connect(self.saveAllSelectedButton, SIGNAL('clicked()'), self.saveAllSelected)

        self.v.addWidget(self.secondListWidget)
        h = QHBoxLayout()
        h.addWidget(self.saveSelectedButton)
        h.addWidget(self.saveAllSelectedButton)
        self.v.addLayout(h)

        self.setLayout(self.v)

        self.resize(640, 480)
        centre_window(self)


    def showItem(self, item):
        self.label = QLabel(self, Qt.Window)
        self.label.setWindowTitle(item.text())
        icon = item.icon()
        self.label.setPixmap(icon.pixmap(400, 400))
        self.label.setScaledContents(True)
        self.label.setToolTip('Drag to resize image, right-click to save.')
        pixmap = self.label.pixmap()
        self.label.resize(pixmap.width() * 4, pixmap.height() * 4)
        centre_window(self.label)
        self.label.show()
        self.label.setContextMenuPolicy(Qt.CustomContextMenu)
        self.connect(self.label, SIGNAL('customContextMenuRequested(const QPoint &)'), self.saveLabel)

    def saveLabel(self):
        filename = self.getSaveFilename(self.label.windowTitle())
        if filename != '':
            if not filename.endsWith(QString('.png'), Qt.CaseInsensitive):
                filename = QString('%s.png' % filename)
            pixmap = self.label.pixmap().scaled(self.label.size())
            pixmap.save(filename, 'png')
            self.lastDirectory = QFileInfo(filename).absolutePath()

    def getSaveFilename(self, filename):
        if hasattr(self, 'lastDirectory'):
            filename = '%s/%s' % (self.lastDirectory, filename)
        filename = QFileDialog.getSaveFileName(self, 'Specify a filename to save image to', filename, 'PNG files (*.png)')
        if filename != '':
            if not filename.endsWith(QString('.png'), Qt.CaseInsensitive):
                filename = QString('%s.png' % filename)
            self.lastDirectory = QFileInfo(filename).absolutePath()
        return filename


    def update_ui(self):
        self.overlapPairwiseButton.setEnabled(len(self.listWidget.selectedItems()) > 1)
        self.saveSelectedButton.setEnabled(len(self.secondListWidget.selectedItems()) == 1)
        self.saveAllSelectedButton.setEnabled(len(self.secondListWidget.selectedItems()) > 0)

    def overlapPairwise(self):
#        # remove secondListWidget 
#        layoutItem = self.v.itemAt(2)
#        if layoutItem != 0:
#            self.v.removeItem(layoutItem)
#        self.v.addWidget(self.secondListWidget)

        self.secondListWidget.clear()

        surfaces = [item.surface for item in self.listWidget.selectedItems()]

        import itertools
        for pair in itertools.combinations(surfaces, 2):
            s1 = pair[0]
            s2 = pair[1]
            array1 = s1.arrayAtPosition(self.position)
            array2 = s2.arrayAtPosition(self.position) * -1
            array = array1 + array2

            fileLikeObject = StringIO.StringIO()
            save_array_as_image(fileLikeObject, array, format='PNG')
            pixmap = QPixmap()
            succeeded = pixmap.loadFromData(fileLikeObject.getvalue(), "PNG")
            fileLikeObject.close()
            if succeeded:
                pixmap = pixmap.scaledToWidth(100)
                item = QListWidgetItem('%s+%s' % (s1.species_name, s2.species_name), self.secondListWidget)
                item.setIcon(QIcon(pixmap))
                info = QFileInfo(self.parent.filename)
                item.filename = '%s+%s_%s_%s.png' % (s1.species_name, s2.species_name, self.position, info.fileName())
                item.array = array

    def saveSelected(self):
        item = self.secondListWidget.selectedItems()[0]
        filename = self.getSaveFilename(item.text())
        if filename != '':
            save_array_as_image(filename, item.array, format='png')

    def saveAllSelected(self):
        directory = QFileDialog.getExistingDirectory(self, 'Specify a directory to save images to')
        if directory != '':
            items = self.secondListWidget.selectedItems()
            for item in items:
                save_array_as_image('%s/%s' % (directory, item.filename), item.array)


def save_array_as_image(filename, array, colourmap=None, vmin=None, vmax=None, format=None, origin=None):
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    from matplotlib import cm

    figure = Figure(figsize=array.shape[::-1], dpi=1, frameon=False)
    canvas = FigureCanvas(figure) # essential even though it isn't used
    figure.figimage(array, cmap=cm.get_cmap(colourmap), vmin=vmin, vmax=vmax, origin=origin)
    figure.savefig(filename, dpi=1, format=format)




class ControlsWidget(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self.ui = Ui_ControlsWidget()
        self.ui.setupUi(self)
        self.maximum = self.ui.positionSlider.maximum()
        self.position = 0
        self.timer = QTimer(self)
        self.connect(self.timer, SIGNAL("timeout()"), self.next_position);
        self.reset()
        self.connect(self.ui.playPauseButton, SIGNAL("clicked()"), self.playPauseButton_clicked)
        self.connect(self.ui.positionSlider, SIGNAL("valueChanged(int)"), self.set_position)
        self.connect(self, SIGNAL("position_changed(int)"), self.ui.positionSlider, SLOT("setValue(int)"))

    def reset(self):
        self.set_position(0)
        self.finished = False
        self.pause()

    def pause(self):
        self.paused = True
        self.update_ui()
        self.timer.stop()

    def play(self):
        self.paused = False
        self.update_ui()
        self.timer.start(0) # <-- change this to make steps longer

    def set_position(self, position):
        if self.position != position:
            if 0 <= position <= self.maximum:
                self.position = position
                self.emit(SIGNAL("position_changed(int)"), self.position)
            if self.position == self.maximum:
                self.finished = True
                self.pause()
            else:
                self.finished = False
            self.update_ui()

    def next_position(self):
        self.set_position(self.position + 1)

    def update_ui(self):
        if self.ui.positionSlider.value() == self.maximum:
            self.ui.playPauseButton.setText("Reset")
        else:
            self.ui.playPauseButton.setText("Play") if self.paused else self.ui.playPauseButton.setText("Pause")

    def playPauseButton_clicked(self):
        if self.finished:
            self.reset()
        else:
            self.play() if self.paused else self.pause()


class SpatialPlotsControlsWidget(ControlsWidget):

    def __init__(self, surfaces):
        ControlsWidget.__init__(self)
        self.surfaces = surfaces
        self.connect(self, SIGNAL("position_changed(int)"), self.update_surfaces)
        self.maximum = len(surfaces[0].timepoints) - 1
        self.ui.positionSlider.setMaximum(self.maximum)
        self.ui.positionSlider.setTickPosition(QSlider.TicksBelow)
        self.ui.spinBox.setMaximum(self.maximum)

    def update_surfaces(self):
        for surface in self.surfaces:
            surface.set_position(self.position)

    def getPosition(self):
        return self.ui.positionSlider.value()


class Surface(HasTraits):
    scene = Instance(MlabSceneModel, ())
    surf = Instance(PipelineBase) # surf = plot

    def _surf_default(self):
        """ (Called after initialisation) \
            Plots a surface with the shape of the first two indicies in \ 
            self.array and the height of the value in the third index.
        """
        # create the surf trait, our surface
        surf = self.scene.mlab.surf(self.array[:, :, 0], warp_scale=self.warp_scale)#, figure=self.scene.mayavi_scene)

        # create a title and get handle to it
        self.title = self.scene.mlab.title("Molecules of %s at 0" % self.species_name, size=0.5, height=0.91)#, figure=self.scene.mayavi_scene)
        self.title.x_position = 0.03
        self.title.actor.width = 0.94

        # create axes showing compartment x,y coordinates and fix text formatting
        axes = self.scene.mlab.axes(ranges=self.extent, xlabel="X", ylabel="Y") #, figure=self.scene.mayavi_scene)
        axes.label_text_property.set(italic=0, bold=0)
        #axes.axes.print_traits()
        axes.axes.number_of_labels = 3
        axes.axes.z_axis_visibility = 0
        axes.axes.z_label = ""

        # create and get a handle to the scalarbar
        scalarbar = self.scene.mlab.scalarbar(None, "", "vertical", 5, None, '%.f')#, figure=self.scene.mayavi_scene)
        # set scalarbar title and label fonts
        scalarbar.title_text_property.set(font_size=4, italic=0, bold=0)
        scalarbar.label_text_property.set(font_size=4, italic=0, bold=0)#, line_spacing=0.5)
        # vtk (< 5.2)
#        scalarbar.position = [0.832050505051, 0.0348561403509]
#        scalarbar.position2 = value = [0.162034646465, 0.287167919799]

        # set angle scene is viewed from
        self.scene.scene_editor.isometric_view() #WARNING removing this line causes the surface not to display and the axes to rotate 90 degrees vertically!
##        self.scene.mlab.view(-45, 90, 4) # rotated 45 degrees, viewed side on, from a distance of 4  
        # more angle setting in self.create_pipeline()

        return surf

    def __init__(self, array, warp_scale, extent, species_name, timepoints):
        HasTraits.__init__(self)
        self.array = array
        self.warp_scale = warp_scale
        self.extent = extent
        self.species_name = species_name
        self.timepoints = timepoints
        # create a 'position' trait that enables us to choose the frame
        self.add_trait('position', Range(0, len(timepoints) - 1, 0))

    view = View(Item('scene', show_label=False, editor=SceneEditor(scene_class=MayaviScene)),
                VGroup('position'#, 'sync_positions'
                ),
                kind='panel', resizable=True)

    @on_trait_change('scene.activated')
    def create_pipeline(self):
        """ set traits for items in figure """
        # some things need to activated here otherwise it crashes

        # doing this somehow fixes the overlapping figures problem in MayaVi2 3.1 that "figure=self.scene.mayavi_scene)" fixes in 3.3
        scalar_bar_widget = self.surf.module_manager.scalar_lut_manager.scalar_bar_widget
#        # vtk (>= 5.2)
#        # set position and size of scalarbar
#        # since VTK-5.2 the actual scalarbar widget is accessed through the scalar_bar_widget's representation property 
#        # (see https://mail.enthought.com/pipermail/enthought-dev/2009-May/021342.html)
#        scalar_bar_widget.representation.set(position=[0.827,0.0524], position2=[0.1557,0.42])

        f = self.scene.mlab.gcf()
        camera = f.scene.camera
        camera.focal_point = (-0.5, -0.5, 0)
        camera.position = (36.0146, 67.4237, 77.1612)
        camera.distance = 100

    # PyQt4 slot
    def set_position(self, position):
        self.position = position

    @on_trait_change('position')
    def update_plot(self):
        self.surf.mlab_source.set(scalars=self.array[:, :, self.position])
        self.title.text = "Molecules of %s at %s" % (self.species_name, round(self.timepoints[self.position]))

    def arrayAtPosition(self, position):
        return self.array[:, :, position]


def test():
#    w = SimulationResultsDialog(filename='/home/jvb/dashboard/examples/NAR-poptimizer/NAR_output.h5')
#    w = SimulationResultsDialog(filename='/home/jvb/phd/eclipse/infobiotics/dashboard/tests/NAR-ok/simulation.h5')
    w = SimulationResultsDialog(filename='/home/jvb/dashboard/examples/autoregulation/autoregulation_simulation.h5')

    if w.loaded:
#        w.ui.species_list_widget.selectAll()
#        w.ui.species_list_widget.setCurrentItem(w.ui.species_list_widget.findItems("proteinGFP", Qt.MatchExactly)[0])
#        for item in w.ui.species_list_widget.findItems("protein1*", Qt.MatchWildcard): item.setSelected(True)

#        w.ui.compartments_list_widget.selectAll()
#        w.ui.compartments_list_widget.setCurrentItem(w.ui.compartments_list_widget.item(0))

#        w.ui.runs_list_widget.setCurrentItem(w.ui.runs_list_widget.item(0))

        for widget in (w.ui.species_list_widget, w.ui.compartments_list_widget, w.ui.runs_list_widget):
            widget.item(0).setSelected(True)
            widget.item(widget.count() - 1).setSelected(True)

        w.ui.average_over_selected_runs_check_box.setChecked(False)

###        w.ui.visualise_population_button.click()

##        w.plot()
##        w.plotsPreviewDialog.ui.plotsListWidget.selectAll() #TODO rename
##        w.plotsPreviewDialog.combine()

#        w.export_data_as('test.csv')    # write_csv
#        w.export_data_as('test.txt')   # write_csv
#        w.export_data_as('test', open_after_save=False)        # write_csv
#        w.export_data_as('test.xls')    # write_xls
        w.export_data_as('test.npz')    # write_npz

#    centre_window(w)
#    w.show()


def test_SimulatorResults_export_data_as():
#    w = SimulationResultsDialog(filename='/home/jvb/dashboard/examples/modules/module1.h5')
    w = SimulationResultsDialog(filename='/home/jvb/dashboard/examples/autoregulation/autoregulation_simulation.h5')
    for widget in (w.ui.species_list_widget, w.ui.compartments_list_widget, w.ui.runs_list_widget):
        widget.item(0).setSelected(True)
        widget.item(widget.count() - 1).setSelected(True)
    w.ui.average_over_selected_runs_check_box.setChecked(False)
#    w.export_data_as('test.csv')    # write_csv
    w.export_data_as('test.xls')    # write_xls
#    w.export_data_as('test.npz')    # write_npz


def test_volumes():
    w = main()
    w.ui.runs_list_widget.select(0)
    w.ui.species_list_widget.select(-1)
    w.ui.species_list_widget.select(-2)
    w.ui.compartments_list_widget.select(-1)
    w.ui.compartments_list_widget.select(-2)
    w.every = 100
    p = w.plot()
#    p.ui.plotsListWidget.selectAll()
#    p.combine()
    

def profile_SimulatorResults_get_amounts():
    results = SimulatorResults(
        '/home/jvb/dashboard/examples/germination_09.h5',
        None,
    )
    get_amounts = profile(results.get_amounts)
    amounts = get_amounts()
    print amounts
    exit()

def main():
    argv = qApp.arguments()
#    argv.insert(1, '/home/jvb/dashboard/examples/modules/module1.h5')
    argv.insert(1, '/home/jvb/dashboard/examples/germination_09.h5')
    if len(argv) > 2:
        print 'usage: python simulator_results.py {h5file}'#mcss_results.sh {h5file}'
        sys.exit(2)
    if len(argv) == 1:
#        shared.settings.register_infobiotics_settings()
        w = SimulationResultsDialog()
    elif len(argv) == 2:
        w = SimulationResultsDialog(filename=argv[1])
    centre_window(w)
    w.show()
    return w
#    shared.settings.restore_window_size_and_position(w)


if __name__ == "__main__":
    main()
#    test()
#    test_SimulatorResults_export_data_as()
#    test_volumes()
#    profile_SimulatorResults_get_amounts()
    exit(qApp.exec_())

