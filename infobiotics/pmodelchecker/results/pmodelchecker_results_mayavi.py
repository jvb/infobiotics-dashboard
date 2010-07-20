import os; os.environ['ETS_TOOLKIT'] = 'qt4'
from enthought.traits.api import HasTraits, List, Float, Str, Int, Range, Array, Instance, Unicode, Enum, Property, Button, on_trait_change, Tuple
from enthought.traits.ui.api import View, Item, VGroup, HGroup, RangeEditor, ListEditor, Label, Spring, TextEditor
import numpy as np
from bisect import bisect
from enthought.mayavi.core.ui.api import MlabSceneModel, SceneEditor#, MayaviScene 
from enthought.tvtk.pyface.api import Scene
from enthought.mayavi.core.api import PipelineBase
from infobiotics.commons.mayavi import extent

class TraitedPrismVariable(HasTraits):
    name = Str
    values = List
    resultsIndex = Int
    start = Float
    stop = Float
    value = Range('start', 'stop', 'start') 
    valueIndex = Int
    format = Unicode
    
    def findIndexInValues(self, value):
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

    def evaluateValue(self, value):
        ''' Returns the value closest '''
        self.valueIndex = self.findIndexInValues(value)
        return self.values[self.valueIndex]
        
    def _value_changed(self, value):
        ''' Sets the valueIndex to be used even when the value is set programmatically. '''
        self.value = self.evaluateValue(value)

    def traits_view(self):
        return View(
            HGroup(
                Item('name', show_label=False, style='readonly'),
                Item('value', show_label=False,
                    editor=RangeEditor(
                        evaluate=self.evaluateValue, # evaluate_name works
                        format=self.format,          # but format_name doesn't, so we need traits_view method to access self
                        mode='slider', 
                        low_name='start', 
                        high_name='stop',
                    ),                    
                    visible_when='len(object.values) > 1',
                    tooltip='Warning: the value shown in the box may not be the same as the actual value of this variable (shown to the right)',
                ),
                Item('value', show_label=False, style='readonly',
                    editor=TextEditor(),
                ),
            ),
        )


class TraitedPrismResults(HasTraits):
    property = Str
    variables = List(TraitedPrismVariable)
    results = Array
    
    scene = Instance(MlabSceneModel, ())

    axisVariables = Property(List(TraitedPrismVariable), depends_on='variables')
    def _get_axisVariables(self):
        ''' Returns the set of variables with more than 1 possible value (that can therefore be an axis). '''
        return [variable for variable in self.variables if len(variable.values) > 1]

    axisVariablesNames = Property(List(Str), depends_on='axisVariables')
    def _get_axisVariablesNames(self):
        return [variable.name for variable in self.axisVariables]
    
    xAxis = Enum(values='axisVariablesNames')
    
    notXAxisVariablesNames = Property(List(Str), depends_on='xAxis, axisVariables')
    def _get_notXAxisVariablesNames(self):
        return [variable.name for variable in self.axisVariables if variable.name != self.xAxis] 
    
    yAxis = Enum(values='notXAxisVariablesNames') 
    
    notAxes = Property(List(TraitedPrismVariable), depends_on='xAxis, yAxis')
    def _get_notAxes(self):
        return [variable for variable in self.variables if variable.name not in (self.xAxis, self.yAxis)]

    xAxisVariable = Property(Instance(TraitedPrismVariable), depends_on='xAxis')
    def _get_xAxisVariable(self):
        for variable in self.variables:
            if variable.name == self.xAxis:
                return variable
        raise ValueError("'%s' not found in variables." % self.xAxis)
    
    yAxisVariable = Property(Instance(TraitedPrismVariable), depends_on='yAxis')
    def _get_yAxisVariable(self):
        for variable in self.variables:
            if variable.name == self.yAxis:
                return variable
        return None
        raise ValueError("'%s' not found in variables." % self.yAxis)

    scalars_indicies = Property(Str)
    def _get_scalars_indicies(self):
        ''' Returns an evalable string corresponding to an extended slice of the results array. '''
        # Can't do this with a list comprehension because "else" is not allowed by the grammar/language.
        s = ''
        for i, variable in enumerate(self.variables):
            s += ':' if variable.name == self.xAxis or variable.name == self.yAxis else str(variable.valueIndex)
            if i < len(self.variables) - 1:
                s += ','
        return s

    scalars = Property(Array)
    def _get_scalars(self):
        ''' Return a 2-dimensional slice of the results array. '''
        scalars = eval('self.results[%s]' % self.scalars_indicies)
        if self.xAxisVariable.resultsIndex > self.yAxisVariable.resultsIndex:
            # transpose scalars if axes are swapped using either:
            # scalars.transpose() or scalars.T (or even results.swapaxes(x,y)) 
            scalars = scalars.T
        return scalars

    fake_scalars = Property(Array)
    def _get_fake_scalars(self):
        ''' Returns an ndarray with the same shape as scalars but the same min 
        and max as self.results. '''
        min = np.min(self.results)
        max = np.max(self.results)
