# This file is part of the Infobiotics Dashboard. See LICENSE for copyright.
# $Id: FromToDoubleSpinBox.py 354 2009-10-02 14:13:02Z jvb $
# $HeadURL: https://psiren.cs.nott.ac.uk/repos/infobiotics/gui/trunk/src/simulator_results/FromToDoubleSpinBox.py $
# $Author: jvb $
# $Revision: 354 $
# $Date: 2009-10-02 15:13:02 +0100 (Fri, 02 Oct 2009) $


from PyQt4.QtGui import QDoubleSpinBox


class FromToDoubleSpinBox(QDoubleSpinBox):

    def __init__(self, parent=0):
        QDoubleSpinBox.__init__(self, parent)
        self.step = 1

    def set_interval(self, interval):
        self.step = round(interval, 2)
        self.setSingleStep(self.step)

    def set_maximum(self, max):
        self.setMaximum(max - self.step)

    def set_minimum(self, min):
        self.setMinimum(min + self.step)
