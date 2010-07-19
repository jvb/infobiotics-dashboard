import os; os.environ['ETS_TOOLKIT'] = 'qt4'
from enthought.traits.api import HasTraits, List, Float, Str, Int, Range, Array, Instance, Unicode, Enum, Property, Bool, on_trait_change
from enthought.traits.ui.api import View, Item, VGroup, HGroup, RangeEditor, ListEditor, Heading, Label, Spring, TextEditor, InstanceEditor
from numpy import array, arange, zeros, float32
import numpy as np
from bisect import bisect
from enthought.tvtk.pyface.scene_editor import SceneEditor
from enthought.mayavi.tools.mlab_scene_model import MlabSceneModel
from enthought.mayavi.core.ui.mayavi_scene import MayaviScene
from infobiotics.commons.mayavi import extent, normalized_extent, normalized_extent_z_by_other_array

def normalize_array_by_other_array(a, other):
    min = np.min(other)
    return (a - min) * 1 / (np.max(other) - min)
    # brackets are vital here because only '(a - min)' returns an array

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
        previous = next - 1
        if next == len(self.values):
            # value is greater than last item in values
            return previous
        b = self.values[next]
        a = self.values[previous]
        if abs(value - a) < abs(value - b):
            # value is closer to previous
            return previous
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
                        format=self.format,          # but format_name doesn't
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

# test evaluate function
#TraitedPrismVariable(values=[0,4,8], start=0, stop=8, format='%d').configure_traits()
#v = TraitedPrismVariable(values=[0,4,8], start=0, stop=8, format='%d')
#print v.value, v.valueIndex
#v.value = 5
#print v.value, v.valueIndex
#exit()

class TraitedPrismResults(HasTraits):
    property = Str
    variables = List(TraitedPrismVariable)
    results = Array
    
    scene = Instance(MlabSceneModel, ())

#    can_be_3d = Bool(False)
#    def _can_be_3d_default(self):
#        return len(self.variables) > 1

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

    def getScalarsIndicies(self):
        ''' Returns an evalable string corresponding to an extended slice of the results array. '''
        # Can't do this with a list comprehension because "else" is not allowed by the grammar/language.
        s = ''
        for i, variable in enumerate(self.variables):
            s += ':' if variable.name == self.xAxis or variable.name == self.yAxis else str(variable.valueIndex)
            if i < len(self.variables) - 1:
                s += ','
        return s

    def get_scalars(self):
        ''' Return a 2-dimensional slice of the results array. '''
        scalars = eval('self.results[%s]' % self.getScalarsIndicies())
        if self.xAxisVariable.resultsIndex > self.yAxisVariable.resultsIndex:
            # transpose scalars if axes are swapped using either:
            # scalars.transpose() or scalars.T (or results.swapaxes(x,y) initially) 
            scalars = scalars.T
        return scalars
#        normalized = normalize_array_by_other_array(scalars, self.results) 
#        print normalized
#        return normalized
#        # this doesn't work because then the scalarbar is set to 0 or 1
    
    @on_trait_change('variables:value') # ':' means call when 'value' attribute of items in variables change but not the object assigned to 'variables' changes 
    def updateSurface(self):
        self.plot.mlab_source.scalars = self.get_scalars()

    @on_trait_change('xAxis, yAxis')
    def change_data(self): #self.axes.axes.ranges = ...
        mlab = self.scene.mlab
        mlab.clf()
        self.create_plot()
        #TODO recalculate extent
        self.axes = mlab.axes(ranges=self.ranges, nb_labels=5, xlabel=self.xAxis, ylabel=self.yAxis, zlabel="Result")#, color=(0,0,0))
        self.title = mlab.title("%s" % self.property, size=0.5, height=0.85)#, color=(0,0,0))
        self.scalarbar = mlab.scalarbar(title ='Result', orientation='vertical', label_fmt='%.f', nb_labels=5)

    def create_plot(self):
        scalars = self.get_scalars() #FIXME scalars aren't changing, maybe dataset looks same from all directions?
        x = self.xAxisVariable.values
        y = self.yAxisVariable.values
        self.ranges = extent(x, y, scalars) # used in add_actors
#        self.ranges = extent(x, y, self.results)#,scalars) # used in add_actors
        self.plot = self.scene.mlab.surf(x, y, scalars, colormap='jet', extent=[0,1,0,1,0,1])

    @on_trait_change('scene.activated')
    def add_actors(self):
        if not hasattr(self, 'ranges'): return #TODO remove
        mlab = self.scene.mlab
        self.axes = mlab.axes(ranges=self.ranges, nb_labels=5, xlabel=self.xAxis, ylabel=self.yAxis, zlabel="Result")#, color=(0,0,0))
        self.title = mlab.title("%s" % self.property, size=0.5, height=0.85)#, color=(0,0,0))
        self.scalarbar = mlab.scalarbar(title ='Result', orientation='vertical', label_fmt='%.f', nb_labels=5)
        
#        self.scene.scene_editor.isometric_view() # finally works! but below is better
        mlab.view(225, 90, 4) # rotated 45 degrees, viewed side on, from a distance of 4  

#        # setting scalarbar title and label fonts
#        scalarbar.title_text_property.set(font_size=4)
#        scalarbar.label_text_property.set(font_size=4, italic=0, bold=0)#, line_spacing=0.5)
#        
#        # set position and size of scalarbar
#        scalar_bar_widget = self.plot.module_manager.scalar_lut_manager.scalar_bar_widget
#        # since VTK-5.2 the actual widget is accessed through its representation property (see https://mail.enthought.com/pipermail/enthought-dev/2009-May/021342.html) - we using at least VTK-5.4
#        scalar_bar_widget.representation.set(position=[0.9,0.08], position2=[0.09,0.42])
#
#        # set scene's foreground and background colours
#        self.scene.scene_editor.background = (1,1,1) # white background
#        self.scene.scene_editor.foreground = (0,0,0) # black text

    def traits_view(self):
        return View(
            VGroup(
                HGroup(
                    Label('Variables to plot: '),
                    Item('xAxis', label='X'),
                    Item('yAxis', label='Y'),
                ),
                Item(
                    'scene', 
                    show_label=False,
                    editor=SceneEditor(scene_class=MayaviScene),
                    height=250,
                    width=300, 
                    resizable=True
                ),
                Item('notAxes', 
                    visible_when='len(notAxes) > 0', 
                    show_label=False, 
                    editor=ListEditor(style='custom'), 
                    resizable=False, 
                    style='readonly',
                ),
                show_border=True,
            ),
            resizable=True,
            title='%s' % self.property,
        )
    


class TraitedPrismResultsPlotter(HasTraits):
    fileName = Str
    results = List(TraitedPrismResults)
    
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
            variableValues = array([line.split(' ')[:-1] for line in lines[2:]], float32)
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
            resultValues = array([line.split(' ')[-1] for line in lines[2:]], float32)
#            print resultValues
            
            # reshape into dimensions of variables
#            print resultValues, shape #TODO remove
            resultValues = resultValues.reshape(shape)
#            print resultValues[1,1,1,1] #TODO remove
            
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
            VGroup(
                Item('results', show_label=False, style='custom', 
                     editor=ListEditor(use_notebook=True, page_name='.property'),
                ),
                show_border=True,
            ),
            title='%s' % self.fileName,
        )


if __name__ == '__main__':
    main = TraitedPrismResultsPlotter()
    main.load('1-4_variables.psm')
    main.results[2].create_plot()
    main.configure_traits()
        
