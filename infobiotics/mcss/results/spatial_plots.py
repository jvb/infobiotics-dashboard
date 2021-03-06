from __future__ import division
#import sip
#sip.setapi('QString', 2)
from traits.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'qt4'
from traits.api import *
from traitsui.api import View, Item, VGroup
from mayavi.core.pipeline_base import PipelineBase
from mayavi.core.ui.mayavi_scene import MayaviScene
from mayavi.tools.mlab_scene_model import MlabSceneModel
from tvtk.pyface.scene_editor import SceneEditor
import numpy as np
from PyQt4.QtGui import (
    QWidget, QHBoxLayout, QGridLayout, QVBoxLayout, QPushButton, QListWidget, 
    QPixmap, QListWidgetItem, QIcon, QLabel, QFileDialog, QSlider, QMessageBox, 
    QProgressDialog
)
from PyQt4.QtCore import Qt, SIGNAL, QSize, QFileInfo, QTimer, SLOT
from infobiotics.commons.qt4 import centre_window
import cStringIO as StringIO
from ui_player_control_widget import Ui_ControlsWidget
from infobiotics.commons.sequences import arrange
import os.path
from infobiotics.commons.qt4 import open_file

can_record = False
try:
    import movie
    can_record = True
except EnvironmentError, e:
    '''Enables movie module to quit prematurely without taking us down too'''
    pass
if can_record:
    import Image


class SpatialPlotsWindow(QWidget):
    def __init__(self, surfaces, parent=None):
        QWidget.__init__(self)

        self.setAttribute(Qt.WA_DeleteOnClose)

        self.connect(parent, SIGNAL("destroyed(QObject*)"), self.close)
        self.filename = parent.filename

        self.setWindowTitle('%s surfaces' % os.path.basename(unicode(self.filename)))

        self.surfaces = surfaces
        h = QHBoxLayout()
        h.setSpacing(0)
        self.widgets = []
        for surface in self.surfaces:
            self.widgets.append(surface.edit_traits(kind='subpanel').control) #TODO edit_traits(kind='panel')?
            
