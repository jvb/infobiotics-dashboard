from __future__ import with_statement
from enthought.traits.api import HasTraits, Str, Float, Enum, Property
from enthought.traits.ui.api import View, Item, HGroup, VGroup

range_or_value_group = VGroup(
    Item('range_or_value', style='custom'),
    HGroup(
        Item('lower'),
        Item('step'),
        Item('upper'),
        enabled_when='object.range_or_value == "range"',
    ),
    Item('value', enabled_when='object.range_or_value == "value"'),
)
    
model_parameter_view = View(
    VGroup(
#        Item('id', style='readonly', label='ID'),
#        Item('name', style='readonly'),
        Item('description', style='readonly'),
        range_or_value_group,
        show_border=True,
    ),
    title='Edit model parameter',
    width=400,
    resizable=True,
    buttons = ['OK', 'Cancel'] 
)    

class PModelCheckerParameter(HasTraits):
    range_or_value = Enum(['range','value'])
    lower = Float(0)
    step = Float(1.0) # Range('lower','upper', 'value')
    upper = Float(2.0) #FIXME these aren't good defaults
    value = Float(1.0)
    
class ModelParameter(PModelCheckerParameter):
    ''' modelVariable or ruleConstant. '''
    def traits_view(self):
        model_parameter_view.title=self.name
        return model_parameter_view
    id = Str
    name = Str
    description = Str
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
    ''' Parses modelParameters.xml created by pmodelchecker --task=Translate.

    Adapted from ParamsXMLReader.   
    
    See also http://docs.python.org/library/xml.sax.handler.html
    
    '''
    def __init__(self):
        self.modelVariables = []
        self.ruleConstants = []
        self.moleculeConstants = []
        self.rewardConstants = []
        self.switch1 = ''
        self.switch2 = ''
        ContentHandler.__init__(self)

    elements1 = ('modelVariables', 'ruleConstants', 'moleculeConstants', 'rewardConstants')
    elements2 = ('variable', 'constant')
    
    def startElement(self, name, attrs):
        if name in self.elements1:
            self.switch1 = name
        elif name in self.elements2 and self.switch1 in self.elements1:
            if self.switch1 == 'moleculeConstants':
                self.model_parameter = MoleculeConstant()
            elif self.switch1 == 'ruleConstants': return # TODO
            elif self.switch1 == 'modelVariables':
                self.model_parameter = ModelParameter()
            elif self.switch1 == 'rewardConstants': return #TODO
            self.model_parameter.id=attrs['id']
        elif name in ('name', 'description', 'value'):
            self.switch2 = name

    def characters(self, content):
        # need to strip and then avoid empty content
        content = content.strip()
        if len(content) > 0:
            if self.switch2 == 'name':
                self.model_parameter.name = content
            elif self.switch2 == 'description':
                self.model_parameter.description = content
            elif self.switch2 == 'value' and self.switch1 == 'rewardConstants':
                pass#self.model_parameter.value = content #TODO
     
    def endElement(self, name):
        if name in self.elements2:
            getattr(self, self.switch1).append(self.model_parameter)


from enthought.traits.api import File, List, Tuple, Instance, DelegatesTo
from enthought.traits.ui.table_column import ObjectColumn, ExpressionColumn
import os
from enthought.traits.directory import Directory
from common.files import read

class ModelParameters(HasTraits):
    _cwd = Directory
    modelVariables = List(ModelParameter) 
    ruleConstants = List(ModelParameter) 
    moleculeConstants = List(MoleculeConstant) 
    
    def __cwd_changed(self):
        model_parameters_file = os.path.join(self._cwd, 'modelParameters.xml')
        try:
            with read(model_parameters_file) as f:
                from xml import sax
                parser = sax.make_parser()
                handler = ModelParametersXMLReader()
                parser.setContentHandler(handler)
                try:
                    parser.parse(f) # read parameters from file into dictionary
                except sax._exceptions.SAXParseException, e: 
                    print e
                self.modelVariables = handler.modelVariables
                self.ruleConstants = handler.ruleConstants
                self.moleculeConstants = handler.moleculeConstants
        except IOError, e:
            print e, 'ModelParameters.__cwd_changed()'
    
    _all_model_parameters = Property(depends_on='ruleConstants, moleculeConstants')#modelVariables, 
    def _get__all_model_parameters(self):
#        return self.modelVariables + self.ruleConstants + self.moleculeConstants
        return self.ruleConstants + self.moleculeConstants
    
    model_parameters = Property(depends_on='_all_model_parameters', desc='example_parameter_name=10, another_parameter=low:high:step')

    def _get_model_parameters(self):
        return ','.join([model_parameter.value_string for model_parameter in self._all_model_parameters])
    
    def _set_model_parameters(self, model_parameters):
        model_parameters = model_parameters.split(',')
        for model_parameter in model_parameters: 
            name, value = model_parameter.split('=')
            if ':' in value:
                range_or_value = 'range'
                lower, step, upper = value.split(':')
            else:
                range_or_value = 'value'
                value = value
            for model_parameter in self._all_model_parameters:
                if model_parameter.name == name:
                    if range_or_value == 'value':
                        model_parameter.value = int(value) if isinstance(model_parameter, MoleculeConstant) else float(value)
                    else:
                        model_parameter.lower = int(lower) if isinstance(model_parameter, MoleculeConstant) else float(lower)
                        model_parameter.step = int(step) if isinstance(model_parameter, MoleculeConstant) else float(step)
                        model_parameter.upper = int(upper) if isinstance(model_parameter, MoleculeConstant) else float(upper)
                    model_parameter.range_or_value = range_or_value
                    break

    def __len__(self):
        return len(self.modelVariables) + len(self.ruleConstants) + len(self.moleculeConstants)

    def traits_view(self):
        return View(
            model_parameters_group,
            buttons=['OK','Cancel'],
            title='Edit model parameters',
            resizable=True,
        )
    
    dclick = Tuple(Instance(ModelParameter), Instance(ObjectColumn))
    
    def _dclick_changed(self, info):
        self.dclick[0].edit_traits(kind='livemodal')

    
from enthought.traits.ui.api import Group, TableEditor

model_parameters_group = Group(
    Item('_all_model_parameters', #FIXME change to moleculeConstants if necessary
        show_label=False, 
        editor=TableEditor(
            columns=[
                ObjectColumn(name='name',
                    width=0.25,
                ),
                ExpressionColumn(name='value',
                    expression='object.value_string.split("=")[1]',
                    width=0.25,
                    tooltip='Double-click to edit model parameter',
                ),
                ObjectColumn(name='description',
                    width=0.5,
                ),
            ],
            sortable=True,
            dclick='dclick',
            editable=False,
        ),
    ),
#    label='Model parameters',
)


if __name__ == '__main__':
    execfile('prism_experiment.py')
