# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'plots_preview_dialog.ui'
#
# Created: Wed Mar 16 09:54:31 2011
#      by: PyQt4 UI code generator 4.7
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_PlotsPreviewDialog(object):
    def setupUi(self, PlotsPreviewDialog):
        PlotsPreviewDialog.setObjectName("PlotsPreviewDialog")
        PlotsPreviewDialog.resize(549, 480)
        self.verticalLayout_2 = QtGui.QVBoxLayout(PlotsPreviewDialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.instructionLabel = QtGui.QLabel(PlotsPreviewDialog)
        self.instructionLabel.setWordWrap(True)
        self.instructionLabel.setObjectName("instructionLabel")
        self.verticalLayout_2.addWidget(self.instructionLabel)
        self.hideInvariantsCheckBox = QtGui.QCheckBox(PlotsPreviewDialog)
        self.hideInvariantsCheckBox.setEnabled(True)
        self.hideInvariantsCheckBox.setChecked(True)
        self.hideInvariantsCheckBox.setObjectName("hideInvariantsCheckBox")
        self.verticalLayout_2.addWidget(self.hideInvariantsCheckBox)
        self.plotsListWidget = PlotsListWidget(PlotsPreviewDialog)
        self.plotsListWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.plotsListWidget.setProperty("showDropIndicator", False)
        self.plotsListWidget.setDragEnabled(True)
        self.plotsListWidget.setDragDropMode(QtGui.QAbstractItemView.InternalMove)
        self.plotsListWidget.setAlternatingRowColors(False)
        self.plotsListWidget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.plotsListWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectItems)
        self.plotsListWidget.setIconSize(QtCore.QSize(200, 200))
        self.plotsListWidget.setTextElideMode(QtCore.Qt.ElideMiddle)
        self.plotsListWidget.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerItem)
        self.plotsListWidget.setMovement(QtGui.QListView.Snap)
        self.plotsListWidget.setFlow(QtGui.QListView.LeftToRight)
        self.plotsListWidget.setProperty("isWrapping", True)
        self.plotsListWidget.setResizeMode(QtGui.QListView.Adjust)
        self.plotsListWidget.setLayoutMode(QtGui.QListView.SinglePass)
        self.plotsListWidget.setGridSize(QtCore.QSize(200, 200))
        self.plotsListWidget.setViewMode(QtGui.QListView.IconMode)
        self.plotsListWidget.setUniformItemSizes(True)
        self.plotsListWidget.setWordWrap(False)
        self.plotsListWidget.setObjectName("plotsListWidget")
        self.verticalLayout_2.addWidget(self.plotsListWidget)
        self.line = QtGui.QFrame(PlotsPreviewDialog)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_2.addWidget(self.line)
        self.actionLayout = QtGui.QHBoxLayout()
        self.actionLayout.setObjectName("actionLayout")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.actionLayout.addItem(spacerItem)
        self.combineButton = QtGui.QPushButton(PlotsPreviewDialog)
        self.combineButton.setObjectName("combineButton")
        self.actionLayout.addWidget(self.combineButton)
        self.stackButton = QtGui.QPushButton(PlotsPreviewDialog)
        self.stackButton.setObjectName("stackButton")
        self.actionLayout.addWidget(self.stackButton)
        self.tileButton = QtGui.QPushButton(PlotsPreviewDialog)
        self.tileButton.setObjectName("tileButton")
        self.actionLayout.addWidget(self.tileButton)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.actionLayout.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.actionLayout)

        self.retranslateUi(PlotsPreviewDialog)
        QtCore.QMetaObject.connectSlotsByName(PlotsPreviewDialog)

    def retranslateUi(self, PlotsPreviewDialog):
        PlotsPreviewDialog.setWindowTitle(QtGui.QApplication.translate("PlotsPreviewDialog", "Simulation - Plots", None, QtGui.QApplication.UnicodeUTF8))
        self.instructionLabel.setText(QtGui.QApplication.translate("PlotsPreviewDialog", "Select multiple plots (using Ctrl-click) to combine, stack or tile. Drag to rearrange.", None, QtGui.QApplication.UnicodeUTF8))
        self.hideInvariantsCheckBox.setText(QtGui.QApplication.translate("PlotsPreviewDialog", "Hide invariants (using Ctrl-A to select all always selects invariants)", None, QtGui.QApplication.UnicodeUTF8))
        self.combineButton.setText(QtGui.QApplication.translate("PlotsPreviewDialog", "Combine", None, QtGui.QApplication.UnicodeUTF8))
        self.stackButton.setText(QtGui.QApplication.translate("PlotsPreviewDialog", "Stack", None, QtGui.QApplication.UnicodeUTF8))
        self.tileButton.setText(QtGui.QApplication.translate("PlotsPreviewDialog", "Tile", None, QtGui.QApplication.UnicodeUTF8))

from PlotsListWidget import PlotsListWidget

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    PlotsPreviewDialog = QtGui.QWidget()
    ui = Ui_PlotsPreviewDialog()
    ui.setupUi(PlotsPreviewDialog)
    PlotsPreviewDialog.show()
    sys.exit(app.exec_())