#        # sync cameras #TODO button
#        if len(self.surfaces) > 1:
#            figure = self.surfaces[0].scene.mayavi_scene
#            mlab = self.surfaces[0].scene.mlab 
#            for surface in self.surfaces[1:]:
#                mlab.sync_camera(figure, surface.scene.mayavi_scene)
            
        gridLayout = QGridLayout()
        gridLayout.setHorizontalSpacing(6)
        gridLayout.setVerticalSpacing(6)
        rows, cols = arrange(self.surfaces)
        if len(self.widgets) == 3:
            for i, widget in enumerate(self.widgets):
                gridLayout.addWidget(widget, 0, i)
        else:
            for i, widget in enumerate(self.widgets):
                gridLayout.addWidget(widget, i // rows, i % rows) 
        v = QVBoxLayout()
        v.setSpacing(0)
        v.addLayout(gridLayout)

        self.controls = SpatialPlotsControlsWidget(surfaces, parent=self)
        v.addWidget(self.controls)
        v.addSpacing(6)
        h2 = QHBoxLayout()
        h2.addStretch()
        if len(self.surfaces) > 1:
            compareButton = QPushButton('Compare')
            self.connect(compareButton, SIGNAL('clicked()'), self.createSurfacesListWidget)
            h2.addWidget(compareButton)
        self.saveDataButton = QPushButton('Save Data')
        self.saveDataButton.setToolTip('Save surface data in uncompressed NumPy .npz format')
        self.connect(self.saveDataButton, SIGNAL('clicked()'), self.saveData)
        h2.addWidget(self.saveDataButton)
        v.addLayout(h2)
        self.setLayout(v)

    def createSurfacesListWidget(self):
        position = self.controls.getPosition()
        self.surfacesListWidget = SurfacesListWidget(self.surfaces, position, self)
        self.surfacesListWidget.show()

    def saveData(self):
        file = self.filename+'_surfaces.npz'
        try: #REMOVE
            file = QFileDialog.getSaveFileName(self, 'Specify a filename to save data to', file, 'NumPy files (*.npz)')
            if file != '':
                kwargs = dict((
                    str(s.species_name).replace(' (mean)','_mean'), 
                    s.array
                ) for s in self.surfaces)
                np.savez(str(file), **kwargs)
                self.saveDataButton.setText('Saved')
                self.saveDataButton.setToolTip(file)
                self.saveDataButton.setEnabled(False)
        except Exception, e:
            self.saveDataButton.setText('Failed')
            self.saveDataButton.setToolTip(str(e))
            self.saveDataButton.setEnabled(False)
            
class SurfacesListWidget(QWidget):
    def __init__(self, surfaces, position, parent):
        QWidget.__init__(self)
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.parent = parent

        self.surfaces = surfaces
        self.position = position
        #TODO position to time

        self.setWindowTitle('Surfaces at position %s' % self.position)

        self.setupUi()

        self.update_ui()


    def setupUi(self):

        self.listWidget = QListWidget(self)
        self.listWidget.setViewMode(QListWidget.IconMode)
        self.listWidget.setSelectionMode(QListWidget.ExtendedSelection)
        self.listWidget.setSelectionBehavior(QListWidget.SelectItems)
        self.listWidget.setIconSize(QSize(200, 200))
#        self.listWidget.setDragDropMode(QListWidget.InternalMove)
#        self.listWidget.setDragEnabled(True)
        self.listWidget.setUniformItemSizes(True)

        for surface in self.surfaces:
            array = surface.arrayAtPosition(self.position)
            fileLikeObject = StringIO.StringIO()
            save_array_as_image(fileLikeObject, array, format='PNG')
            pixmap = QPixmap()
            succeeded = pixmap.loadFromData(fileLikeObject.getvalue(), "PNG")
            fileLikeObject.close()
            if succeeded:
                pixmap = pixmap.scaledToWidth(100)
                item = QListWidgetItem(surface.species_name, self.listWidget)
                item.setIcon(QIcon(pixmap))
                item.surface = surface

        self.connect(self.listWidget, SIGNAL('itemSelectionChanged()'), self.update_ui)
        self.connect(self.listWidget, SIGNAL('itemDoubleClicked(QListWidgetItem *)'), self.showItem)

        self.overlapPairwiseButton = QPushButton('Overlap pairwise', self)
        self.connect(self.overlapPairwiseButton, SIGNAL('clicked()'), self.overlapPairwise)

        self.v = QVBoxLayout(self)
        self.v.addWidget(self.listWidget)
        self.v.addWidget(self.overlapPairwiseButton)
        # next index for v is 2

        self.secondListWidget = QListWidget(self)
        self.secondListWidget.setViewMode(QListWidget.IconMode)
        self.secondListWidget.setSelectionMode(QListWidget.ExtendedSelection)
        self.secondListWidget.setSelectionBehavior(QListWidget.SelectItems)
        self.secondListWidget.setIconSize(QSize(200, 200))
#        self.secondListWidget.setDragDropMode(QListWidget.InternalMove)
#        self.secondListWidget.setDragEnabled(True)
        self.secondListWidget.setUniformItemSizes(True)

        self.connect(self.secondListWidget, SIGNAL('itemSelectionChanged()'), self.update_ui)
        self.connect(self.secondListWidget, SIGNAL('itemDoubleClicked(QListWidgetItem *)'), self.showItem)
        self.saveSelectedButton = QPushButton('Save selected', self)
        self.connect(self.saveSelectedButton, SIGNAL('clicked()'), self.saveSelected)
        self.saveAllSelectedButton = QPushButton('Save all selected', self)
        self.connect(self.saveAllSelectedButton, SIGNAL('clicked()'), self.saveAllSelected)

        self.v.addWidget(self.secondListWidget)
        h = QHBoxLayout()
        h.addWidget(self.saveSelectedButton)
        h.addWidget(self.saveAllSelectedButton)
        self.v.addLayout(h)

        self.setLayout(self.v)

        self.resize(640, 480)
        centre_window(self)


    def showItem(self, item):
        self.label = QLabel(self, Qt.Window)
        self.label.setWindowTitle(item.text())
        icon = item.icon()
        self.label.setPixmap(icon.pixmap(400, 400))
        self.label.setScaledContents(True)
        self.label.setToolTip('Drag to resize image, right-click to save.')
        pixmap = self.label.pixmap()
        self.label.resize(pixmap.width() * 4, pixmap.height() * 4)
        centre_window(self.label)
        self.label.show()
        self.label.setContextMenuPolicy(Qt.CustomContextMenu)
        self.connect(self.label, SIGNAL('customContextMenuRequested(const QPoint &)'), self.saveLabel)

    def saveLabel(self):
        filename = self.getSaveFilename(self.label.windowTitle())
        if filename != '':
            if not filename.endsWith('.png', Qt.CaseInsensitive):
                filename = '%s.png' % filename
            pixmap = self.label.pixmap().scaled(self.label.size())
            pixmap.save(filename, 'png')
            self.lastDirectory = QFileInfo(filename).absolutePath()

    def getSaveFilename(self, filename):
        if hasattr(self, 'lastDirectory'):
            filename = '%s/%s' % (self.lastDirectory, filename)
        filename = QFileDialog.getSaveFileName(self, 'Specify a filename to save image to', filename, 'PNG files (*.png)')
        if filename != '':
            if not filename.endsWith('.png', Qt.CaseInsensitive):
                filename = '%s.png' % filename
            self.lastDirectory = QFileInfo(filename).absolutePath()
        return filename


    def update_ui(self):
        self.overlapPairwiseButton.setEnabled(len(self.listWidget.selectedItems()) > 1)
        self.saveSelectedButton.setEnabled(len(self.secondListWidget.selectedItems()) == 1)
        self.saveAllSelectedButton.setEnabled(len(self.secondListWidget.selectedItems()) > 0)

    def overlapPairwise(self):
#        # remove secondListWidget 
#        layoutItem = self.v.itemAt(2)
#        if layoutItem != 0:
#            self.v.removeItem(layoutItem)
#        self.v.addWidget(self.secondListWidget)

        self.secondListWidget.clear()

        surfaces = [item.surface for item in self.listWidget.selectedItems()]

        import itertools
        for pair in itertools.combinations(surfaces, 2):
            s1 = pair[0]
            s2 = pair[1]
            array1 = s1.arrayAtPosition(self.position)
            array2 = s2.arrayAtPosition(self.position) * -1
            array = array1 + array2

            fileLikeObject = StringIO.StringIO()
            save_array_as_image(fileLikeObject, array, format='PNG')
            pixmap = QPixmap()
            succeeded = pixmap.loadFromData(fileLikeObject.getvalue(), "PNG")
            fileLikeObject.close()
            if succeeded:
                pixmap = pixmap.scaledToWidth(100)
                item = QListWidgetItem('%s+%s' % (s1.species_name, s2.species_name), self.secondListWidget)
                item.setIcon(QIcon(pixmap))
                info = QFileInfo(self.parent.filename)
                item.filename = '%s+%s_%s_%s.png' % (s1.species_name, s2.species_name, self.position, info.fileName())
                item.array = array

    def saveSelected(self):
        item = self.secondListWidget.selectedItems()[0]
        filename = self.getSaveFilename(item.text())
        if filename != '':
            save_array_as_image(filename, item.array, format='png')

    def saveAllSelected(self):
        directory = QFileDialog.getExistingDirectory(self, 'Specify a directory to save images to')
        if directory != '':
            items = self.secondListWidget.selectedItems()
            for item in items:
                save_array_as_image('%s/%s' % (directory, item.filename), item.array)


def save_array_as_image(filename, array, colourmap=None, vmin=None, vmax=None, format=None, origin=None):
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    from matplotlib import cm

    figure = Figure(figsize=array.shape[::-1], dpi=1, frameon=False)
#    canvas = FigureCanvas(figure) # essential even though it isn't used
    FigureCanvas(figure) # essential even though it isn't used
    figure.figimage(array, cmap=cm.get_cmap(colourmap), vmin=vmin, vmax=vmax, origin=origin)
    figure.savefig(filename, dpi=1, format=format)


class ControlsWidget(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = Ui_ControlsWidget()
        self.ui.setupUi(self)
        self.maximum = self.ui.positionSlider.maximum()
        self.position = 0
        self.timer = QTimer(self)
        self.connect(self.timer, SIGNAL("timeout()"), self.next_position);
        self.reset()
        self.connect(self.ui.playPauseButton, SIGNAL("clicked()"), self.playPauseButton_clicked)
        self.connect(self.ui.positionSlider, SIGNAL("valueChanged(int)"), self.set_position)
        self.connect(self, SIGNAL("position_changed(int)"), self.ui.positionSlider, SLOT("setValue(int)"))

    def reset(self):
        self.set_position(0)
        self.finished = False
        self.pause()

    def pause(self):
        self.paused = True
        self.update_ui()
        self.timer.stop()

    def play(self):
        self.paused = False
        self.update_ui()
        self.timer.start(0) # <-- change this to make steps longer

    def set_position(self, position):
        if self.position != position:
            if 0 <= position <= self.maximum:
                self.position = position
                self.emit(SIGNAL("position_changed(int)"), self.position)
            if self.position == self.maximum:
                self.finished = True
                self.pause()
            else:
                self.finished = False
            self.update_ui()

    def next_position(self):
        self.set_position(self.position + 1)

    def update_ui(self):
        if self.ui.positionSlider.value() == self.maximum:
            self.ui.playPauseButton.setText("Reset")
        else:
            self.ui.playPauseButton.setText("Play") if self.paused else self.ui.playPauseButton.setText("Pause")

    def playPauseButton_clicked(self):
        if self.finished:
            self.reset()
        else:
            self.play() if self.paused else self.pause()


class SpatialPlotsControlsWidget(ControlsWidget):

    def __init__(self, surfaces, parent=None):
        ControlsWidget.__init__(self, parent)
        self.surfaces = surfaces
        self.connect(self, SIGNAL("position_changed(int)"), self.update_surfaces)
        self.maximum = len(surfaces[0].timepoints) - 1
        self.ui.positionSlider.setMaximum(self.maximum)
        self.ui.positionSlider.setTickPosition(QSlider.TicksBelow)
        self.ui.spinBox.setMaximum(self.maximum)

        # remove border
        margin = 0
        self.ui.verticalLayout.setContentsMargins(margin, margin, margin, margin)
        self.ui.horizontalLayout.setContentsMargins(margin, margin, margin, margin)

        self.record_button = QPushButton('Record')
        self.record_button.setCheckable(True)
        self.ui.horizontalLayout.insertWidget(0, self.record_button)
        self.connect(self.record_button, SIGNAL('clicked(bool)'), self.record_button_toggled)
        self.recording = False
        
        # disable recording if ffmpeg not found
        if not can_record: # find 'import movie'
            self.record_button.setEnabled(False)
            self.record_button.setToolTip("Requires 'ffmpeg' to be installed and in system path.")

    def record_button_toggled(self, recording):
        parent = self.parent()
        if recording:
            self.parentmaxsize = parent.maximumSize()
            parent.setFixedSize(parent.size())
            if hasattr(self.surfaces[0], 'species_name'):
                default_filename = ' vs '.join(str(surface.species_name) for surface in self.surfaces)
            else:
                default_filename = ' vs '.join(str(name) for name in self.surfaces[0].species_names)
            filename = QFileDialog.getSaveFileName(
                parent, 
                'Specify a filename to save data to', 
                default_filename,
                movie.QFileDialog_filter_from_available_formats(),
#                'AVI format *.avi (*.avi)'
            )
            filename = str(filename)
            if filename == '':
                self.record_button.setChecked(False)
                return 
            self.movie = movie.movie(
                filename,
                25, #TODO make frame rate an option
                '%012d.png' 
            )
            self.recording = True
            self.record_button.setText('Stop')
            self.connect(self, SIGNAL('surfaces_position_changed'), self.record_frame)
            if hasattr(self.surfaces[0], 'species_name'):
                self.templates = ['%s-%%012d.png' % unicode(surface.species_name) for surface in self.surfaces]
            else:
                self.templates = ['%s-%%012d.png' % unicode(' vs '.join(str(name) for name in self.surfaces[0].species_names))] 
            
            self.record_frame() # snap first frame
        else:
            parent.setMaximumSize(self.parentmaxsize)
            self.disconnect(self, SIGNAL('surfaces_position_changed'), self.record_frame)
            self.pause()
            
            progressDialog = QProgressDialog(
                'Processing recording',
                '',#QString(), # no cancel button,
                0, # min
                2, # join + encode
                parent# = self.parent()
            )
            progressDialog.setWindowModality(Qt.WindowModal)
            progressDialog.setWindowTitle('Processing recording')
            progressDialog.open()
            
            if len(self.templates) > 1:
                progressDialog.setLabelText('Joining surface images into frames')
                # join surfaces together
                tempdir = self.movie.tempdir
                image = Image.open(os.path.join(tempdir, self.templates[0] % 1))
                width, height = image.size
                mode = image.mode
                for i in range(1, self.movie.frames + 1):
                    frames = [os.path.join(tempdir, template % i) for template in self.templates]
                    frame = Image.new(mode, ((width * len(frames)) + (6 * (len(frames) - 1)), height))
                    x = 0
                    for f in frames:
                        try:
                            image = Image.open(f)
                        except IOError, e:
                            break
                        frame.paste(image, (x, 0))
                        x += width + 6
                    filename = os.path.join(tempdir, self.movie.template % i)
                    frame.save(filename)
            else:
                self.movie.template = self.templates[0]
            
            progressDialog.setLabelText("Encoding movie:\n'%s'" % self.movie.filename)
            progressDialog.setValue(1)
            success = self.movie.encode()
            if success:
                progressDialog.setValue(2)
                if QMessageBox.Yes == QMessageBox.question(
                    self.parent(), 
                    'Recording succeeded',
                    'Play recording now?',
                    buttons=QMessageBox.Yes|QMessageBox.No,
                    defaultButton=QMessageBox.No
                ):
                    open_file(self.movie.filename)
            else:
                progressDialog.close()
                QMessageBox.critical(
                    self.parent(),
                    'Recording failed',
                    self.movie.output, 
                    buttons=QMessageBox.Ok)
            del self.movie
            self.recording = False
            self.record_button.setText('Record')

    def record_frame(self):
        for i, surface in enumerate(self.surfaces):
            surface.scene.mlab.savefig(self.movie.next_frame(self.templates[i]), figure=surface.surf)
            
    def update_surfaces(self):
        for surface in self.surfaces:
            surface.set_position(self.position)
        self.emit(SIGNAL('surfaces_position_changed'))

    def getPosition(self):
        return self.ui.positionSlider.value()


class Surface(HasTraits):
    scene = Instance(MlabSceneModel)
    def _scene_default(self):
        return MlabSceneModel()
    
    surf = Instance(PipelineBase) # surf = plot

    def __init__(self, array, warp_scale, extent, species_name, quantities_display_units, timepoints):
        HasTraits.__init__(self)
        self.array = array
        self.warp_scale = warp_scale
        self.extent = extent
        self.species_name = species_name
        self.quantities_display_units = quantities_display_units
        self.timepoints = timepoints
        # create a 'position' trait that enables us to choose the frame
        self.add_trait('position', Range(0, len(timepoints) - 1, 0))

    view = View(
        Item(
            'scene', 
            show_label=False, 
            editor=SceneEditor(scene_class=MayaviScene)
        ),
#        VGroup(
#            'position'#, 'sync_positions'
#        ),
        kind='panel', 
        resizable=True,
    )

    @on_trait_change('scene.activated')
    def create_pipeline(self):
        """ set traits for items in figure """
        self.surf = self.surf_default()
        # some things need to activated here otherwise it crashes

        # doing this somehow fixes the overlapping figures problem in MayaVi2 3.1 that "figure=self.scene.mayavi_scene)" fixes in 3.3
        scalar_bar_widget = self.surf.module_manager.scalar_lut_manager.scalar_bar_widget
        # vtk (>= 5.2)
#        # set position and size of scalarbar
#        # since VTK-5.2 the actual scalarbar widget is accessed through the scalar_bar_widget's representation property 
#        # (see https://mail.enthought.com/pipermail/enthought-dev/2009-May/021342.html)
        scalar_bar_widget.representation.set(position=[0.827, 0.0524], position2=[0.1557, 0.42])

#        f = self.scene.mlab.gcf()
#        camera = f.scene.camera
#        camera.focal_point = (-0.5, -0.5, 0)
#        camera.position = (36.0146, 67.4237, 77.1612)
#        camera.distance = 100
#        self.scene.isometric_view()
    
    def surf_default(self):
        figure=self.scene.mayavi_scene
        
        # create the surf trait, our surface
        surf = self.scene.mlab.surf(self.array[:, :, 0], warp_scale=self.warp_scale, figure=figure)

        # create a title and get handle to it
        self.title = self.scene.mlab.title(self.maketitle(-1), size=0.5, height=0.91, figure=figure)
        self.title = self.scene.mlab.title("%s at 0" % self.species_name, size=0.5, height=0.91, figure=figure)
        self.title.x_position = 0.03
        self.title.actor.width = 0.9 
        self.title.text = self.maketitle(0)

        # create axes showing compartment x,y coordinates and fix text formatting
        axes = self.scene.mlab.axes(ranges=self.extent, xlabel="X", ylabel="Y", figure=figure, z_axis_visibility=False)
        axes.label_text_property.set(italic=0, bold=0)
#        axes.axes.print_traits()
        axes.axes.number_of_labels = 3
        axes.axes.z_axis_visibility = 0
        axes.axes.z_label = ''#self.quantities_display_units

        # create and get a handle to the scalarbar
        scalarbar = self.scene.mlab.scalarbar(None, str(self.quantities_display_units), "vertical", 5, None, '%.f')
        # set scalarbar title and label fonts
        scalarbar.title_text_property.set(font_size=4, italic=0, bold=0)
        scalarbar.label_text_property.set(font_size=4, italic=0, bold=0)#, line_spacing=0.5)
        # vtk (< 5.2)
#        scalarbar.position = [0.832050505051, 0.0348561403509]
#        scalarbar.position2 = value = [0.162034646465, 0.287167919799]

        # set angle scene is viewed from
        self.scene.scene_editor.isometric_view() #WARNING removing this line causes the surface not to display and the axes to rotate 90 degrees vertically!
##        self.scene.mlab.view(-45, 90, 4) # rotated 45 degrees, viewed side on, from a distance of 4  
        # more angle setting in self.create_pipeline()

        return surf

    def maketitle(self, position):
        return '%s at %s' % (self.species_name, round(self.timepoints[self.position], 2))

    # PyQt4 slot
    def set_position(self, position):
        self.position = position

    @on_trait_change('position')
    def update_plot(self):
        self.surf.mlab_source.set(scalars=self.array[:, :, self.position])
        self.scene.mlab.axes(ranges=self.extent, xlabel="X", ylabel="Y", figure=self.scene.mayavi_scene)#, z_axis_visibility=False)
        self.title.text = self.maketitle(self.position)

    def arrayAtPosition(self, position):
        return self.array[:, :, position]

#    def __del__(self):
#        del self.surf


#lut = surf.module_manager.scalar_lut_manager.lut.table.to_array()

blue_to_red_lut_table = np.ndarray((256,4))
blue_to_red_lut_table[:, 0] = np.linspace(0, 255, 256) # red
blue_to_red_lut_table[:, 1] = np.linspace(0, 0, 256) # green
blue_to_red_lut_table[:, 2] = np.linspace(255, 0, 256) # blue
blue_to_red_lut_table[:, 3] = np.linspace(255, 255, 256) # alpha

blue_to_green_lut_table = np.ndarray((256,4))
blue_to_green_lut_table[:, 0] = np.linspace(0, 0, 256) # red
blue_to_green_lut_table[:, 1] = np.linspace(0, 255, 256) # green
blue_to_green_lut_table[:, 2] = np.linspace(255, 0, 256) # blue
blue_to_green_lut_table[:, 3] = np.linspace(255, 255, 256) # alpha

black_to_red_lut_table = np.ndarray((256,4))
#black_to_red_lut_table[:, 0] = np.linspace(0, 255, 256) # red
black_to_red_lut_table[:, 0] = np.concatenate((np.linspace(0, 0, 20), np.linspace(20, 255, 236))) # red
black_to_red_lut_table[:, 1] = np.linspace(0, 0, 256) # green
black_to_red_lut_table[:, 2] = np.linspace(0, 0, 256) # blue
black_to_red_lut_table[:, 3] = np.linspace(255, 255, 256) # alpha

black_to_green_lut_table = np.ndarray((256,4))
black_to_green_lut_table[:, 0] = np.linspace(0, 0, 256) # red
#black_to_green_lut_table[:, 1] = np.linspace(20, 255, 256) # green
black_to_green_lut_table[:, 1] = np.concatenate((np.linspace(0, 0, 20), np.linspace(20, 255, 236))) # green
black_to_green_lut_table[:, 2] = np.linspace(0, 0, 256) # blue
black_to_green_lut_table[:, 3] = np.linspace(255, 255, 256) # alpha

#surf.module_manager.scalar_lut_manager.lut.table = lut
#self.scene.mlab.draw()

class RedVsGreen(Surface):
    
    surfaces = List(Instance(PipelineBase))

    def __init__(self, arrays, extent, species_names, quantities_display_units, timepoints, timepoints_display_units, suffix=None):
        HasTraits.__init__(self)
        self.arrays = arrays
        self.extent = extent
        self.species_names = species_names
        self.quantities_display_units = quantities_display_units
        self.timepoints = timepoints
        self.timepoints_display_units = timepoints_display_units
        self.suffix = suffix
        
        self.add_trait('position', Range(0, len(timepoints) - 1, 0))

    def maketitle(self, position):
        return "%s (green) vs %s (red) at %.1f %s" % (self.species_names[0], self.species_names[1], self.timepoints[position], self.timepoints_display_units)
#        return "Turing Pattern Formation in a Bacterial Population (%.1f %s)" % (self.timepoints[position], self.timepoints_display_units)
#        return "Pulse Inverter"# (%.1f %s)" % (self.timepoints[position], self.timepoints_display_units)

    def surf_default(self, arrayindex):
        figure=self.scene.mayavi_scene
        surf = self.scene.mlab.surf(self.arrays[arrayindex][:, :, 0], warp_scale=(1 / np.max(self.arrays[arrayindex])) * 33, figure=figure)

        lut = surf.module_manager.scalar_lut_manager.lut.table.to_array()
        if arrayindex == 0:
            lut = black_to_green_lut_table
        elif arrayindex == 1:
            lut = black_to_red_lut_table
        surf.module_manager.scalar_lut_manager.lut.table = lut
#        self.scene.mlab.draw()

        if arrayindex == 0:
            self.title = self.scene.mlab.title(self.maketitle(-1), size=0.5, height=0.91, figure=figure)
            self.title.x_position = 0.03
            self.title.actor.width = 0.9
            self.title.text = self.maketitle(0)

#            axes = self.scene.mlab.axes(ranges=self.extent, xlabel="X", ylabel="Y", figure=figure, z_axis_visibility=False, zlabel='')#self.quantities_display_units
#            axes.label_text_property.set(italic=0, bold=0)
#            axes.axes.number_of_labels = 3
##            axes.axes.z_axis_visibility = 0
##            axes.axes.z_label = ''#self.quantities_display_units

        self.scene.scene_editor.isometric_view() #WARNING removing this line causes the surface not to display and the axes to rotate 90 degrees vertically!
        self.scene.camera.azimuth(90) #REMOVE?
        
        return surf

    @on_trait_change('scene.activated')
    def create_pipeline(self):
        for i in range(len(self.arrays)): 
            self.surfaces.append(self.surf_default(i))
#        scalarbar = self.scene.mlab.scalarbar(self.surfaces[1], str(self.quantities_display_units), "vertical", 5, None, '%.f')
#        scalarbar.title_text_property.set(font_size=4, italic=0, bold=0)
#        scalarbar.label_text_property.set(font_size=4, italic=0, bold=0)#, line_spacing=0.5)
#        scalar_bar_widget = self.surfaces[1].module_manager.scalar_lut_manager.scalar_bar_widget
#        scalar_bar_widget.representation.set(position=[0.827, 0.0524], position2=[0.1557, 0.42])
        self.scene.mlab.draw()
                        
    @on_trait_change('position')
    def update_plot(self):
        for i, surface in enumerate(self.surfaces):
            surface.mlab_source.set(scalars=self.arrays[i][:, :, self.position])
            self.title.text = self.maketitle(self.position)
        self.scene.camera.azimuth(1/(len(self.timepoints)/360)) # rotate
#        self.scene.camera.roll(1/(len(self.timepoints)/360)) # rotate
#        self.scene.render()


        
        
def test():
    
    from mcss_results_widget import McssResultsWidget
    from PyQt4.QtGui import qApp
    import sys

    argv = sys.argv
    
#    argv.insert(1, '/home/jvb/Desktop/pulseInverter.h5')
    argv.insert(1, '/home/jvb/tmp/ThreeLayers.h5')
    
    if len(argv) > 2:
        print 'usage: python mcss_results_widget.py {h5file}'#TODO mcss-results {h5file}'
        sys.exit(2)
    if len(argv) == 1:
#        shared.settings.register_infobiotics_settings()
        self = McssResultsWidget()
    elif len(argv) == 2:
        self = McssResultsWidget(filename=argv[1])
    centre_window(self)
    self.show()
    
    self.ui.select_all_runs_check_box.setChecked(True)
#    self.ui.select_all_compartments_check_box.setChecked(True)
    for item in self.ui.compartments_list_widget.findItems('*Central*', Qt.MatchWildcard):
        item.setSelected(True)

#    self.ui.from_spin_box.setValue(600);
#    self.ui.to_spin_box.setValue(800);
    
    def select_species(*names):
        for name in names:
            for item in self.ui.species_list_widget.findItems(name, Qt.MatchWildcard):
                item.setSelected(True)

#    select_species("proteinGFP")
#    select_species("proteinCI")
    select_species("FP1", "FP2")
    
#    self.ui.visualise_population_button.click()
    
    self.raise_()
    qApp.processEvents()
    
    exit(qApp.exec_())


if __name__ == "__main__":
#    execfile('mcss_results_widget.py')
    test()
    
