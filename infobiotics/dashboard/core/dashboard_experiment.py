from infobiotics.dashboard.api import InfobioticsDashboardWorkbenchApplication
from traits.api import HasTraits, Instance, Str, Property
from PyQt4.QtGui import QWidget
from envisage.plugins.text_editor.editor.text_editor import TextEditor
from apptools.io.api import File
import os.path

#from pyface.api import GUI
from pyface.gui import GUI

class DashboardExperiment(HasTraits):

    application = Instance(InfobioticsDashboardWorkbenchApplication)
       
    _interaction_mode = Str('gui') # overrides _interaction_mode in Params but means that DashboardExperiment must be imported before McssDashboardExperiment for example 

    _parent_widget = Property(Instance(QWidget))

    def _get__parent_widget(self):
        return self.application.workbench.active_window.control
#        return None #TODO check
    
    def _stderr_pattern_matched(self, pattern_index, match):
        pattern = match.group()
        self._errors += '\n%s' % pattern.strip()
        if pattern_index == 5:
            groupdict = match.groupdict()
            GUI.invoke_later(self.open_file_at_erroneous_line, groupdict)

    def open_file_at_erroneous_line(self, groupdict):
        text_editor = self.application.workbench.active_window.edit(
            obj=File(os.path.normpath(os.path.join(self.directory, groupdict['file']))),
            kind=TextEditor,
            use_existing=True
        )
        text_editor.select_line(int(groupdict['line']))
            
