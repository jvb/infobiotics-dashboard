import os; os.environ['ETS_TOOLKIT'] = 'qt4'
from enthought.traits.api import (
    HasTraits, List, Float, Str, Int, Range, Array, Instance, Unicode, Enum, 
    Property, Button, on_trait_change, Tuple, cached_property, Bool, 
    DelegatesTo,
)
from enthought.traits.ui.api import (
    View, Item, VGroup, HGroup, RangeEditor, ListEditor, Label, Spring, 
    TextEditor, InstanceEditor, CodeEditor, 
#    CheckListEditor,
)

import os.path

from infobiotics.commons.traits.relative_file import RelativeFile 

import hashlib

import numpy as np

from bisect import bisect

# check if mayavi2 version < 3.3.0        
import enthought.mayavi.__version__
version = enthought.mayavi.__version__.__version__
version_info = version.split('.') 
major = int(version_info[0])
minor = int(version_info[1])
if major < 3 or (major == 3 and minor < 3):
    outdated_mayavi = True
else:
    outdated_mayavi = False

if outdated_mayavi:
    # Mayavi < 3.3
    from enthought.tvtk.pyface.api import Scene
    from enthought.mayavi.tools.mlab_scene_model import MlabSceneModel
    from enthought.tvtk.pyface.scene_editor import SceneEditor
    from enthought.mayavi.core.ui.mayavi_scene import MayaviScene
    from enthought.mayavi.core.pipeline_base import PipelineBase
else:
    # Mayavi >= 3.3
    from enthought.mayavi.core.ui.api import MlabSceneModel, SceneEditor, MayaviScene 
    from enthought.mayavi.core.api import Scene, PipelineBase

from infobiotics.commons.mayavi import extent

from matplotlib.figure import Figure

from infobiotics.commons.traits.ui.qt4.matplotlib_figure_editor import MPLFigureEditor 


class PModelCheckerResultsPropertyVariable(HasTraits):
    name = Str
    values = List
    result_array_index = Int
    start = Float
    stop = Float
    value = Range('start', 'stop', 'start') 
    value_index = Int
    format = Unicode
    
    def find_index_in_values(self, value):
        ''' Returns the index of the item closest to value in self.values. '''
        next = bisect(self.values, value)
        prev = next - 1
        if next == len(self.values):
            # value is greater than last item in values
            return prev
        b = self.values[next]
        a = self.values[prev]
        if abs(value - a) < abs(value - b):
            # value is closer to prev
            return prev
        else:
            # value is closer to next
            return next

    def evaluate_value(self, value):
        ''' Returns the value closest '''
        self.value_index = self.find_index_in_values(value)
        return self.values[self.value_index]
        
    def _value_changed(self, value):
        ''' Sets the value_index to be used even when the value is set programmatically. '''
        self.value = self.evaluate_value(value)

    def traits_view(self):
        return View(
            HGroup(
                Item('name', show_label=False, style='readonly'),
                Item('value', show_label=False,
                    editor=RangeEditor(
                        evaluate=self.evaluate_value, # evaluate_name works
                        format=self.format,          # but format_name doesn't, so we need a traits_view method (as opposed to view = View...) to be able to access self
                        mode='slider', 
                        low_name='start', 
                        high_name='stop',
                    ),                    
                    visible_when='len(object.values) > 1',
                    tooltip='Warning: the value shown in the box may not be the same as the actual value of this variable (shown to the right)',
                ),
                Item('value', show_label=False, style='readonly',
                    editor=TextEditor(format_str=self.format),
                ),
            ),
        )


