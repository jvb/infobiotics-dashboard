import os; os.environ['ETS_TOOLKIT'] = 'qt4'
from enthought.traits.api import HasTraits, List, Float, Str, Int, Range, Array, Instance, Unicode, Enum, Property, Button, on_trait_change, Tuple, cached_property, Bool#, Color
from enthought.traits.ui.api import View, Item, VGroup, HGroup, RangeEditor, ListEditor, Label, Spring, TextEditor, CheckListEditor#, InstanceEditor
import numpy as np
from bisect import bisect
#from enthought.mayavi.core.ui.api import MlabSceneModel, SceneEditor#, MayaviScene 
#from enthought.tvtk.pyface.api import Scene
#from enthought.mayavi.core.api import PipelineBase
#from infobiotics.commons.mayavi import extent
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from infobiotics.commons.traits.ui.qt4.matplotlib_figure_editor import MPLFigureEditor 

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
                    editor=TextEditor(format_str=self.format),
                ),
            ),
        )


class TraitedPrismResults(HasTraits):
    property = Str
    variables = List(TraitedPrismVariable)
    results = Array
    
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
    
    yAxis = Enum(values='notXAxisVariablesNames') #TODO change name so as not to conflict with mayavi
    
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

    scalars_indicies = Property(Str, depends_on='xAxis, variables:valueIndex')
    @cached_property
    def _get_scalars_indicies(self):
        ''' Returns an evalable string corresponding to an extended slice of the results array. '''
        # Can't do this with a list comprehension because "else" is not allowed by the grammar/language.
        s = ''
        for i, variable in enumerate(self.variables):
#            s += ':' if variable.name == self.xAxis or variable.name == self.yAxis else str(variable.valueIndex)
            s += ':' if variable.name == self.xAxis else str(variable.valueIndex)
            if i < len(self.variables) - 1:
                s += ','
        return s

    scalars = Property(Array, depends_on='scalars_indicies')
    @cached_property
    def _get_scalars(self):
        ''' Return a 1-dimensional slice of the results array. '''
        scalars = eval('self.results[%s]' % self.scalars_indicies)
        return scalars

   
    min_result = Property(Float, depends_on='results')
    @cached_property
    def _get_min_result(self):
        return np.min(self.results)
    
    max_result = Property(Float, depends_on='results')
    @cached_property
    def _get_max_result(self):
        return np.max(self.results)
    
    dependent_axis_label = Str
    def _dependent_axis_label_default(self):
#        return self.property.split('=')[0].strip() #TODO
        return 'Result'

    @on_trait_change('xAxis, yAxis, variables:value, variables:plot')
    def update_figure(self):
        axes = self.axes
        axes.clear()
        axes.set_title(self.property)
        axes.set_xlabel(self.xAxis)
        axes.set_ylabel('Result')
        axes.grid(True)

        x = self.xAxisVariable.values



        if len(self.notXAxisVariablesNames) >= 1:
            # slice results without changing self.yAxisVariable.valueIndex
            for j, v in enumerate(self.yAxisVariable.values):
                s = ''
                for i, variable in enumerate(self.variables):
                    if variable.name == self.xAxis:
                        s += ':' 
                    elif variable.name == self.yAxis:
                        s += str(j)
                    else:
                        s += str(variable.valueIndex)
                    if i < len(self.variables) - 1:
                        s += ','
                scalars = eval('self.results[%s]' % s)
                label='%s=%s' % (self.yAxis, v)
                for variable in self.variables:
                    if variable not in (self.xAxisVariable, self.yAxisVariable):
                        label += ', %s=%s' % (variable.name, variable.value)
                axes.plot(x, scalars, label=label)
            
            if self.legend:
                self.axes.legend(loc='best')
            
            print self.yAxis, self.notXAxisVariablesNames
                
        else:
            line = axes.plot(x, self.scalars)

        # can only set axes limits after plotting
        self.axes.set_xlim(np.min(x), np.max(x))
        self.axes.set_ylim(self.min_result, self.max_result)
        
        if self.figure.canvas is not None:
            self.figure.canvas.draw()
    
    legend = Bool(True)
    
    figure = Instance(Figure)

    def __init__(self, **traits):
        super(HasTraits, self).__init__(**traits)
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.update_figure()
    
    def traits_view(self):
        return View(
            VGroup(
                HGroup(
                    Label('Plot of'),
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
                    editor=MPLFigureEditor(toolbar=True), #TODO Figure.set_figsize_inches( (w,h) ) # http://www.scipy.org/Cookbook/Matplotlib/AdjustingImageSize
#                    height=250,
#                    width=300, 
                    resizable=True
                ),
                show_border=True,
            ),
            Item('detach', show_label=False),
            resizable=True,
            title='%s' % self.property,
        )

    detach = Button
    def _detach_fired(self):
        self.edit_traits()

    


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

#    selected = Instance(TraitedPrismResults)
#    def _selected_default(self):
#        return self.results[0]
#    def _selected_changed(self):
#        print self.selected

    def traits_view(self):
        return View(
            VGroup(
                Item('results', show_label=False, style='custom', 
                    editor=ListEditor(use_notebook=True, page_name='.property', 
#                        selected='selected', # setting selected doesn't seem to change tab 
#                        dock_style='tab', # dunno what this does
                    ),
                ),
                show_border=True,
            ),
            title='%s' % self.fileName,
            resizable=True,
        )


if __name__ == '__main__':
    main = TraitedPrismResultsPlotter()
    main.load('1-4_variables.psm')
#    main.load('2d_function.psm')
#    main.selected = main.results[1]
    main.configure_traits()
        
