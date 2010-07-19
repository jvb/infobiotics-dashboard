import os; os.environ['ETS_TOOLKIT'] = 'qt4'
from enthought.traits.api import HasTraits, List, Float, Str, Int, Range, Array, Instance, Unicode, Enum, Property, Bool, on_trait_change
from enthought.traits.ui.api import View, Item, VGroup, HGroup, RangeEditor, ListEditor, Heading, Label, Spring, TextEditor, InstanceEditor
from numpy import array, arange, zeros, float32
from bisect import bisect
from enthought.tvtk.pyface.scene_editor import SceneEditor
from enthought.mayavi.tools.mlab_scene_model import MlabSceneModel
from enthought.mayavi.core.ui.mayavi_scene import MayaviScene
from infobiotics.commons.mayavi import extent, normalized_extent

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
        # find the index of the item closest to value in self.values
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

    def evaluateValue(self, new):
        return self.values[self.findIndexInValues(new)]
        
    def _value_changed(self, value):
        self.valueIndex = self.findIndexInValues(value)
        print value #TODO remove

    def traits_view(self):
        return View(
            HGroup(
                Item('name', show_label=False, style='readonly'),
                Item('value', 
                    show_label=False,
                    tooltip='Warning: the value shown in the box may not be the same as the actual value of this variable (shown to the right)',
                    editor=RangeEditor(
                        format=self.format,
                        evaluate=self.evaluateValue,
                        mode='slider', 
                        low_name='start', 
                        high_name='stop',
                    ),                    
                    visible_when='len(object.values) > 1',
                ),
                Item('value', 
                    show_label=False, 
                    editor=TextEditor(),
                    style='readonly',
                ),
            ),
        )

## test evaluate function
#TraitedPrismVariable(values=[0,4,8], start=0, stop=8, format='%d').configure_traits()
#exit()


class TraitedPrismResults(HasTraits):
    property = Str
    variables = List(TraitedPrismVariable)
    results = Array
    scene = Instance(MlabSceneModel, ())

#    can_be_3d = Bool(False)
#    def _can_be_3d_default(self):
#        return len(self.variables) > 1

    variablesNames = Property(List(Str), depends_on='variables')
    def _get_variablesNames(self):
        return [variable.name for variable in self.variables]
    
    xAxis = Enum(values='variablesNames')
    
    notXAxis = Property(List(Str), depends_on='xAxis, variablesNames')
    def _get_notXAxis(self):
        return [name for name in self.variablesNames if name != self.xAxis] 
    
    yAxis = Enum(values='notXAxis') 
    
    notAxes = List(TraitedPrismVariable)#, maxlen=len(self.variables)-2)

    def getScalarsIndicies(self):
        ''' Returns an evalable string corresponding to an extended slice of the results array. '''
        # Can't do this with a list comprehension because "else" is not allowed by the grammar/language.
        s = ''
        for i, variable in enumerate(self.variables):
            s += ':' if variable.name == self.xAxis or variable.name == self.yAxis else str(variable.valueIndex)
            s += ',' if i != len(self.variables) - 1 else ''
        return s

#    def _value_changed_for_variables(self, new): #MAGIC #DEPRECATED
    @on_trait_change('variables.value')#'variables:value')
    def updateSurface(self):
        self.surface.mlab_source.scalars = self.get_scalars()

    def get_scalars(self):
        scalars = eval('self.results[%s]' % self.getScalarsIndicies())
        if self.xAxisVariable.resultsIndex > self.yAxisVariable.resultsIndex:
            swapped = scalars.swapaxes(self.xAxisVariable.resultsIndex, self.yAxisVariable.resultsIndex)
            print scalars.shape, swapped.shape
            return swapped
        return scalars
    
    @on_trait_change('xAxis, yAxis')
    def change_data(self):
        self.set_x_y_variables()
        self.surface.mlab_source.reset(x=self.xAxisVariable.values, y=self.yAxisVariable.values, scalars=self.get_scalars())

    def set_x_y_variables(self):
        self.xAxisVariable = [variable for variable in self.variables if variable.name == self.xAxis][0]
        self.yAxisVariable = [variable for variable in self.variables if variable.name == self.yAxis][0]
    
    def plotSurface(self, first_time=False):
#        self.notXAxis = [name for name in self.variablesNames if name != self.xAxis]
#        self.notAxes = [variable for variable in self.variables if variable.name != self.xAxis and variable.name != self.yAxis]
        #TODO recalculate extent
        x = [variable.values for variable in self.variables if variable.name == self.xAxis]
        y = [variable.values for variable in self.variables if variable.name == self.yAxis]
        print x,y
        mlab = self.scene.mlab
        mlab.clf()
        self.set_x_y_variables()
        scalars = self.get_scalars()
        self.ranges = extent(x,y,scalars)
        self.surface = mlab.surf(scalars, colormap='jet', extent=normalized_extent(x, y, scalars))

    @on_trait_change('scene.activated')
    def add_actors(self):
        mlab = self.scene.mlab
        self.axes = mlab.axes(ranges=self.ranges, nb_labels=5, xlabel=self.xAxis, ylabel=self.yAxis, zlabel="Result")#, color=(0,0,0))
        self.title = mlab.title("%s" % self.property, size=0.5, height=0.85)#, color=(0,0,0))
        self.scalarbar = mlab.scalarbar(title ='Result', orientation='vertical', label_fmt='%.f', nb_labels=5)