class PModelCheckerResultsPropertyVisualisation(HasTraits):
    property = Instance('PModelCheckerResultsProperty')
    property_string = DelegatesTo('property')
    variables = DelegatesTo('property')
    result_array = DelegatesTo('property')
    axisVariables = DelegatesTo('property')    

    type = Str
    def _type_default(self):
        raise NotImplementedError('Subclasses of PModelCheckerResultsPropertyVisualisation should specify a type.')

    def __init__(self, property, **traits):
        self.property = property # must come before __init__ because that tries to use it as a delegates
        super(PModelCheckerResultsPropertyVisualisation, self).__init__(**traits)
        self.init()

    def init(self):
        ''' Can be overridden by subclasses to initialise their visualisation apparatus. '''
        pass
    
    axisVariablesNames = Property(List(Str), depends_on='axisVariables')
    def _get_axisVariablesNames(self):
        return [variable.name for variable in self.axisVariables]
    
    xAxis = Enum(values='axisVariablesNames')
    
    notXAxisVariablesNames = Property(List(Str), depends_on='xAxis, axisVariables')
    def _get_notXAxisVariablesNames(self):
        return [variable.name for variable in self.axisVariables if variable.name != self.xAxis] 
    
    yAxis = Enum(values='notXAxisVariablesNames')
    
    notAxes = Property(List(PModelCheckerResultsPropertyVariable), depends_on='xAxis, yAxis')
    def _get_notAxes(self):
        return [variable for variable in self.variables if variable.name not in (self.xAxis, self.yAxis)]

    xAxisVariable = Property(Instance(PModelCheckerResultsPropertyVariable), depends_on='xAxis')
    def _get_xAxisVariable(self):
        for variable in self.variables:
            if variable.name == self.xAxis:
                return variable
        raise ValueError("'%s' not found in variables." % self.xAxis)
    
    yAxisVariable = Property(Instance(PModelCheckerResultsPropertyVariable), depends_on='yAxis')
    def _get_yAxisVariable(self):
        for variable in self.variables:
            if variable.name == self.yAxis:
                return variable
        return None
        raise ValueError("'%s' not found in variables." % self.yAxis)

    dependent_axis_label = Str
    def _dependent_axis_label_default(self):
        return 'Result'#self.property_string.split('=')[0].strip() #FIXME
        
        
class PModelCheckerResultsPropertyFigure(PModelCheckerResultsPropertyVisualisation):
    ''' Interactive Matplotlib figure showing the results for a PModelCheckerResultsProperty. '''
    type = 'Figure'
    figure = Instance(Figure)
    legend = Bool(True)

    scalars_indicies = Property(Str, depends_on='xAxis, variables:value_index')
    @cached_property #TODO uncache?
    def _get_scalars_indicies(self):
        ''' Returns an evalable string corresponding to an extended slice of result_array. '''
        # Can't do this with a list comprehension because "else" is not allowed by the grammar/language.
        s = ''
        for i, variable in enumerate(self.variables):
#            s += ':' if variable.name == self.xAxis or variable.name == self.yAxis else str(variable.value_index)
            s += ':' if variable.name == self.xAxis else str(variable.value_index)
            if i < len(self.variables) - 1:
                s += ','
        return s

    scalars = Property(Array, depends_on='scalars_indicies')
    @cached_property
    def _get_scalars(self):
        ''' Return a 1-dimensional slice of result_array. '''
        scalars = eval('self.result_array[%s]' % self.scalars_indicies)
        return scalars

   
    min_result = Property(Float, depends_on='result_array')
    @cached_property
    def _get_min_result(self):
        return np.min(self.result_array)
    
    max_result = Property(Float, depends_on='result_array')
    @cached_property
    def _get_max_result(self):
        return np.max(self.result_array)
    
    @on_trait_change('xAxis, yAxis')#, variables:value')
    def update(self):
        axes = self.axes
        axes.clear()
        axes.set_title(self.property_string)
        axes.set_xlabel(self.xAxis)
        axes.set_ylabel('Result')
        axes.grid(True)

        x = self.xAxisVariable.values

        if len(self.notXAxisVariablesNames) < 1:
            axes.plot(x, self.scalars)
        else:
            # slice result_array without changing self.yAxisVariable.value_index
            for j, v in enumerate(self.yAxisVariable.values):
                s = ''
                for i, variable in enumerate(self.variables):
                    if variable.name == self.xAxis:
                        s += ':' 
                    elif variable.name == self.yAxis:
                        s += str(j)
                    else:
                        s += str(variable.value_index)
                    if i < len(self.variables) - 1:
                        s += ','
                scalars = eval('self.result_array[%s]' % s)
                label='%s=%s' % (self.yAxis, v)
                for variable in self.variables:
                    if variable not in (self.xAxisVariable, self.yAxisVariable):
                        label += ', %s=%s' % (variable.name, variable.value)
                axes.plot(x, scalars, label=label)
            if self.legend:
                self.axes.legend(loc='best')

        # can only set axes limits after plotting
        self.axes.set_xlim(np.min(x), np.max(x))
        self.axes.set_ylim(self.min_result, self.max_result)
        
        if self.figure.canvas is not None:
            self.figure.canvas.draw()
    
    def init(self):
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.update()
    
    def traits_view(self):
        return View(
            VGroup(
                HGroup(
                    Item('dependent_axis_label', show_label=False, style='readonly'),
                    Label('for each'),
#                    Item('yAxis', show_label=False, defined_when='len(object.notXAxisVariablesNames) > 1'), # choice case
#                    Item('yAxis', show_label=False, style='readonly', defined_when='len(object.notXAxisVariablesNames) == 1'), # no choice case #FIXME text doesn't change when value of yAxis changes 
                    Item('yAxis', show_label=False),
#                    Item('notXAxisVariablesNames', style='custom', 
#                        editor=CheckListEditor(
#                            name='object.notXAxisVariablesNames', # can't use this until EPD > 6.2: http://markmail.org/message/lf6qfg47xhl5j6u2
#                        )
#                    ),
                    Label('at all'),
                    Item('xAxis', show_label=False),
                    Label('when', defined_when='len(object.notAxes) > 0'),
                    defined_when='len(object.notXAxisVariablesNames) > 0', 
                ),
                Item('notAxes', 
                    show_label=False, 
                    editor=ListEditor(style='custom'), 
                    resizable=False, 
                    style='readonly',
                    defined_when='len(object.notAxes) > 0', 
                ),
                Item(
                    'figure', 
                    show_label=False,
                    editor=MPLFigureEditor(toolbar=True), #TODO save with Figure.set_figsize_inches( (w,h) ) # http://www.scipy.org/Cookbook/Matplotlib/AdjustingImageSize
                    resizable=True
                ),
                HGroup(
                    Spring(), 
                    Item('detach', show_label=False),
                ),
                show_border=True,
            ),
            title=self.property_string,
            resizable=True,
        )

    detach = Button
    def _detach_fired(self):
        self.edit_traits()


