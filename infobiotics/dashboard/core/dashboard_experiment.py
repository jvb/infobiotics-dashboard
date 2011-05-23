from has_infobiotics_dashboard_workbench_application import HasInfobioticsDashboardWorkbenchApplication
from enthought.traits.api import Str, Property, Instance
from PyQt4.QtGui import QWidget

class DashboardExperiment(HasInfobioticsDashboardWorkbenchApplication):
    
    _interaction_mode = Str('gui') # overrides _interaction_mode in Params but means that DashboardExperiment must be imported before McssDashboardExperiment for example 

    _parent_widget = Property(Instance(QWidget))

    def _get__parent_widget(self):
        return self.application.workbench.active_window.control
    
    def _stderr_pattern_matched(self, pattern_index, match):
        pattern = match.group()
        self._errors += ':\n%s' % pattern.strip()
        if pattern_index == 5:
            d = match.groupdict()
            print 'file="%s" line=%s' % (d['file'], d['line']) #TODO open editor at this line
            