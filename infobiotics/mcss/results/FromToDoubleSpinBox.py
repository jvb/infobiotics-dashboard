from PyQt4.QtGui import QDoubleSpinBox

class FromToDoubleSpinBox(QDoubleSpinBox):

    def __init__(self, parent=0):
        QDoubleSpinBox.__init__(self, parent)
        self.step = 1

    def set_interval(self, interval):
        self.step = round(interval, 2)
        self.setSingleStep(self.step)

    def set_maximum(self, max):
#TODO fix this:
#  File "/home/jvb/eclipse/workspaces/infobiotics/infobiotics-dashboard/infobiotics/mcss/results/FromToDoubleSpinBox.py", line 15, in set_maximum
#    self.set_maximum(0)
#  File "/home/jvb/eclipse/workspaces/infobiotics/infobiotics-dashboard/infobiotics/mcss/results/FromToDoubleSpinBox.py", line 14, in set_maximum
#    if max - self.step < 0:
#  RuntimeError: maximum recursion depth exceeded in cmp
        if max - self.step < 0:
            self.set_maximum(0)
        self.setMaximum(max - self.step)

    def set_minimum(self, min):
        self.setMinimum(min + self.step)
