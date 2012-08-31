# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'player_control_widget.ui'
#
# Created: Wed Mar 16 09:54:31 2011
#      by: PyQt4 UI code generator 4.7
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ControlsWidget(object):
    def setupUi(self, ControlsWidget):
        ControlsWidget.setObjectName("ControlsWidget")
        ControlsWidget.resize(363, 33)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ControlsWidget.sizePolicy().hasHeightForWidth())
        ControlsWidget.setSizePolicy(sizePolicy)
        self.verticalLayout = QtGui.QVBoxLayout(ControlsWidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(2, 2, 2, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(9)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.playPauseButton = QtGui.QPushButton(ControlsWidget)
        self.playPauseButton.setObjectName("playPauseButton")
        self.horizontalLayout.addWidget(self.playPauseButton)
        self.positionSlider = QtGui.QSlider(ControlsWidget)
        self.positionSlider.setOrientation(QtCore.Qt.Horizontal)
        self.positionSlider.setObjectName("positionSlider")
        self.horizontalLayout.addWidget(self.positionSlider)
        self.spinBox = QtGui.QSpinBox(ControlsWidget)
        self.spinBox.setObjectName("spinBox")
        self.horizontalLayout.addWidget(self.spinBox)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(ControlsWidget)
        QtCore.QObject.connect(self.positionSlider, QtCore.SIGNAL("valueChanged(int)"), self.spinBox.setValue)
        QtCore.QObject.connect(self.spinBox, QtCore.SIGNAL("valueChanged(int)"), self.positionSlider.setValue)
        QtCore.QMetaObject.connectSlotsByName(ControlsWidget)

    def retranslateUi(self, ControlsWidget):
        ControlsWidget.setWindowTitle(QtGui.QApplication.translate("ControlsWidget", "Spatial Plots Controls", None, QtGui.QApplication.UnicodeUTF8))
        self.playPauseButton.setText(QtGui.QApplication.translate("ControlsWidget", "Play", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ControlsWidget = QtGui.QWidget()
    ui = Ui_ControlsWidget()
    ui.setupUi(ControlsWidget)
    ControlsWidget.show()
    sys.exit(app.exec_())

