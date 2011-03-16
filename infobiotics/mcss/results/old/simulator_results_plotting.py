#        plots = []
#        if averaging:
#            for ci, c in enumerate(compartments):
#                for si, s in enumerate(species):
#                    plot = Plot(
#                        timepoints=timepoints,
#                        levels=amounts[mean_index][si, ci],
##                        yerr=errors[si,ci],
#                        species=s.data,
#                        compartment=c.data,
#                        colour=colours.colour(si),
#                    )
#                    plots.append(plot)
#
#        else:
#            for ri, r in enumerate(runs):
#                for ci, c in enumerate(compartments):
#                    for si, s in enumerate(species):
#                        colour = colours.colour(si)
#                        plot = Plot(
#                            timepoints=timepoints,
#                            levels=amounts[ri][si, ci, :],
#                            run=r.data,
#                            species=s.data,
#                            compartment=c.data,
#                            colour=colour,
#                        )
#                        plots.append(plot)
#                    if self.volumes_selected:
#                        colour = colours.colour(len(species) + 1)
#                        plot = VolumePlot(
#                            timepoints=timepoints,
#                            levels=volumes[ri][ci, :],
#                            run=r.data,
#                            compartment=c.data,
#                            colour=colour,
#                        )
#                        plots.append(plot)
#
#        if len(plots) > 0:
#            self.plotsPreviewDialog = PlotsPreviewDialog(
#                runs=len(runs),
#                averaging=averaging,
#                windowTitle=os.path.basename(self.simulation.model_input_file),
#            )
#            if self.plotsPreviewDialog.addPlots(plots):
#    #            if len(plots) > 8:
#    #                self.plotsPreviewDialog.showMaximized()
#    #            else:
#                centre_window(self.plotsPreviewDialog)
#                self.plotsPreviewDialog.show()
#                # bring to fore (needed in this order)
#                self.plotsPreviewDialog.raise_()
#                self.plotsPreviewDialog.activateWindow()
#                return self.plotsPreviewDialog
#            else:
#                self.plotsPreviewDialog.combine()
#                self.plotsPreviewDialog.close()
#
##        # deprecated because Jamie's Ctrl-C signal handling fixes it. But what about crashes?        
##        try:
##            # all of the above
##        except ZeroDivisionError, e:
##            QMessageBox.warning(self, QString(u"Error"),
##                                QString(u'There was a problem processing the simulation data.\n%s\nMaybe the simulation was aborted.\nTry rerunning the simulation and letting it finish.' % e))
##        finally:
##            # reset mouse pointer
##            self.setCursor(Qt.ArrowCursor)
#
#class Plot(object): #rename to timeseries
#    def __init__(self, timepoints, levels, colour, species, compartment, run=None, yerr=None, width=5, height=5, dpi=100):
#        '''
#        
#        run == None when averaging over runs
#        
#        '''
#        self.figure = Figure(figsize=(width, height), dpi=dpi)
#        self.canvas = FigureCanvasAgg(self.figure) #TODO remove?
#        self.timepoints = timepoints
#        self.levels = levels
#        self.yerr = yerr
#        self.run = run
#        self.colour = colour
#        self.species = species
#        self.compartment = compartment
#        self.setup()
#
#    def setup(self):
#        #self.axes.hold(False) clear every time plot() is called
#        self.axes = self.figure.add_subplot(111)
#        self.axes.plot(self.timepoints, self.levels, color=self.colour, label=self.label)
#        self.axes.set_xlabel('time')# %s' % self.units)
#        self.axes.set_ylabel('molecules')
#        self.axes.set_title(self.label)
#        #self.axes.legend()
#
#    def get_label(self):
#        compartment_name_and_xy_coords = self.compartment.compartment_name_and_xy_coords()
#        if self.run == None:
#            return "%s in %s" % (self.species.name, compartment_name_and_xy_coords)
#        else:
#            return "%s in %s of run %s" % (self.species.name, compartment_name_and_xy_coords, self.run._run_number)
#
#    label = property(get_label)
#
##    def least(self):
##        return np.min(self.levels)
##
##    def most(self):
##        return np.max(self.levels)
##
##    def invariant(self):
##        return (True if self.least() == self.most() else False)
##
##    def zeros(self):
##        return (True if self.least() == 0 and self.most() == 0 else False)
#
#    def pixmap(self):
#        fileLikeObject = StringIO.StringIO()
#        self.png(fileLikeObject)
#        pixmap = QPixmap()
#        succeeded = pixmap.loadFromData(fileLikeObject.getvalue(), "PNG")
#        fileLikeObject.close()
#        if succeeded:
#            return pixmap
#        else:
#            return None
#
#    def png(self, filename, dpi=100):
#        self.figure.savefig(filename, format='png')
#
#    def eps(self, filename, dpi=300):
#        #TODO do something with dpi
#        self.figure.savefig(filename, format='eps')
#
#
#class VolumePlot(Plot):
#    def __init__(self, timepoints, levels, colour, compartment, run=None, yerr=None, width=5, height=5, dpi=100):
#        class Species(object):
#            def __init__(self, name):
#                self.name = name
#        super(VolumePlot, self).__init__(timepoints, levels, colour, Species(name='Volumes'), compartment, run, yerr, width, height, dpi)
#        
#    def setup(self):
#        self.axes = self.figure.add_subplot(111)
#        self.axes.plot(self.timepoints, self.levels, color=self.colour, label=self.label)
#        self.axes.set_xlabel('Time')
#        self.axes.set_ylabel('Volume')
#        self.axes.set_title(self.label)
#        
#    def get_label(self):
#        compartment_name_and_xy_coords = self.compartment.compartment_name_and_xy_coords()
#        if self.run == None:
#            return "Volume of %s" % compartment_name_and_xy_coords
#        else:
#            return "Volume of %s in run %s" % (compartment_name_and_xy_coords, self.run._run_number)
#    
#    label = property(get_label)        
#        
#
## adapted from Pawel's tiling code
#def arrange(number):
#    """ Returns the smallest rows x columns tuple for a given number of items. """
#    rows = math.sqrt(number / math.sqrt(2))
#    cols = rows * math.sqrt(2)
#    # finds lowest integer combination of rows and columns, thanks Pawel 
#    if number <= math.ceil(rows) * math.floor(cols):
#        rows = int(math.ceil(rows))
#        cols = int(math.floor(cols))
#    elif number <= math.floor(rows) * math.ceil(cols):
#        rows = int(math.floor(rows))
#        cols = int(math.ceil(cols))
#    else:
#        rows = int(math.ceil(rows))
#        cols = int(math.ceil(cols))
#    return (rows, cols)
#
#
#from enthought.traits.api import Bool
#
#class TraitsPlot(HasTraits):
#    figure = Instance(Figure, ())
#    title = Str('title')
#    show_individual_legends = Bool
#    show_figure_legend = Bool
#
#    def _show_figure_legend_changed(self, value):
#        if value:
#            pass#self.figure.legend()
#        else:
#            self.figure.legend_ = None
#
#    def traits_view(self):
#        return View(
#            VGroup(
#                Item('figure',
#                    show_label=False,
#                    editor=MatplotlibFigureEditor(
#                        toolbar=True
#                    ),
#                ),
#                HGroup(
#                    'show_individual_legends',
#                    'show_figure_legend',
#                    Spring(),
#                    Item('save_resized', show_label=False),
#                ),
#                show_border=True,
#            ),
#            width=640, height=480,
#            resizable=True,
#            title=self.title
#        )
#
#    save_resized = Button
#    def _save_resized_fired(self):
#        resize_and_save_matplotlib_figure(self.figure)
#
#
#class PlotsPreviewDialog(QWidget):
#
#    def __init__(self, runs=1, averaging=False, windowTitle=None, parent=None):
#        if parent != None:
#            QObject.setParent(self, parent)
#        QWidget.__init__(self)
#        self._runs_list = runs
#        self.averaging = averaging
#        self.fontManager = font_manager.FontProperties(size='medium')#'small')
#        self.windowTitle = windowTitle
#        self.ui = Ui_PlotsPreviewDialog()
#        self.ui.setupUi(self)
#        self.connect(self.ui.combineButton, SIGNAL("clicked()"), self.combine)
#        self.connect(self.ui.stackButton, SIGNAL("clicked()"), self.stack)
#        self.connect(self.ui.tileButton, SIGNAL("clicked()"), self.tile)
#        self.connect(self.ui.plotsListWidget, SIGNAL("itemSelectionChanged()"), self.update_ui)
#        self.update_ui()
##        self.traits_plot_list = [] #TODO remove
#
#    def update_ui(self):
#        # disable buttons and create handle lists
#        self.items = self.ui.plotsListWidget.selectedItems()
#        if len(self.items) == 0:
#            self.ui.combineButton.setEnabled(False)
#            self.ui.stackButton.setEnabled(False)
#            self.ui.tileButton.setEnabled(False)
#        else:
#            self.ui.combineButton.setEnabled(True) #TODO singles?
#            self.ui.stackButton.setEnabled(True)
#            self.ui.tileButton.setEnabled(True)
#        # lists of handles for figurelegend()
#        self.lines = []
#        self.errorbars = []
#
#    def addPlots(self, plots):
#        self.ui.plotsListWidget.addPlots(plots)
#        # select lone plot
#        if self.ui.plotsListWidget.count() == 1:
#            self.ui.plotsListWidget.selectAll()
#            return False
#        else:
#            self.ui.plotsListWidget.clearSelection()
#            return True
#
#    def reset(self):
##        pyplot.close()
#        self.traits_plot = TraitsPlot()
##        self.traits_plot_list.append(self.traits_plot) #FIXME keeping a reference seems to cause a Qt crash, but not keeping it will lead to GC, wtf?
##        print self.traits_plot_list #TODO remove and above
#        self.figure = self.traits_plot.figure
##        self.axes = None
#        self.no_labels = False
#        self.labels_and_title()
#
#    def labels_and_title(self):
#        species = [item.plot.species for item in self.items]
#        compartments = [item.plot.compartment for item in self.items]
#        single_species = True if len(set(species)) == 1 else False
#        single_compartment = True if len(set(compartments)) == 1 else False
#        # check if only 1 species
#        single_run = True if self._runs_list == 1 else False
#        title = ""
#        if single_run:
#            if single_species:
#                # check if only 1 compartment
#                if single_compartment:
#                    title = "%s in %s (1 run)" % (item.plot.species.name, item.plot.compartment.compartment_name_and_xy_coords())
#                    for item in self.items:
#                        item.label = None
#                        self.no_labels = True
#                else:
#                    title = "%s (1 run)" % (item.plot.species.name)
#                    for item in self.items:
#                        item.label = item.plot.compartment.compartment_name_and_xy_coords()
#            else:
#                if single_compartment:
#                    title = "%s (1 run)" % (item.plot.compartment.compartment_name_and_xy_coords())
#                    for item in self.items:
#                        item.label = item.plot.species.name
#                else:
#                    title = "1 run"
#                    for item in self.items:
#                        item.label = "%s in %s" % (item.plot.species.name, item.plot.compartment.compartment_name_and_xy_coords())
#        else:
#            if self.averaging:
#                if single_species:
#                    if single_compartment:
#                        title = "%s in %s (mean of %s runs)" % (item.plot.species.name, item.plot.compartment.compartment_name_and_xy_coords(), self._runs_list)
#                        for item in self.items:
#                            item.label = None
#                            self.no_labels = True
#                    else:
#                        title = "%s (mean of %s runs)" % (item.plot.species.name, self._runs_list)
#                        for item in self.items:
#                            item.label = "%s" % (item.plot.compartment.compartment_name_and_xy_coords())
#                else:
#                    if single_compartment:
#                        title = "%s (mean of %s runs)" % (item.plot.compartment.compartment_name_and_xy_coords(), self._runs_list)
#                        for item in self.items:
#                            item.label = "%s" % (item.plot.species.name)
#                    else:
#                        title = "Mean of %s runs" % (self._runs_list)
#                        for item in self.items:
#                            item.label = "%s in %s" % (item.plot.species.name, item.plot.compartment.compartment_name_and_xy_coords())
#            else:
#                if single_species:
#                    if single_compartment:
#                        title = "%s in %s  (%s runs)" % (item.plot.species.name, item.plot.compartment.compartment_name_and_xy_coords(), self._runs_list)
#                        for item in self.items:
#                            item.label = "Run %s" % item.plot.run._run_number
#                    else:
#                        title = "%s (%s runs)" % (item.plot.species.name, self._runs_list)
#                        for item in self.items:
#                            item.label = "%s (run %s)" % (item.plot.compartment.compartment_name_and_xy_coords(), item.plot.run._run_number)
#                else:
#                    if single_compartment:
#                        title = "%s (%s runs)" % (item.plot.compartment.compartment_name_and_xy_coords(), self._runs_list)
#                        for item in self.items:
#                            item.label = "%s (run %s)" % (item.plot.species.name, item.plot.run._run_number)
#                    else:
#                        title = "%s runs" % (self._runs_list)
#                        for item in self.items:
#                            item.label = "%s in %s (run %s)" % (item.plot.species.name, item.plot.compartment.compartment_name_and_xy_coords(), item.plot.run._run_number)
#        # set main title
##        pyplot.suptitle(title)
#        self.figure.suptitle(title)        
#
#
#    def combine(self):
#        """different colours for all lines"""
#        self.reset()
#
#        # determine if some volumes but not (no volumes or all volumes)
#        volumes = 0
#        for item in self.items:
#            if item.plot.species.name == 'Volumes':
#                volumes += 1
#        if 0 < volumes < len(self.items):
#            some_volumes = True
#        else:
#            some_volumes = False
#
#        if not some_volumes: # either all volumes or no volumes
#            # plot all on 1st y-axis
#            for i, item in enumerate(self.items):
##                pyplot.xlabel("time (%s)" % item.plot.units)
##                pyplot.ylabel("molecules")
#                self.axes = self.figure.add_subplot(111) #FIXME move this out of loop?
#                self.axes.set_xlabel("time")# (%s)" % item.plot.units)
#                self.axes.set_ylabel("molecules") #TODO concentration
#                colour = colours.colour(i)
#                self.line(self.axes, item, colour)
#                if self.averaging:
#                    self.errorbar(item, colour)
#        else:
#            # mix, plot species on 1st y-axis and volumes on 2nd y-axis
#            not_volumes = [item for item in self.items if item.plot.species.name != 'Volumes']
#            volumes = [item for item in self.items if item.plot.species.name == 'Volumes']
#            self.axes = self.figure.add_subplot(111)
#            self.axes.set_xlabel("time")# (%s)" % item.plot.units)
#            self.axes.set_ylabel("molecules")
#            for i, item in enumerate(not_volumes):
##                pyplot.xlabel("time (%s)" % item.plot.units)
##                pyplot.ylabel("molecules")
#                colour = colours.colour(i)
#                self.line(self.axes, item, colour)
#                if self.averaging:
#                    self.errorbar(item, colour)
#            axes = self.axes.twinx()
#            for i, item in enumerate(volumes):
#                i += len(not_volumes)
##                axes.set_xlabel("time")# (%s)" % item.plot.units)
#                axes.set_ylabel("Volumes")
#                colour = colours.colour(i)
#                self.line(axes, item, colour)
#                if self.averaging:
#                    self.errorbar(item, colour)
#            
#        if not self.no_labels: self.legend() #TODO
#
#        self.finalise()
#
#
#    def stack(self):
#        """same colour for each species (legend), _compartments_list title"""
#        self.reset()
#        rows = len(self.items)
#        cols = 1
#        for i, item in enumerate(self.items):
#            if i == 0:
#                self.sharedAxis = self.figure.add_subplot(rows, cols, rows - i)
#                self.axes = self.sharedAxis
#                self.sharedAxis.set_xlabel("time")# (%s)" % item.plot.units)
#                self.line(self.axes, item)
#                if self.averaging:
#                    self.errorbar(item)
#            else:
#                self.axes = self.figure.add_subplot(rows, cols, rows - i, sharex=self.sharedAxis)
##                pyplot.setp(self.axes.get_xticklabels(), visible=False) #TODO
#                self.line(self.axes, item)
#                if self.averaging:
#                    self.errorbar(item)
#            if len(self.items) < 6: #TODO 6 is a bit arbitary  
#                self.axes.set_ylabel("molecules") #TODO change for volumes/concentration
#            
#            if not self.no_labels: self.legend() #TODO
#        
#        self.finalise()
#
#
#    def tile(self):
#        """same colours for each species (legend), _compartments_list title"""
#        self.reset()
#        rows, cols = arrange(len(self.items))
#        for i, item in enumerate(self.items):
#            self.axes = self.figure.add_subplot(rows, cols, i + 1)
#            self.axes.set_xlabel("time")# (%s)" % item.plot.units)
#            self.axes.set_ylabel("molecules")
#            self.line(self.axes, item)
#            if self.averaging:
#                self.errorbar(item)
#
#            if not self.no_labels: self.legend() #TODO
#        
#        self.finalise()
#
#    def line(self, axes, item, colour=None):
#        lines = axes.plot(
#            item.plot.timepoints,
#            item.plot.levels,
#            label=item.label,
#            color=colour if colour is not None else item.plot.colour,
#        )
#        self.lines.append((lines[0], item.label))
#
#    def errorbar(self, item, colour=None):
#        return #TODO
##        step = int(len(timepoints) / 10)
##        errorbar = pyplot.errorbar( #TODO
##            item.plot.timepoints[::step], 
##            item.plot.levels[::step],
##            yerr=item.plot.yerr[::step],
##            label=None,#item.plot.label
##            color=colour if colour is not None else item.plot.colour,
##            fmt=None, 
##            linestyle=None, 
##            capsize=0
##        )
##        self.errorbars.append(errorbar)
#
#    def legend(self):
##        self.axes.legend(loc=0, prop=self.fontManager)
#        pass
##        from infobiotics.commons.matplotlib.draggable_legend import DraggableLegend
###        legend = DraggableLegend(ax.legend())
##        legend = self.axes.legend(loc=0, prop=self.fontManager)
##        print self.traits_plot.figure.canvas
##        legend.canvas = self.traits_plot.figure.canvas
##        DraggableLegend(legend) # fails because legend.figure.canvas is None
#        
#
#    def figurelegend(self): #FIXME use this
#        """Create a legend for all subplots."""
#        lines = [line for line, label in self.lines]
#        labels = [label for line, label in self.lines]
#        legend = self.figure.legend(lines, labels, loc='right', prop=self.fontManager)
##        legend.draggable(True) #TODO test for new matplotlib version before setting
#
#    def background(self):
#        """Change figure background."""
##        pyplot.gcf().set_facecolor("whitesmoke")
#        self.figure.set_facecolor("whitesmoke")
#
#    def finalise(self):
#
#        self.figurelegend()
#
#        self.lines = []
#        self.errorbars = []
#
#        self.background()
#
#        if self.windowTitle is not None:
#            self.traits_plot.title = self.windowTitle
#
#        # http://www.mail-archive.com/pyqt@riverbankcomputing.com/msg16645.html
#        from PyQt4.QtCore import QAbstractEventDispatcher 
#        if QAbstractEventDispatcher.instance() != 0:
#            self.traits_plot.edit_traits()
#        else:
#            self.traits_plot.configure_traits()