#        fake_scalars = np.random.random_integers(min, high=max, size=self.scalars.shape) # not necessarily ints
        fake_scalars = np.random.random_sample(size=self.scalars.shape) * (max - min) + min # floats using element-wise multiplication and addition
        fake_scalars[0,0] = min # ensure min in array
        fake_scalars[-1,-1] = max # ensure max in array
        return fake_scalars

    @on_trait_change('variables:value') # ':' means call when 'value' attribute of items in variables change but not the object assigned to 'variables' changes 
    def update_surface(self):
        self.surface.mlab_source.scalars = self.scalars # self.surface.mlab_source.(re)set(scalars=self.scalars)

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

    ranges = Property(Tuple((Float, Float, Float, Float, Float, Float)))
    def _get_ranges(self):
        return extent(self.xAxisVariable.values, self.yAxisVariable.values, self.results)
        
    @on_trait_change('scene.activated')
    def add_actors_and_update_scalars(self):
        if self.surface is None:
            return
        
        mlab = self.scene.mlab
        mlab.figure(self.scene.mayavi_scene) # setting figure here avoids mlab.axes(figure=self.scene.mayavi_scene, ...) for each actor

        mlab.axes(ranges=self.ranges, nb_labels=5, xlabel=self.xAxis, ylabel=self.yAxis, zlabel="Result")#, color=(0,0,0))
        mlab.title("%s" % self.property, size=0.5, height=0.85)#, color=(0,0,0))
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

        self.update_surface()

        mlab.view(225, 90, 4) # rotated 45 degrees, viewed side on, from a distance of 4   
    
    reset_view = Button
    def _reset_view_fired(self):
        mlab = self.scene.mlab
        mlab.figure(self.scene.mayavi_scene)
        mlab.view(225, 90, 4) # rotated 45 degrees, viewed side on, from a distance of 4

    def traits_view(self):
        return View(
            VGroup(
                HGroup(
                    Label('Plot result for'),
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
                        editor=SceneEditor(scene_class=Scene),#MayaviScene),
                    ),
                ),
                HGroup(Spring(), Item('reset_view', show_label=False,),),
                show_border=True,
                defined_when='object.surface is not None',
            ),
            title='%s' % self.property,
        )
    

class TraitedPrismResultsPlotter(HasTraits):
    fileName = Str
    results = List(TraitedPrismResults)
    
    surfaces = Property(List(TraitedPrismResults))
    def _get_surfaces(self):
        return [result for result in self.results if len(result.variables) > 1] 
    
    def __init__(self, fileName=None, **traits):
        super(TraitedPrismResultsPlotter, self).__init__(**traits)
        if fileName is not None:
            self.load(fileName)
    
    def load(self, fileName):
        ''' Sets self.results with results from fileName. '''
        
        # read .psm file 
        file = open(fileName, "r")
        string = file.read()
        file.close()
        
        # split and strip lines
        lines = [line.strip() for line in string.split("\n")]
        
        # handle multiple sets of results in same file
        results = []
        started = ended = -1
        for i, line in enumerate(lines):
            if str(line).endswith(":"):
                started = i
            elif len(line) == 0:
                ended = i
            if started != -1 and ended != -1:
                results.append(lines[started:ended])