#        # set scene's foreground and background colours
##        self.scene.scene_editor.background = (1,1,1) # white background
##        self.scene.scene_editor.foreground = (0,0,0) # black text
#        
##        self.scene.scene_editor.isometric_view() # finally works! but below is better
        self.scene.mlab.view(-45, 90, 4) # rotated 45 degrees, viewed side on, from a distance of 4  

#        # setting scalarbar title and label fonts
#        scalarbar.title_text_property.set(font_size=4)
#        scalarbar.label_text_property.set(font_size=4, italic=0, bold=0)#, line_spacing=0.5)
#        
#        # set position and size of scalarbar
#        scalar_bar_widget = self.surface.module_manager.scalar_lut_manager.scalar_bar_widget
#        # since VTK-5.2 the actual widget is accessed through its representation property (see https://mail.enthought.com/pipermail/enthought-dev/2009-May/021342.html) - we using at least VTK-5.4
#        scalar_bar_widget.representation.set(position=[0.9,0.08], position2=[0.09,0.42])

#   used to discover good view parameters 
    @on_trait_change('scene.view') #TODO change to when view is moved
    def print_view(self):
        print self.scene.mlab.view()
    
    def traits_view(self):
        return View(
#            Heading(self.property),
#            Spring(),
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
                style='custom',
            ),
            resizable=True,
            title='%s (%s)' % (self.property, self.fileName)
        )
    
    @classmethod
    def fromPsmFile(cls, fileName):
        '''
        load .psm file
        extract data in n-property dimensional array with result as the value
        create TraitedPrismPropertys
        return This
        '''
        
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
            
            #TODO find decimal places code
            
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
#            print resultValues, shape
            resultValues = resultValues.reshape(shape)
#            print resultValues[1,1,1,1]
            
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
                fileName=fileName # fileName is in HasTraits.__init__(self, **metadata)
            )
            listOfTraitedPrismResultsInstances.append(instance)
            
        return listOfTraitedPrismResultsInstances


#instances = TraitedPrismResults.fromPsmFile('4_variables.psm')
#instances = TraitedPrismResults.fromPsmFile('3_results.psm')
#instances = TraitedPrismResults.fromPsmFile('2_properties.psm')
#instances = TraitedPrismResults.fromPsmFile('/home/jvb/Desktop/motifs/Const/modelChecking/Const_results.mc2')
#instances = TraitedPrismResults.fromPsmFile('results.psm')
instances = TraitedPrismResults.fromPsmFile('1-4_variables.psm')

#for instance in instances:
#    instance.print_traits()
instances[0].plotSurface()
instances[0].configure_traits()


    
class TraitedPrismResultsPlotter(HasTraits):
    results = List(TraitedPrismResults)

    traits_view = View(
        Item('results', style='custom', editor=ListEditor(use_notebook=True))
    )
    
    
    
    
    
    
    
    
    

# http://markmail.org/search/?q=RangeEditor+is+still+the+intermediate+value%20list:com.enthought.mail.enthought-dev#query:RangeEditor%20is%20still%20the%20intermediate%20value%20list%3Acom.enthought.mail.enthought-dev+page:1+mid:ypjjb752y3c5uklx+state:results    

'''
Hello all,

I have a class with a trait 'value' that I want to edit with a
RangeEditor but I want it to only have certain values within that range.

To do this I have another trait 'values' which a sorted list of possible
values and when 'value' changes I search 'values' for the closet value
and reassign 'value' with that. This all takes place in the
'_value_changed' method. 

The 'value' gets set correctly but the value displayed by the
RangeEditor is still the intermediate value.

Can you please tell me how can I trigger the RangeEditor to show the
correct value and whether there is a better way of achieving what I want
to do. (I also want the index of the value in 'values' for slicing an
array.)

Thanks

Jon

# start code

from enthought.traits.api import *
from enthought.traits.ui.api import *
from numpy import array, arange, zeros, float32
from bisect import bisect
    
class Variable(HasTraits):
    name = Str
    values = List
    start = Float
    stop = Float
    value = Range('start', 'stop', 'start') 
    valueIndex = Int
    
    def _value_changed(self, new):
        valueIndex = self.findIndexInValues(new)
        value = self.values[valueIndex]
        if value != new:
            self.value = value
        self.valueIndex = valueIndex
        print self.value

    def findIndexInValues(self, value):
        # find the index of the item closest to value in self.values
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

    traits_view = View(
        HGroup(
            Item('name', show_label=False, style='readonly'),
            Item('value', show_label=False),
        )
    )

class Results(HasTraits):
    variables = List(Variable)

    def default_traits_view(self):
        return View(
            Item('variables', style='custom',
editor=ListEditor(style='custom', mutable=False)),
            buttons=['OK'],
        )
    
values = [1,3.3,2,0]
values = sorted(values)
Results(
    variables=[Variable(
        name='test',
        values=values,
        start=values[0],
        stop=values[-1]
    )]
).configure_traits()

# end code

when the slider is dragged it prints:
0.0
1.0
2.2
3.3
but shows intermediate values like 2.26116 (picture attached).
'''

'''
Jonathan,

It sounds like what you really want to do is provide your own 'evaluate' 
method, something like this:

def my_evaluate(value):
    if value < 2:
        raise ValueError('value is too small'):
    else:
        return value**2

You can also specify your own 'format', such as "%02.2f".

Bryce
'''

'''
Hi Bryce,

'format' helped me to correct the look of the range labels, thanks.

'evaluate' helps me get the correct value but the RangeEditor still
displays the intermediate value (see attached).

Jon

'''
