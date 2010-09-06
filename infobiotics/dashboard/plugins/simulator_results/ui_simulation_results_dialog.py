# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'simulation_results_dialog.ui'
#
# Created: Mon Sep  6 16:29:05 2010
#      by: PyQt4 UI code generator 4.7
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_SimulationResultsDialog(object):
    def setupUi(self, SimulationResultsDialog):
        SimulationResultsDialog.setObjectName("SimulationResultsDialog")
        SimulationResultsDialog.setEnabled(True)
        SimulationResultsDialog.resize(960, 562)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SimulationResultsDialog.sizePolicy().hasHeightForWidth())
        SimulationResultsDialog.setSizePolicy(sizePolicy)
        SimulationResultsDialog.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.gridLayout_5 = QtGui.QGridLayout(SimulationResultsDialog)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.file_name_line_edit = QtGui.QLineEdit(SimulationResultsDialog)
        self.file_name_line_edit.setEnabled(True)
        self.file_name_line_edit.setReadOnly(True)
        self.file_name_line_edit.setObjectName("file_name_line_edit")
        self.gridLayout_5.addWidget(self.file_name_line_edit, 0, 0, 1, 7)
        self.load_button = QtGui.QPushButton(SimulationResultsDialog)
        self.load_button.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.load_button.setObjectName("load_button")
        self.gridLayout_5.addWidget(self.load_button, 0, 7, 1, 1)
        self._timepoints_group_box = QtGui.QGroupBox(SimulationResultsDialog)
        self._timepoints_group_box.setFlat(True)
        self._timepoints_group_box.setObjectName("_timepoints_group_box")
        self.gridLayout_4 = QtGui.QGridLayout(self._timepoints_group_box)
        self.gridLayout_4.setContentsMargins(0, 6, 0, 0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self._from_label = QtGui.QLabel(self._timepoints_group_box)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self._from_label.sizePolicy().hasHeightForWidth())
        self._from_label.setSizePolicy(sizePolicy)
        self._from_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self._from_label.setObjectName("_from_label")
        self.gridLayout_4.addWidget(self._from_label, 0, 0, 1, 1)
        self.from_spin_box = FromToDoubleSpinBox(self._timepoints_group_box)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.from_spin_box.sizePolicy().hasHeightForWidth())
        self.from_spin_box.setSizePolicy(sizePolicy)
        self.from_spin_box.setObjectName("from_spin_box")
        self.gridLayout_4.addWidget(self.from_spin_box, 0, 1, 1, 1)
        self._to_label = QtGui.QLabel(self._timepoints_group_box)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self._to_label.sizePolicy().hasHeightForWidth())
        self._to_label.setSizePolicy(sizePolicy)
        self._to_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self._to_label.setObjectName("_to_label")
        self.gridLayout_4.addWidget(self._to_label, 0, 2, 1, 1)
        self.to_spin_box = FromToDoubleSpinBox(self._timepoints_group_box)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.to_spin_box.sizePolicy().hasHeightForWidth())
        self.to_spin_box.setSizePolicy(sizePolicy)
        self.to_spin_box.setObjectName("to_spin_box")
        self.gridLayout_4.addWidget(self.to_spin_box, 0, 3, 1, 1)
        self._every_label = QtGui.QLabel(self._timepoints_group_box)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self._every_label.sizePolicy().hasHeightForWidth())
        self._every_label.setSizePolicy(sizePolicy)
        self._every_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self._every_label.setObjectName("_every_label")
        self.gridLayout_4.addWidget(self._every_label, 0, 4, 1, 1)
        self.every_spin_box = QtGui.QSpinBox(self._timepoints_group_box)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.every_spin_box.sizePolicy().hasHeightForWidth())
        self.every_spin_box.setSizePolicy(sizePolicy)
        self.every_spin_box.setObjectName("every_spin_box")
        self.gridLayout_4.addWidget(self.every_spin_box, 0, 5, 1, 1)
        self._multiplied_by_label = QtGui.QLabel(self._timepoints_group_box)
        self._multiplied_by_label.setObjectName("_multiplied_by_label")
        self.gridLayout_4.addWidget(self._multiplied_by_label, 0, 6, 1, 1)
        self.log_interval_label = QtGui.QLabel(self._timepoints_group_box)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.log_interval_label.sizePolicy().hasHeightForWidth())
        self.log_interval_label.setSizePolicy(sizePolicy)
        self.log_interval_label.setObjectName("log_interval_label")
        self.gridLayout_4.addWidget(self.log_interval_label, 0, 7, 1, 1)
        spacerItem = QtGui.QSpacerItem(57, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem, 0, 8, 1, 1)
        self.gridLayout_5.addWidget(self._timepoints_group_box, 2, 0, 1, 7)
        spacerItem1 = QtGui.QSpacerItem(244, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem1, 5, 0, 1, 2)
        self.plot_timeseries_button = QtGui.QCommandLinkButton(SimulationResultsDialog)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/plot_2d.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.plot_timeseries_button.setIcon(icon)
        self.plot_timeseries_button.setIconSize(QtCore.QSize(64, 64))
        self.plot_timeseries_button.setObjectName("plot_timeseries_button")
        self.gridLayout_5.addWidget(self.plot_timeseries_button, 5, 3, 1, 1)
        self._runs_species_compartments_splitter = QtGui.QSplitter(SimulationResultsDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self._runs_species_compartments_splitter.sizePolicy().hasHeightForWidth())
        self._runs_species_compartments_splitter.setSizePolicy(sizePolicy)
        self._runs_species_compartments_splitter.setFrameShape(QtGui.QFrame.NoFrame)
        self._runs_species_compartments_splitter.setOrientation(QtCore.Qt.Horizontal)
        self._runs_species_compartments_splitter.setOpaqueResize(True)
        self._runs_species_compartments_splitter.setHandleWidth(6)
        self._runs_species_compartments_splitter.setChildrenCollapsible(False)
        self._runs_species_compartments_splitter.setObjectName("_runs_species_compartments_splitter")
        self._runs_group_box = QtGui.QGroupBox(self._runs_species_compartments_splitter)
        self._runs_group_box.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self._runs_group_box.setFlat(True)
        self._runs_group_box.setObjectName("_runs_group_box")
        self.gridLayout_3 = QtGui.QGridLayout(self._runs_group_box)
        self.gridLayout_3.setContentsMargins(0, 6, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.select_all_runs_check_box = QtGui.QCheckBox(self._runs_group_box)
        self.select_all_runs_check_box.setEnabled(True)
        self.select_all_runs_check_box.setChecked(False)
        self.select_all_runs_check_box.setObjectName("select_all_runs_check_box")
        self.gridLayout_3.addWidget(self.select_all_runs_check_box, 0, 0, 1, 1)
        self.runs_list_widget = QtGui.QListWidget(self._runs_group_box)
        self.runs_list_widget.setEnabled(True)
        self.runs_list_widget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.runs_list_widget.setObjectName("runs_list_widget")
        self.gridLayout_3.addWidget(self.runs_list_widget, 1, 0, 1, 3)
        self.random_runs_spin_box = QtGui.QSpinBox(self._runs_group_box)
        self.random_runs_spin_box.setEnabled(True)
        self.random_runs_spin_box.setMinimum(0)
        self.random_runs_spin_box.setMaximum(1000)
        self.random_runs_spin_box.setSingleStep(1)
        self.random_runs_spin_box.setProperty("value", 1)
        self.random_runs_spin_box.setObjectName("random_runs_spin_box")
        self.gridLayout_3.addWidget(self.random_runs_spin_box, 2, 0, 1, 1)
        self.random_runs_label = QtGui.QLabel(self._runs_group_box)
        self.random_runs_label.setObjectName("random_runs_label")
        self.gridLayout_3.addWidget(self.random_runs_label, 2, 1, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem2, 2, 2, 1, 1)
        self.runs_selected_and_total_label = QtGui.QLabel(self._runs_group_box)
        self.runs_selected_and_total_label.setScaledContents(False)
        self.runs_selected_and_total_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.runs_selected_and_total_label.setObjectName("runs_selected_and_total_label")
        self.gridLayout_3.addWidget(self.runs_selected_and_total_label, 0, 2, 1, 1)
        self._species_group_box = QtGui.QGroupBox(self._runs_species_compartments_splitter)
        self._species_group_box.setFlat(True)
        self._species_group_box.setObjectName("_species_group_box")
        self.gridLayout_2 = QtGui.QGridLayout(self._species_group_box)
        self.gridLayout_2.setContentsMargins(0, 6, 0, 0)
        self.gridLayout_2.setHorizontalSpacing(6)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.select_all_species_check_box = QtGui.QCheckBox(self._species_group_box)
        self.select_all_species_check_box.setEnabled(True)
        self.select_all_species_check_box.setChecked(False)
        self.select_all_species_check_box.setObjectName("select_all_species_check_box")
        self.gridLayout_2.addWidget(self.select_all_species_check_box, 0, 0, 1, 1)
        self.species_selected_and_total_label = QtGui.QLabel(self._species_group_box)
        self.species_selected_and_total_label.setScaledContents(False)
        self.species_selected_and_total_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.species_selected_and_total_label.setObjectName("species_selected_and_total_label")
        self.gridLayout_2.addWidget(self.species_selected_and_total_label, 0, 1, 1, 1)
        self.species_list_widget = QtGui.QListWidget(self._species_group_box)
        self.species_list_widget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.species_list_widget.setObjectName("species_list_widget")
        QtGui.QListWidgetItem(self.species_list_widget)
        self.gridLayout_2.addWidget(self.species_list_widget, 1, 0, 1, 2)
        self.filter_species_line_edit = QtGui.QLineEdit(self._species_group_box)
        self.filter_species_line_edit.setObjectName("filter_species_line_edit")
        self.gridLayout_2.addWidget(self.filter_species_line_edit, 2, 0, 1, 1)
        self.sort_species_check_box = QtGui.QCheckBox(self._species_group_box)
        self.sort_species_check_box.setObjectName("sort_species_check_box")
        self.gridLayout_2.addWidget(self.sort_species_check_box, 2, 1, 1, 1)
        self._compartments_group_box = QtGui.QGroupBox(self._runs_species_compartments_splitter)
        self._compartments_group_box.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self._compartments_group_box.setFlat(True)
        self._compartments_group_box.setObjectName("_compartments_group_box")
        self.gridLayout = QtGui.QGridLayout(self._compartments_group_box)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setContentsMargins(0, 6, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.select_all_compartments_check_box = QtGui.QCheckBox(self._compartments_group_box)
        self.select_all_compartments_check_box.setEnabled(True)
        self.select_all_compartments_check_box.setChecked(False)
        self.select_all_compartments_check_box.setObjectName("select_all_compartments_check_box")
        self.gridLayout.addWidget(self.select_all_compartments_check_box, 0, 0, 1, 1)
        self.compartments_selected_and_total_label = QtGui.QLabel(self._compartments_group_box)
        self.compartments_selected_and_total_label.setScaledContents(False)
        self.compartments_selected_and_total_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.compartments_selected_and_total_label.setObjectName("compartments_selected_and_total_label")
        self.gridLayout.addWidget(self.compartments_selected_and_total_label, 0, 1, 1, 1)
        self.compartments_list_widget = QtGui.QListWidget(self._compartments_group_box)
        self.compartments_list_widget.setEnabled(True)
        self.compartments_list_widget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.compartments_list_widget.setObjectName("compartments_list_widget")
        self.gridLayout.addWidget(self.compartments_list_widget, 2, 0, 1, 2)
        self.filter_compartments_line_edit = QtGui.QLineEdit(self._compartments_group_box)
        self.filter_compartments_line_edit.setObjectName("filter_compartments_line_edit")
        self.gridLayout.addWidget(self.filter_compartments_line_edit, 3, 0, 1, 1)
        self.sort_compartments_check_box = QtGui.QCheckBox(self._compartments_group_box)
        self.sort_compartments_check_box.setObjectName("sort_compartments_check_box")
        self.gridLayout.addWidget(self.sort_compartments_check_box, 3, 1, 1, 1)
        self.gridLayout_5.addWidget(self._runs_species_compartments_splitter, 1, 0, 1, 8)
        self.export_data_as_button = QtGui.QCommandLinkButton(SimulationResultsDialog)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/data.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.export_data_as_button.setIcon(icon1)
        self.export_data_as_button.setIconSize(QtCore.QSize(64, 64))
        self.export_data_as_button.setCheckable(False)
        self.export_data_as_button.setAutoExclusive(False)
        self.export_data_as_button.setObjectName("export_data_as_button")
        self.gridLayout_5.addWidget(self.export_data_as_button, 5, 2, 1, 1)
        self._data_group_box = QtGui.QGroupBox(SimulationResultsDialog)
        self._data_group_box.setFlat(True)
        self._data_group_box.setObjectName("_data_group_box")
        self.gridLayout_8 = QtGui.QGridLayout(self._data_group_box)
        self.gridLayout_8.setContentsMargins(0, 6, 0, 0)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.quantities_label = QtGui.QLabel(self._data_group_box)
        self.quantities_label.setObjectName("quantities_label")
        self.gridLayout_8.addWidget(self.quantities_label, 1, 0, 1, 1)
        self.average_over_selected_runs_check_box = QtGui.QCheckBox(self._data_group_box)
        self.average_over_selected_runs_check_box.setObjectName("average_over_selected_runs_check_box")
        self.gridLayout_8.addWidget(self.average_over_selected_runs_check_box, 0, 0, 1, 3)
        self.quantities_combo_box = QtGui.QComboBox(self._data_group_box)
        self.quantities_combo_box.setEnabled(False)
        self.quantities_combo_box.setObjectName("quantities_combo_box")
        self.quantities_combo_box.addItem("")
        self.quantities_combo_box.addItem("")
        self.gridLayout_8.addWidget(self.quantities_combo_box, 1, 1, 1, 1)
        self.calculate_button = QtGui.QCommandLinkButton(self._data_group_box)
        self.calculate_button.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.calculate_button.setObjectName("calculate_button")
        self.gridLayout_8.addWidget(self.calculate_button, 0, 4, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_8.addItem(spacerItem3, 1, 2, 1, 3)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_8.addItem(spacerItem4, 0, 3, 1, 1)
        self.gridLayout_5.addWidget(self._data_group_box, 3, 0, 1, 8)
        self.plot_histograms_button = QtGui.QCommandLinkButton(SimulationResultsDialog)
        self.plot_histograms_button.setEnabled(False)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/hist.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.plot_histograms_button.setIcon(icon2)
        self.plot_histograms_button.setIconSize(QtCore.QSize(64, 64))
        self.plot_histograms_button.setCheckable(False)
        self.plot_histograms_button.setAutoExclusive(False)
        self.plot_histograms_button.setObjectName("plot_histograms_button")
        self.gridLayout_5.addWidget(self.plot_histograms_button, 5, 5, 1, 3)
        self.visualise_population_button = QtGui.QCommandLinkButton(SimulationResultsDialog)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/plot_3d.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.visualise_population_button.setIcon(icon3)
        self.visualise_population_button.setIconSize(QtCore.QSize(64, 64))
        self.visualise_population_button.setObjectName("visualise_population_button")
        self.gridLayout_5.addWidget(self.visualise_population_button, 5, 4, 1, 1)
        self.random_runs_label.setBuddy(self.random_runs_spin_box)

        self.retranslateUi(SimulationResultsDialog)
        QtCore.QMetaObject.connectSlotsByName(SimulationResultsDialog)
        SimulationResultsDialog.setTabOrder(self.file_name_line_edit, self.select_all_runs_check_box)
        SimulationResultsDialog.setTabOrder(self.select_all_runs_check_box, self.random_runs_spin_box)
        SimulationResultsDialog.setTabOrder(self.random_runs_spin_box, self.runs_list_widget)
        SimulationResultsDialog.setTabOrder(self.runs_list_widget, self.select_all_species_check_box)
        SimulationResultsDialog.setTabOrder(self.select_all_species_check_box, self.species_list_widget)
        SimulationResultsDialog.setTabOrder(self.species_list_widget, self.select_all_compartments_check_box)
        SimulationResultsDialog.setTabOrder(self.select_all_compartments_check_box, self.compartments_list_widget)

    def retranslateUi(self, SimulationResultsDialog):
        SimulationResultsDialog.setWindowTitle(QtGui.QApplication.translate("SimulationResultsDialog", "Simulator Results", None, QtGui.QApplication.UnicodeUTF8))
        self.load_button.setToolTip(QtGui.QApplication.translate("SimulationResultsDialog", "Select a different H5 file", None, QtGui.QApplication.UnicodeUTF8))
        self.load_button.setText(QtGui.QApplication.translate("SimulationResultsDialog", "Browse...", None, QtGui.QApplication.UnicodeUTF8))
        self._timepoints_group_box.setTitle(QtGui.QApplication.translate("SimulationResultsDialog", "Timepoints", None, QtGui.QApplication.UnicodeUTF8))
        self._from_label.setToolTip(QtGui.QApplication.translate("SimulationResultsDialog", "Select timepoints starting from <I>n</I>", None, QtGui.QApplication.UnicodeUTF8))
        self._from_label.setText(QtGui.QApplication.translate("SimulationResultsDialog", "From", None, QtGui.QApplication.UnicodeUTF8))
        self.from_spin_box.setToolTip(QtGui.QApplication.translate("SimulationResultsDialog", "Select timepoints starting from <I>n</I>", None, QtGui.QApplication.UnicodeUTF8))
        self._to_label.setToolTip(QtGui.QApplication.translate("SimulationResultsDialog", "Select timepoints up to and including <I>n</I>", None, QtGui.QApplication.UnicodeUTF8))
        self._to_label.setText(QtGui.QApplication.translate("SimulationResultsDialog", "to", None, QtGui.QApplication.UnicodeUTF8))
        self.to_spin_box.setToolTip(QtGui.QApplication.translate("SimulationResultsDialog", "Select timepoints up to and including <I>n</I>", None, QtGui.QApplication.UnicodeUTF8))
        self._every_label.setToolTip(QtGui.QApplication.translate("SimulationResultsDialog", "Select every <I>n</I> timepoints from start to finish", None, QtGui.QApplication.UnicodeUTF8))
        self._every_label.setText(QtGui.QApplication.translate("SimulationResultsDialog", "every", None, QtGui.QApplication.UnicodeUTF8))
        self.every_spin_box.setToolTip(QtGui.QApplication.translate("SimulationResultsDialog", "Select every <I>n</I> timepoints from start to finish", None, QtGui.QApplication.UnicodeUTF8))
        self._multiplied_by_label.setToolTip(QtGui.QApplication.translate("SimulationResultsDialog", "multiplied by", None, QtGui.QApplication.UnicodeUTF8))
        self._multiplied_by_label.setText(QtGui.QApplication.translate("SimulationResultsDialog", "x", None, QtGui.QApplication.UnicodeUTF8))
        self.log_interval_label.setToolTip(QtGui.QApplication.translate("SimulationResultsDialog", "Logging interval (log_interval) of simulation", None, QtGui.QApplication.UnicodeUTF8))
        self.plot_timeseries_button.setToolTip(QtGui.QApplication.translate("SimulationResultsDialog", "Plot timeseries for selected runs, species and compartments", None, QtGui.QApplication.UnicodeUTF8))
        self.plot_timeseries_button.setText(QtGui.QApplication.translate("SimulationResultsDialog", "Plot timeseries", None, QtGui.QApplication.UnicodeUTF8))
        self.plot_timeseries_button.setDescription(QtGui.QApplication.translate("SimulationResultsDialog", "Preview plots individually then combine, stack or tile", None, QtGui.QApplication.UnicodeUTF8))
        self._runs_group_box.setTitle(QtGui.QApplication.translate("SimulationResultsDialog", "Runs", None, QtGui.QApplication.UnicodeUTF8))
        self.select_all_runs_check_box.setToolTip(QtGui.QApplication.translate("SimulationResultsDialog", "Select all runs", None, QtGui.QApplication.UnicodeUTF8))
        self.select_all_runs_check_box.setText(QtGui.QApplication.translate("SimulationResultsDialog", "All", None, QtGui.QApplication.UnicodeUTF8))
        self.runs_list_widget.setToolTip(QtGui.QApplication.translate("SimulationResultsDialog", "Select multiple runs using Ctrl-click, Shift-click or by clicking and dragging.", None, QtGui.QApplication.UnicodeUTF8))
        self.random_runs_spin_box.setToolTip(QtGui.QApplication.translate("SimulationResultsDialog", "Select <I>n</I> random runs", None, QtGui.QApplication.UnicodeUTF8))
        self.random_runs_label.setToolTip(QtGui.QApplication.translate("SimulationResultsDialog", "Select <I>n</I> random runs", None, QtGui.QApplication.UnicodeUTF8))
        self.random_runs_label.setText(QtGui.QApplication.translate("SimulationResultsDialog", "random runs", None, QtGui.QApplication.UnicodeUTF8))
        self.runs_selected_and_total_label.setToolTip(QtGui.QApplication.translate("SimulationResultsDialog", "selected / total", None, QtGui.QApplication.UnicodeUTF8))
        self._species_group_box.setTitle(QtGui.QApplication.translate("SimulationResultsDialog", "Species", None, QtGui.QApplication.UnicodeUTF8))
        self.select_all_species_check_box.setToolTip(QtGui.QApplication.translate("SimulationResultsDialog", "Select all (filtered) species", None, QtGui.QApplication.UnicodeUTF8))
        self.select_all_species_check_box.setText(QtGui.QApplication.translate("SimulationResultsDialog", "All", None, QtGui.QApplication.UnicodeUTF8))
        self.species_selected_and_total_label.setToolTip(QtGui.QApplication.translate("SimulationResultsDialog", "selected / total", None, QtGui.QApplication.UnicodeUTF8))
        self.species_list_widget.setToolTip(QtGui.QApplication.translate("SimulationResultsDialog", "Select multiple species using Ctrl-click, Shift-click or by clicking and dragging.", None, QtGui.QApplication.UnicodeUTF8))
        self.species_list_widget.setSortingEnabled(False)
        __sortingEnabled = self.species_list_widget.isSortingEnabled()
        self.species_list_widget.setSortingEnabled(False)
        self.species_list_widget.item(0).setText(QtGui.QApplication.translate("SimulationResultsDialog", "Volumes", None, QtGui.QApplication.UnicodeUTF8))
        self.species_list_widget.setSortingEnabled(__sortingEnabled)
        self.filter_species_line_edit.setToolTip(QtGui.QApplication.translate("SimulationResultsDialog", "Filter Species", None, QtGui.QApplication.UnicodeUTF8))
        self.sort_species_check_box.setText(QtGui.QApplication.translate("SimulationResultsDialog", "Sort", None, QtGui.QApplication.UnicodeUTF8))
        self._compartments_group_box.setTitle(QtGui.QApplication.translate("SimulationResultsDialog", "Compartments", None, QtGui.QApplication.UnicodeUTF8))
        self.select_all_compartments_check_box.setToolTip(QtGui.QApplication.translate("SimulationResultsDialog", "Select all (filter) compartments", None, QtGui.QApplication.UnicodeUTF8))
        self.select_all_compartments_check_box.setText(QtGui.QApplication.translate("SimulationResultsDialog", "All", None, QtGui.QApplication.UnicodeUTF8))
        self.compartments_selected_and_total_label.setToolTip(QtGui.QApplication.translate("SimulationResultsDialog", "selected / total", None, QtGui.QApplication.UnicodeUTF8))
        self.compartments_list_widget.setToolTip(QtGui.QApplication.translate("SimulationResultsDialog", "Select multiple compartments using Ctrl-click, Shift-click or by clicking and dragging.", None, QtGui.QApplication.UnicodeUTF8))
        self.compartments_list_widget.setSortingEnabled(False)
        self.filter_compartments_line_edit.setToolTip(QtGui.QApplication.translate("SimulationResultsDialog", "Filter Compartments", None, QtGui.QApplication.UnicodeUTF8))
        self.sort_compartments_check_box.setText(QtGui.QApplication.translate("SimulationResultsDialog", "Sort", None, QtGui.QApplication.UnicodeUTF8))
        self.export_data_as_button.setToolTip(QtGui.QApplication.translate("SimulationResultsDialog", "Save timeseries data for selected runs, species and compartments", None, QtGui.QApplication.UnicodeUTF8))
        self.export_data_as_button.setText(QtGui.QApplication.translate("SimulationResultsDialog", "Export data as...", None, QtGui.QApplication.UnicodeUTF8))
        self.export_data_as_button.setDescription(QtGui.QApplication.translate("SimulationResultsDialog", "text (.csv)\n"
"Excel (.xls)\n"
"NumPy (.npz)", None, QtGui.QApplication.UnicodeUTF8))
        self._data_group_box.setTitle(QtGui.QApplication.translate("SimulationResultsDialog", "Data", None, QtGui.QApplication.UnicodeUTF8))
        self.quantities_label.setText(QtGui.QApplication.translate("SimulationResultsDialog", "Quantities as", None, QtGui.QApplication.UnicodeUTF8))
        self.average_over_selected_runs_check_box.setText(QtGui.QApplication.translate("SimulationResultsDialog", "Average over selected runs", None, QtGui.QApplication.UnicodeUTF8))
        self.quantities_combo_box.setItemText(0, QtGui.QApplication.translate("SimulationResultsDialog", "molecules", None, QtGui.QApplication.UnicodeUTF8))
        self.quantities_combo_box.setItemText(1, QtGui.QApplication.translate("SimulationResultsDialog", "concentrations", None, QtGui.QApplication.UnicodeUTF8))
        self.calculate_button.setText(QtGui.QApplication.translate("SimulationResultsDialog", "Calculate other functions...", None, QtGui.QApplication.UnicodeUTF8))
        self.plot_histograms_button.setToolTip(QtGui.QApplication.translate("SimulationResultsDialog", "Save timeseries data for selected runs, species and compartments", None, QtGui.QApplication.UnicodeUTF8))
        self.plot_histograms_button.setText(QtGui.QApplication.translate("SimulationResultsDialog", "Plot histograms", None, QtGui.QApplication.UnicodeUTF8))
        self.plot_histograms_button.setDescription(QtGui.QApplication.translate("SimulationResultsDialog", "Plot distribution of species in runs or compartments", None, QtGui.QApplication.UnicodeUTF8))
        self.visualise_population_button.setToolTip(QtGui.QApplication.translate("SimulationResultsDialog", "Animate levels of selected species on the lattice", None, QtGui.QApplication.UnicodeUTF8))
        self.visualise_population_button.setText(QtGui.QApplication.translate("SimulationResultsDialog", "Visualise population", None, QtGui.QApplication.UnicodeUTF8))
        self.visualise_population_button.setDescription(QtGui.QApplication.translate("SimulationResultsDialog", "Animate species levels as a surface over the lattice", None, QtGui.QApplication.UnicodeUTF8))

from simulator_results import FromToDoubleSpinBox
import icons_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    SimulationResultsDialog = QtGui.QWidget()
    ui = Ui_SimulationResultsDialog()
    ui.setupUi(SimulationResultsDialog)
    SimulationResultsDialog.show()
    sys.exit(app.exec_())