class PModelCheckerResultsPropertySurface(PModelCheckerResultsPropertyVisualisation):
    type = 'Surface'
    scene = Instance(MlabSceneModel, ())

    scalars_indicies = Property(Str)
    def _get_scalars_indicies(self):
        ''' Returns an evalable string corresponding to an extended slice of result_array. '''
        # Can't do this with a list comprehension because "else" is not allowed by the grammar/language.
        s = ''
        for i, variable in enumerate(self.variables):
            s += ':' if variable.name == self.xAxis or variable.name == self.yAxis else str(variable.value_index)
            if i < len(self.variables) - 1:
                s += ','
        return s

    scalars = Property(Array)
    def _get_scalars(self):
        ''' Return a 2-dimensional slice of result_array. '''
        scalars = eval('self.result_array[%s]' % self.scalars_indicies)
        if self.xAxisVariable.result_array_index > self.yAxisVariable.result_array_index:
            # transpose scalars if axes are swapped using either:
            # scalars.transpose() or scalars.T (or even result_array.swapaxes(x,y)) 
            scalars = scalars.T
        return scalars

    fake_scalars = Property(Array)
    def _get_fake_scalars(self):
        ''' Returns an ndarray with the same shape as scalars but the same min 
        and max as self.result_array. '''
        min = np.min(self.result_array)
        max = np.max(self.result_array)
#        fake_scalars = np.random.random_integers(min, high=max, size=self.scalars.shape) # not necessarily ints
        fake_scalars = np.random.random_sample(size=self.scalars.shape) * (max - min) + min # floats using element-wise multiplication and addition
        fake_scalars[0,0] = min # ensure min in array
        fake_scalars[-1,-1] = max # ensure max in array
        return fake_scalars

