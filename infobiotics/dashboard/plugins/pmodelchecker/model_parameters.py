from __future__ import with_statement
import os; os.environ['ETS_TOOLKIT']='qt4'
from enthought.traits.api import HasTraits, Str, Float, Enum, Property
from enthought.traits.ui.api import View, Item#, HGroup
    
model_parameter_view = View(
#    Item('id', style='readonly', label='ID'),
#    Item('name', style='readonly'),
    Item('description', style='readonly'),
    Item('range_or_value', style='custom'),
#    HGroup(
#        Item('lower'),
#        Item('step'),
#        Item('upper'),
#        visible_when='object.range_or_value == "range"',
#    ),
    Item('lower', visible_when='object.range_or_value == "range"'),
    Item('step', visible_when='object.range_or_value == "range"'),
    Item('upper', visible_when='object.range_or_value == "range"'),
    Item('value', visible_when='object.range_or_value == "value"'),
    
    title='Edit model parameter',
    width=400, #height=200,
    resizable=True,
    buttons = ['OK', 'Cancel'] 
)    
    
class ModelParameter(HasTraits):
    ''' modelVariable or ruleConstant. '''
    def traits_view(self):
        model_parameter_view.title=self.name
        return model_parameter_view
    id = Str
    name = Str
    description = Str
    range_or_value = Enum(['range','value'])
    lower = Float(0)
    step = Float(1.0)
    upper = Float(2.0)
    value = Float(1.0)
    value_string = Property(depends_on='range_or_value, value, lower, step, upper')
    def _get_value_string(self):
        if self.range_or_value == 'value':
            return '%s=%s' % (self.name, self.value)
        else:
            return '%s=%s:%s:%s' % (self.name, self.lower, self.step, self.upper)
    
    def __repr__(self):
        if self.range_or_value == 'value':
            return '''ModelParameter(
    id = %s,
    name = %s, 
    description = %s, 
    value = %s, 
)''' % (self.id, self.name, self.description, self.value)
        else:
            return '''ModelParameter(
    id = %s,
    name = %s, 
    description = %s, 
    lower = %s, 
    step = %s, 
    upper = %s, 
)''' % (self.id, self.name, self.description, self.lower, self.step, self.upper)

    def __str__(self):
        return super(HasTraits, self).__str__()


from enthought.traits.api import Int 

class MoleculeConstant(ModelParameter):
    ''' Subclass of ModelParameter than only allows integer values. '''
    value = Int(1)
    lower = Int(0)
    step = Int(1)
    upper = Int(2)
    
    
from xml.sax import ContentHandler

class ModelParametersXMLReader(ContentHandler):
    ''' Parses modelParameters.xml created by pmodelchecker --task=Translate
    and inserts parameters into dictionary passed to __init__.

    Adapted from ParamsXMLReader.   
    
    See also http://docs.python.org/library/xml.sax.handler.html
    
    '''
    def __init__(self):
        self.modelVariables = []
        self.ruleConstants = []
        self.moleculeConstants = []
        self.switch1 = ''
        self.switch2 = ''
        ContentHandler.__init__(self)

    def startElement(self, name, attrs):
        if name == 'modelVariables':
            self.switch1 = name
        elif name == 'ruleConstants':
            self.switch1 = name
        elif name == 'moleculeConstants':
            self.switch1 = name
        elif name in ('variable', 'constant'):
            if self.switch1 == 'moleculeConstants':
                self.model_parameter = MoleculeConstant()
            else:
                self.model_parameter = ModelParameter()
            self.model_parameter.id=attrs['id']
        elif name == 'name':
            self.switch2 = name
        elif name == 'description':
            self.switch2 = name

    def characters(self, content):
        # need to strip and then avoid empty content
        content = content.strip()
        if len(content) > 0:
            if self.switch2 == 'name':
                self.model_parameter.name = content
            elif self.switch2 == 'description':
                self.model_parameter.description = content
     
    def endElement(self, name):
        if name in ('variable', 'constant'):
            getattr(self, self.switch1).append(self.model_parameter)
