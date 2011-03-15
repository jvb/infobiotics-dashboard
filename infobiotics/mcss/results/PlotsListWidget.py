from PyQt4.QtGui import QListWidget, QListWidgetItem, QIcon


class PlotsListWidget(QListWidget):

    def __init__(self, parent=None, plots=None):
        QListWidget.__init__(self, parent)
#        # default settings now done in PlotsPreviewDialog.ui
#        self.setViewMode(QListView.IconMode)
#        self.setAcceptDrops(False)
#        self.setFlow(QListWidget.LeftToRight)
#        self.setWrapping(True)
#        self.setResizeMode(QListView.Adjust)
#        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        #self.setIconSize(QSize(200,200))
#        self.hideInvariants = True
        #TODO implement/connect hide invariants checkbox in PlotsPreviewDialog
        self.addPlots(plots)

    def addPlots(self, plots):
        if plots is not None:
            for plot in plots:
                self.addPlot(plot)

    def addPlot(self, plot):
        item = QListWidgetItem(self)
        item.plot = plot
        item.setIcon(QIcon(plot.pixmap()))
#        if plot.invariant():
#            item.setHidden(True) #TODO is this ideal?