#    @on_trait_change('variables:value') # ':' means call when 'value' attribute of items in variables change but not the object assigned to 'variables' changes 
    # done in PModelCheckerResultsProperty.update_visualisations
    def update(self):
        self.surface.mlab_source.scalars = self.scalars # self.surface.mlab_source.(re)set(scalars=self.scalars)
        self.title.text = self.title_text 

    title_text = Property(Str)
    def _get_title_text(self):
        s = "%s" % self.property_string
        if len(self.variables) > 2:
            s += ' '
            s += '(%s)' % ','.join(['%s=%s' % (variable.name, variable.value) for variable in self.variables if variable not in (self.xAxisVariable, self.yAxisVariable)])
        return s
    
    @on_trait_change('xAxis, yAxis')
    def change_data(self):
        self.scene.mlab.clf(figure=self.scene.mayavi_scene)
        self.surface = self.create_surface()
        self.add_actors_and_update_scalars()

    def create_surface(self):
        return self.scene.mlab.surf(self.fake_scalars, colormap='jet', extent=[0,1,0,1,0,1], figure=self.scene.mayavi_scene)

    surface = Instance(PipelineBase)
    def _surface_default(self):
        if len(self.axisVariables) > 1:
            return self.create_surface()
        return None

    ranges = Property(Tuple((Float, Float, Float, Float, Float, Float)))
    def _get_ranges(self):
        return extent(self.xAxisVariable.values, self.yAxisVariable.values, self.result_array)
        
    @on_trait_change('scene.activated')
    def add_actors_and_update_scalars(self):
        if self.surface is None:
            return
        mlab = self.scene.mlab
        mlab.figure(self.scene.mayavi_scene) # setting figure here avoids mlab.axes(figure=self.scene.mayavi_scene, ...) for each actor

        mlab.axes(ranges=self.ranges, nb_labels=5, xlabel=self.xAxis, ylabel=self.yAxis, zlabel="Result")#, color=(0,0,0))
        
        self.title = mlab.title(self.title_text, size=0.4, height=0.88)
        
        mlab.outline(extent=[0,1,0,1,0,1])
        
        scalarbar = mlab.scalarbar(title ='Result', orientation='vertical', label_fmt='%.f', nb_labels=5)
        scalarbar.title_text_property.set(font_size=4)
        scalarbar.label_text_property.set(font_size=4)#, italic=0, bold=0)#, line_spacing=0.5)
        # since VTK-5.2 the actual widget is accessed through its representation property (see https://mail.enthought.com/pipermail/enthought-dev/2009-May/021342.html) - we using at least VTK-5.4
        scalar_bar_widget = self.surface.module_manager.scalar_lut_manager.scalar_bar_widget
        scalar_bar_widget.representation.set(position=[0.9,0.08], position2=[0.09,0.42])

#        # set scene's foreground and background colours
#        self.scene.scene_editor.background = (0,0,0) # black background
#        self.scene.scene_editor.foreground = (1,1,1) # white text

        self.update()

    reset_view = Button
    @on_trait_change('scene.activated, reset_view')
    def reorient_view(self):
        mlab = self.scene.mlab
        mlab.figure(self.scene.mayavi_scene)
        mlab.view(225, 90, 4) # rotated 45 degrees, viewed side on, from a distance of 4

    def traits_view(self):
        return View(
            VGroup(
                HGroup(
                    Item('dependent_axis_label', show_label=False, style='readonly'),
                    Label('for'),
                    Item('yAxis', show_label=False),
                    Label('against'),
                    Item('xAxis', show_label=False),
                    Label('when', resizable=False, defined_when='len(object.notAxes) > 0',),
                    defined_when='object.surface is not None',
                ),
                VGroup(
                    Item('notAxes', 
                        show_label=False, 
                        editor=ListEditor(style='custom'), 
                        style='readonly',
                        visible_when='len(object.notAxes) > 0',
                        resizable=False, springy=False, height=20, # must set these enable scene to fill all available space
                    ),
                    Item(
                        'scene', 
                        show_label=False,
                        editor=SceneEditor(scene_class=MayaviScene),#Scene),
                    ),
                ),
                HGroup(
                    Spring(), 
                    Item('reset_view', show_label=False),
                ),
                show_border=True,
                defined_when='object.surface is not None',
            ),
        )


class PModelCheckerResultsPropertyRawData(PModelCheckerResultsPropertyVisualisation):
    type = 'Data'
    raw_data = DelegatesTo('property')
    md5sum = DelegatesTo('property')
    full_file_name = Property(Str)
    def _get_full_file_name(self):
        return os.path.normpath(self.property.file_name_)
    
    def update(self):
        # gets called by PModelCheckerResultsProperty.update_visualisations()
        pass
    
    view = View(
        VGroup(
            Item('raw_data',
                show_label=False,
                editor=CodeEditor(lexer='null'),
                style='readonly',
            ),
            VGroup(
                Item('full_file_name', label='in'),
                Item('md5sum', label='with md5sum'),
            ),
            show_border=True,
        ),
    )