#            self.model_parameter = None
#            self.switch2 = ''


from enthought.traits.api import File, List, Tuple, Instance, DelegatesTo
from enthought.traits.ui.table_column import ObjectColumn, ExpressionColumn
from infobiotics.dashboard.plugins.experiments.params_experiment import ParamsExperiment
import os

class ModelParameters(HasTraits):
    file = DelegatesTo('prism_experiment')
    prism_experiment = Instance(ParamsExperiment)
    _modelVariables = List(ModelParameter) 
    _ruleConstants = List(ModelParameter) 
    _moleculeConstants = List(MoleculeConstant) 
    
    def _file_changed(self):
        model_parameters_file = os.path.join(os.path.dirname(self.file), 'modelParameters.xml')
        try:
            with open(model_parameters_file, 'rb') as fh:
                from xml import sax
                parser = sax.make_parser()
                handler = ModelParametersXMLReader()
                parser.setContentHandler(handler)
                error = None
                try:
                    parser.parse(fh) # read parameters from file into dictionary
                except sax._exceptions.SAXParseException, e: 
                    print e
                self._modelVariables = handler.modelVariables
                self._ruleConstants = handler.ruleConstants
                self._moleculeConstants = handler.moleculeConstants
        except IOError, e:
            print e, 'model_parameters.ModelParameters._file_changed()'
    
    _all_model_parameters = Property(depends_on='_modelVariables, _ruleConstants, _moleculeConstants')
    def _get__all_model_parameters(self):
        return self._modelVariables + self._ruleConstants + self._moleculeConstants
    
    model_parameters = Property(depends_on='_all_model_parameters', desc='example_parameter_name=10, another_parameter=low:high:step')
    def _get_model_parameters(self):
        return ','.join([model_parameter.value_string for model_parameter in self._all_model_parameters])
    def _set_model_parameters(self):
        ''' loading from a string '''
        pass

    def __len__(self):
        return len(self._modelVariables) + len(self._ruleConstants) + len(self._moleculeConstants)

    def traits_view(self):
        return View(
            editable_modal_parameters_group,
            buttons=['OK','Cancel'],
            title='Edit model parameters',
            resizable=True,
        )
    
    dclick = Tuple(Instance(ModelParameter), Instance(ObjectColumn))
    def _dclick_changed(self, info):
#        ModelParameterHandler().edit_traits(context={'object':self.dclick[0]})
        self.dclick[0].edit_traits(kind='modal')

    selected_model_parameter = Instance(ModelParameter)
    def _selected_model_parameter_changed(self):
        print self.selected_model_parameter
    
from enthought.traits.ui.api import Group, TableEditor

model_parameters_group = Group(
    Item('_all_model_parameters', #FIXME change to _moleculeConstants if necessary
        show_label=False, 
        editor=TableEditor(
            columns=[
                ObjectColumn(name='name',
                    width=0.25,
                    editable=False,
                ),
                ExpressionColumn(name='value',
                    expression='object.value_string.split("=")[1]',
                    width=0.25,
                    tooltip='Double-click to edit model parameter',
                ),
                ObjectColumn(name='description',
                    width=0.5,
                    editable=False,
                ),
            ],
            sortable=True,
            dclick='dclick',
            selected='selected_model_parameter',
#            edit_view=model_parameter_view,
        ),
    ),
    label='Model parameters',
)


from enthought.traits.ui.api import VSplit 

editable_modal_parameters_group = VSplit(
    model_parameters_group,
    Item('selected_model_parameter', style='custom', show_label=False),
)


if __name__ == '__main__':
    execfile('prism_experiment.py')

#if __name__ == '__main__':
#    object = ModelParameters(file='/home/jvb/phd/eclipse/infobiotics/dashboard/examples/pmodelchecker/Const/modelCheckingPRISM/Const_PRISM.params')
#    PRISMExperimentHandler().configure_traits(context={'object':object})
