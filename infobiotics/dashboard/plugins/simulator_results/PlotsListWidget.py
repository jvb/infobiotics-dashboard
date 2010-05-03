# This file is part of the Infobiotics Dashboard. See LICENSE for copyright.
# $Id: PlotsListWidget.py 342 2009-09-09 11:49:07Z jvb $
# $HeadURL: https://psiren.cs.nott.ac.uk/repos/infobiotics/gui/trunk/src/simulator_results/PlotsListWidget.py $
# $Author: jvb $
# $Revision: 342 $
# $Date: 2009-09-09 12:49:07 +0100 (Wed, 09 Sep 2009) $


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
        self.hideInvariants = True
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
        if plot.invariant():
            item.setHidden(True) #TODO is this ideal?