# a list of tuples of (callable, the minimum number of axes required for the visualisation)  
visualisation_classes = [(PModelCheckerResultsPropertyFigure, 1)]
if not outdated_mayavi:
    visualisation_classes += [(PModelCheckerResultsPropertySurface, 2)]
visualisation_classes += [(PModelCheckerResultsPropertyRawData, 0)]


class PModelCheckerResultsProperty(HasTraits):
    property_string = Str
    variables = List(Instance('PModelCheckerResultsPropertyVariable'))
    result_array = Array
    raw_data = Str
    file_name = RelativeFile
    md5sum = Str

    visualisations = List(Instance('PModelCheckerResultsPropertyVisualisation'))
    def _visualisations_default(self):
        return [klass(property=self) for klass, min_axes in visualisation_classes if len(self.axisVariables) >= min_axes]

    @on_trait_change('variables:value')
    def update_visualisations(self):
        ''' Unfortunately this is necessary because change to value of items in 
        variables are not propagating to the visualisations, and not necessarily
        due to delegation! '''
        for visualisation in self.visualisations:
            visualisation.update()

    axisVariables = Property(List(PModelCheckerResultsPropertyVariable), depends_on='variables')
    @cached_property
    def _get_axisVariables(self):
        ''' Returns the set of variables with more than 1 possible value (that can therefore be an axis). '''
        return [variable for variable in self.variables if len(variable.values) > 1]

    traits_view = View(
        VGroup(
            Item('visualisations',
                show_label=False, 
                style='custom', 
                editor=ListEditor(
                    use_notebook=True, 
                    page_name='.type',
                ),
#                defined_when='not object.outdated_mayavi and len(object.surfaces) > 0', # not object.outdated_mayavi must come first! #TODO remove
            ),
            show_border=True,
#            defined_when='len(object.properties) > 0', #TODO remove
        ),
    )

    name = Str # used by PModelCheckerResults.selected InstanceEditor for long property names combobox
    def _name_default(self):
        return self.property_string

        
class PModelCheckerResults(HasTraits):

    file_name = RelativeFile(
        absolute=True,
        exists=True,
        filter=[
            'PModelChecker results files (*.psm)',
        ],
    )

    properties = List(PModelCheckerResultsProperty)

    selected = Instance(PModelCheckerResultsProperty)
    def _properties_changed(self):
        self.selected = self.properties[0]

    def __init__(self, file_name=None, **traits):
        super(PModelCheckerResults, self).__init__(**traits)
        if file_name is not None:
            self.file_name = file_name
            
    def _file_name_changed(self):
        self.load(self.file_name)
    
    def load(self, file_name):
        ''' Sets self.properties with properties from file_name. '''
        
        # read .psm file 
        file = open(file_name, "r")
        string = file.read()
        md5sum = hashlib.md5(string).hexdigest()
        lines = [line.strip() for line in string.split("\n")]
        file.close()
        
        # split and strip lines
        
        # handle multiple sets of properties in same file
        properties = []
        started = ended = -1
        for i, line in enumerate(lines):
            if str(line).endswith(":"):
                started = i
            elif len(line) == 0:
                ended = i
            if started != -1 and ended != -1:
                properties.append(lines[started:ended])
#                properties.append([line.strip() for line in lines[started:ended]])
                started = ended = -1
            if started == -1 and ended != -1:
                ended = -1
        if started != -1 and ended == -1:
            properties.append(lines[started:len(lines)])            
#        
        # remove properties without 2 lines of values (i.e. a property with just a header or a single result that isn't amenable to visualisation)
        for lines in reversed(properties):
            if not (len(lines) >= 4 and lines[0].endswith(':') and lines[1].endswith('Result')):
                properties.pop()
        
        # create PModelCheckerResultsPropertyVariables and return list of PModelCheckerResultsProperty
        listOfPModelCheckerResultsPropertyInstances = []
        for lines in properties:
            # extract property string
            property_string = lines[0].split(':')[0]

            # extract variables names ignoring 'Result'
            variableNames = lines[1].split(' ')[:-1]

            # extract variable values into array from lines excluding Results column
            ''' e.g.
          [[0 0 0 0 0]
           [0 0 0 1 1]
           [0 0 1 0 2]
           [0 0 1 1 3]
           [0 1 0 0 4]]
            '''            
            variableValues = np.array([line.split(' ')[:-1] for line in lines[2:]], np.float32)