#                results.append([line.strip() for line in lines[started:ended]])
                started = ended = -1
            if started == -1 and ended != -1:
                ended = -1
        if started != -1 and ended == -1:
            results.append(lines[started:len(lines)])            
#        
        # remove headers without 2 lines of results
        for lines in reversed(results):
            if not (len(lines) >= 4 and lines[0].endswith(':') and lines[1].endswith('Result')):
                results.pop()
        
        # create TraitedPrismVariables and return list of TraitedPrismResults
        listOfTraitedPrismResultsInstances = []
        for lines in results:
            # extract property
            property = lines[0].split(':')[0]

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
            variableValuesStrs = [line.split(' ')[:-1] for line in lines[2:]]
#            print variableValuesStrs #TODO find decimal places code
            
            listOfTraitedPrismVariableInstances = []
            for i in range(len(variableNames)):
                # extract this variables column, remove duplicates and sort
#                print variableValues[:,i]
                sortedSet = sorted(set(variableValues[:,i]))
#                print sortedSet

                # change format to integer if only trailing zeros after decimal point
                onlyTrailingZero = True
                for value in sortedSet:
                    if str(value).split('.')[1] != '0':
                        onlyTrailingZero = False
                if onlyTrailingZero:
                    format = '%d'
                else:
                    format = '%02.2f'

                # create TraitedPrismVariable instance and append it
                instance = TraitedPrismVariable(
                    name=variableNames[i],
                    values=sortedSet,
                    resultsIndex=i,
                    start=float(sortedSet[0]), # this is problematic
#                    startLabel=str(sortedSet[0]),
                    stop=float(sortedSet[-1]),
#                    stopLabel=str(sortedSet[-1])
                    format=format
                )
#                print instance.values
#                print instance.start, instance.stop
                listOfTraitedPrismVariableInstances.append(instance)
            
            # get dimensions tuple from length of each variables values
            shape = tuple([len(instance.values) for instance in listOfTraitedPrismVariableInstances])
        
            # extract results column from lines excluding variables columns
            resultValues = np.array([line.split(' ')[-1] for line in lines[2:]], np.float32)
#            print resultValues
            
            # reshape into dimensions of variables
            resultValues = resultValues.reshape(shape)
            
            # create TraitedPrismResults instance and append it
            '''
            class TraitedPrismResults(HasTraits):                
                property = Str
                variables = List(TraitedPrismVariable)
                results = Array
            '''
            instance = TraitedPrismResults(
                property=property, 
                variables=listOfTraitedPrismVariableInstances, 
                results=resultValues,
            )
            listOfTraitedPrismResultsInstances.append(instance)
            
        self.results = listOfTraitedPrismResultsInstances
        self.fileName = fileName

    def traits_view(self):
        return View(
            HGroup(
#                Item('results', show_label=False, style='custom',  #TODO use for matplotlib figures
#                    editor=ListEditor(
#                        use_notebook=True, 
#                        page_name='.property',
#                    ),
#                ),
                Item('surfaces', show_label=False, style='custom', 
                    editor=ListEditor(
                        use_notebook=True, 
                        page_name='.property',
                    ),
                    defined_when='len(object.surfaces) > 1'
                ),
                show_border=True,
                defined_when='len(object.results) > 0',
            ),
            Label("No results found in '%s'" % self.fileName, defined_when='len(object.results) == 0'),
            title='%s' % self.fileName,
            resizable=True,
            id='view_%s' % self.fileName,
        )


if __name__ == '__main__':
    main = TraitedPrismResultsPlotter()
    main.load('1-4_variables.psm')
    main.configure_traits()
        
