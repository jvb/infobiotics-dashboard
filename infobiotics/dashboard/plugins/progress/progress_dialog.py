from enthought.pyface.api import ProgressDialog as PyFaceProgressDialog
from i_progress_meter import IProgressMeter
from enthought.traits.api import implements, Bool, Long
from PyQt4.QtCore import SIGNAL

class ProgressDialog(PyFaceProgressDialog):
    implements(IProgressMeter)
    
    cancelled = Bool(False)
    
    def _create_buttons(self, dialog, layout):
        super(ProgressDialog, self)._create_buttons(dialog, layout)
        
        # make Cancel button set self.cancelled
        dialog.connect(dialog, SIGNAL('rejected()'), self.cancel)
        
        # remove OK button
        buttons = layout.itemAt(layout.count()-1).widget()
        buttons.removeButton(buttons.buttons()[0])
        
    def cancel(self):
        self.cancelled = True