#            variableValuesStrs = [line.split(' ')[:-1] for line in lines[2:]]; print variableValuesStrs #TODO find decimal places code
            
            listOfPModelCheckerResultsPropertyVariableInstances = []
            for i in range(len(variableNames)):
                # extract this variables column, remove duplicates and sort
                sortedSet = sorted(set(variableValues[:,i]))

                # change format to integer if only trailing zeros after decimal point
                onlyTrailingZero = True
                for value in sortedSet:
                    if str(value).split('.')[1] != '0':
                        onlyTrailingZero = False
                if onlyTrailingZero:
                    format = '%d'
                else:
                    format = '%02.2f'

                # create PModelCheckerResultsPropertyVariable instance and append it
                instance = PModelCheckerResultsPropertyVariable(
                    name=variableNames[i],
                    values=sortedSet,
                    result_array_index=i,
                    start=float(sortedSet[0]), #FIXME this is problematic
#                    startLabel=str(sortedSet[0]),
                    stop=float(sortedSet[-1]),
#                    stopLabel=str(sortedSet[-1])
                    format=format
                )
                listOfPModelCheckerResultsPropertyVariableInstances.append(instance)
            
            # get dimensions tuple from length of each variables values
            shape = tuple([len(instance.values) for instance in listOfPModelCheckerResultsPropertyVariableInstances])
        
            # extract result column from lines excluding variables columns
            result_array = np.array([line.split(' ')[-1] for line in lines[2:]], np.float32)
            
            # reshape into dimensions of variables
            result_array = result_array.reshape(shape)
            
            # create PModelCheckerResultsProperty instance and append it
            instance = PModelCheckerResultsProperty(
                property_string=property_string, 
                variables=listOfPModelCheckerResultsPropertyVariableInstances, 
                result_array=result_array,
                raw_data = '\n'.join(lines),
                file_name=file_name,
                md5sum=md5sum,
            )
            listOfPModelCheckerResultsPropertyInstances.append(instance)
            
        self.properties = listOfPModelCheckerResultsPropertyInstances # setting this triggers the creation of the plots
#        self.file_name = file_name

    values = Property(List(Tuple(PModelCheckerResultsProperty, Str)), depends_on='properties')
    @cached_property
    def _get_values(self):
        return [(property, property.property_string) for property in self.properties]

    def traits_view(self):
        return View(
            VGroup(
                Item('file_name', label='Results file'),
#                Label("No properties found in '%s'" % self.file_name, defined_when='len(object.properties) == 0'), #TODO replace with message in text box
#                Label('This functionality is disabled because the current version of Mayavi2 is out of date.\nPlease ensure Mayavi2>=3.3.2 is installed to use this feature.\nIf you are using Ubuntu this dependency is due to be fulfilled in Ubuntu 10.10 Maverick Meerkat.', defined_when='object.outdated_mayavi'), #TODO
                Item('selected',
                    label='Property',
                    editor=InstanceEditor(
                        name='object.properties', #FIXME doesn't update with properties
                        editable=False,
                    ),
                    visible_when='len(object.properties) > 1',
                ),
#                Item('selected',
#                    label='Property',
#                    editor=CheckListEditor( # bug in CheckListEditor or rather Editor than prevents this for working
#                        name='values',
#                    ),
#                    visible_when='len(object.properties) > 1',
#                ),
                VGroup(
                    Item('properties', 
                        show_label=False, 
                        style='custom', 
                        editor=ListEditor(
                            use_notebook=True, 
                            page_name='.property_string',
                            selected='object.selected',
                        ),
#                        defined_when='not object.outdated_mayavi and len(object.surfaces) > 0', # not object.outdated_mayavi must come first! #TODO remove
                    ),
                    visible_when='len(object.properties) > 0',
                ),
                show_border=True,
            ),
            title='%s' % self.file_name,
            resizable=True,
            id='view_%s' % self.file_name,
        )    


if __name__ == '__main__':
    main = PModelCheckerResults('results/1-4_variables.psm')
#    main = PModelCheckerResults(file_name='results/1-4_variables.psm')
#    main.load('2d_function.psm')

#    main.selected = main.properties[1] # doesn't work until PModelCheckerResults.configure_traits()

    main.configure_traits()
            