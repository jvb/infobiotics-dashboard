from pyface.workbench.api import TraitsUIEditor
from traits.api import Str
import os.path

class DashboardExperimentEditor(TraitsUIEditor):

	file_name_attr = Str
	def _file_name_attr_default(self):
#		raise NotImplementedError
		return '_params_file'

	def _name_default(self):
		file_name = os.path.split(getattr(self.obj, self.file_name_attr, ''))[1]
		self.on_trait_change(self.obj_file_name_changed, name='obj.%s' % self.file_name_attr)
		if len(file_name) > 0:
			return '%s (%s)' % (file_name, self.obj.executable_name)
		else:
			return self.obj.executable_name

	def obj_file_name_changed(self):
		self.name = self._name_default()

	def create_ui(self, parent):
		return self.obj.edit(kind='panel', parent=parent)	

	def destroy_control(self):
#		""" Destroy the toolkit-specific control that represents the part. """
		''' Overriding pyface.workbench.editor.Editor.destroy_control because 
		self.control can become none after self.control.close() and therefore 
		before self.control.deleteLater()
		'''

		if self.control is not None:
			self.control.hide()
			self.control.close()
#			if self.control is None:
#				print "self.control is None"
#			elif not hasattr(self.control, 'deleteLater'):
#				print "not hasattr(%s, 'deleteLater')" % self.control
			if self.control is not None:
				self.control.deleteLater()
			self.control = None

		return