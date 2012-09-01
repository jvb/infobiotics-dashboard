from PyQt4.QtGui import QDoubleSpinBox

class FromToDoubleSpinBox(QDoubleSpinBox):

	def __init__(self, parent=0):
		QDoubleSpinBox.__init__(self, parent)
		self.step = 1

	def set_interval(self, interval):
		self.step = round(interval, 2)
		self.setSingleStep(self.step)

	def set_maximum(self, maximum):
		if maximum - self.step < 0:
			self.setMaximum(0)
		else:
			self.setMaximum(maximum - self.step)

	def set_minimum(self, minimum):
		self.setMinimum(minimum + self.step)
