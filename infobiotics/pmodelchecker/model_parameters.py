from __future__ import with_statement
from enthought.etsconfig.api import ETSConfig
ETSConfig.toolkit = 'qt4'
from enthought.traits.api import (
    HasTraits, Str, Float, Int, Undefined, Range, Enum, Property, List, Tuple,
    Instance, Dict, cached_property
) 
from enthought.traits.ui.api import (
    View, Item, HGroup, VGroup, TableEditor, TextEditor, Group, VSplit,
)
from xml.sax import ContentHandler
from xml import sax
from enthought.traits.ui.table_column import ObjectColumn, ExpressionColumn
import os.path
from infobiotics.commons.traits.api import RelativeDirectory
from infobiotics.commons.api import read

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
    buttons=['OK', 'Cancel'] 
)    

class ModelVariable(HasTraits):
    id = Str
    name = Str
    description = Str

    def __repr__(self):
        return '''%s(
    id = '%s',
    name = '%s', 
    description = '%s', 
)''' % (self.__class__.__name__, self.id, self.name, self.description)

    
class RuleConstant(ModelVariable):

    def traits_view(self):
        model_parameter_view.title = self.name
        return model_parameter_view
    
    kind = Str('rule constant')

    value = Float(Undefined)
    lower = Float(Undefined)
    step = Range('lower', 'upper', 'value', editor=TextEditor)
    upper = Float(Undefined)
    
    range_or_value = Enum(['range', 'value'])

    value_string = Property(depends_on='range_or_value, value, lower, step, upper')
 
    def _get_value_string(self):
        if self.range_or_value == 'value':
            return '%s=%s' % (self.name, self.value)
        else:
            return '%s=%s:%s:%s' % (self.name, self.lower, self.step, self.upper)
    
    def __repr__(self):
        if self.range_or_value == 'value':
            return '''%s(
    id = '%s',
    name = '%s', 
    description = '%s', 
    value = %s, 
)''' % (self.__class__.__name__, self.id, self.name, self.description, self.value)
        else:
            return '''%s(
    id = '%s',
    name = '%s', 
    description = '%s', 
    lower = %s, 
    step = %s, 
    upper = %s, 
)''' % (self.__class__.__name__, self.id, self.name, self.description, self.lower, self.step, self.upper)

    def __str__(self): #TODO
        return super(HasTraits, self).__str__()


class MoleculeConstant(RuleConstant):
    ''' As RuleConstant but only allows integer values. '''

    kind = 'molecule constant'
    
    lower = step = upper = value = Int
    
    def _value_changed(self):
        self.lower = self.step = self.upper = self.value

    def _get_value_string(self):
        return '%s=%s' % (self.name, self.value)

    def evaluate(self, value):
        try:
            return int(eval(value))
        except:
            raise TraitError()
    
    
class RewardConstant(HasTraits):
    name = Str
    description = Str
    value = Int(Undefined) 
    
    def __repr__(self):
        return '''%s(
    name = '%s', 
    description = '%s', 
    value = %s, 
)''' % (self.__class__.__name__, self.name, self.description, self.value)


class ModelParametersXMLReader(ContentHandler):
    ''' From modelParameters.xml (pmodelchecker <params_file> --task=Translate)

    Adapted from ParamsXMLReader.
    See also http://docs.python.org/library/xml.sax.handler.html
    '''
    def __init__(self):
        ContentHandler.__init__(self) # can't use super() here !?
        self.modelVariables = []
        self.ruleConstants = []
        self.moleculeConstants = []
        self.rewardConstants = []
        self.switch1 = ''
        self.switch2 = ''

    elements1 = ('modelVariables', 'ruleConstants', 'moleculeConstants', 'rewardConstants')
    elements2 = ('variable', 'constant')
    
    def startElement(self, name, attrs):
        if name in self.elements1:
            self.switch1 = name
        elif name in self.elements2 and self.switch1 in self.elements1:
            if self.switch1 == 'modelVariables':
                self.object = ModelVariable()
            elif self.switch1 == 'ruleConstants':
                self.object = RuleConstant()
            elif self.switch1 == 'moleculeConstants':
                self.object = MoleculeConstant()
            elif self.switch1 == 'rewardConstants':
                self.object = RewardConstant()
            if self.switch1 in ('modelVariables', 'ruleConstants', 'moleculeConstants'):
                self.object.id = attrs['id']
        elif name in ('name', 'description', 'value'):
            self.switch2 = name

    def characters(self, content):
        # need to strip and then avoid empty content
        content = content.strip()
        if len(content) > 0:
            if self.switch2 == 'name':
                self.object.name = content
            elif self.switch2 == 'description':
                self.object.description = content
            elif self.switch2 == 'value' and self.switch1 == 'rewardConstants':
                self.object.value = int(content)
     
    def endElement(self, name):
        if name in self.elements2:
            getattr(self, self.switch1).append(self.object)


class ModelParameters(HasTraits):
    directory = RelativeDirectory
    modelVariables = List(ModelVariable) 
    ruleConstants = List(RuleConstant) 
    moleculeConstants = List(MoleculeConstant)
    rewardConstants = List(RewardConstant)
    rewardConstant_descriptions = List(Str)
    rewardConstant = Enum(Undefined, values='rewardConstant_descriptions')
    
    def _rewardConstant_changed(self):
        self.rewardConstants[self.rewardConstant_descriptions.index(self.rewardConstant)].value #TODO do something with this value
    
    def _directory_changed(self):
        model_parameters_file = os.path.join(self.directory, 'modelParameters.xml')
        try:
            with read(model_parameters_file) as f:
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
                self.rewardConstants = handler.rewardConstants
                self.rewardConstant_descriptions = [rewardConstant.description.replace('A', 'a') for rewardConstant in handler.rewardConstants]
                self.rewardConstant = self.rewardConstant_descriptions[0]
        except IOError, e:
            print e, 'ModelParameters._directory_changed()'
    
    all_model_parameters = Property(List(RuleConstant), depends_on='ruleConstants, moleculeConstants') 
#    @cached_property
    def _get_all_model_parameters(self):
        return self.ruleConstants + self.moleculeConstants
    
    model_parameters = Property(Str, depends_on='all_model_parameters.value_string', desc='parameter=10, another_parameter=low:high:step')
#    @cached_property
    def _get_model_parameters(self):
        model_parameters = ','.join([model_parameter.value_string for model_parameter in self.all_model_parameters]) 
#        print model_parameters
#        print self.all_model_parameters[0]
        return model_parameters 
    
    def _set_model_parameters(self, model_parameters):
        model_parameters = model_parameters.split(',')
        for model_parameter in model_parameters:
            if len(model_parameter) == 0: continue # guard
            name, value = model_parameter.split('=')
            if ':' in value:
                range_or_value = 'range'
                lower, step, upper = value.split(':')
            else:
                range_or_value = 'value'
                value = value
            for model_parameter in self.all_model_parameters:
                if model_parameter.name == name:
                    if isinstance(model_parameter, MoleculeConstant):
                        type = int
                    elif isinstance(model_parameter, RuleConstant):
                        type = float
                    if range_or_value == 'value':
                        model_parameter.value = type(value)
                    else:
                        model_parameter.lower = type(lower)
                        model_parameter.step = type(step)
                        model_parameter.upper = type(upper)
                    model_parameter.range_or_value = range_or_value
                    break

    def __len__(self): #TODO does this ever get called?
        return len(self.ruleConstants) + len(self.moleculeConstants) 

#    def traits_view(self):
#        return View(
#            model_parameters_group,
#            buttons=['OK','Cancel'],
#            title='Edit model parameters',
#            resizable=True,
#        )
    
    
    dclick = Tuple(Instance(RuleConstant), Instance(ObjectColumn))
    def _dclick_changed(self, info):
        self.dclick[0].edit_traits(kind='livemodal')
ruleConstants_table_editor = TableEditor(
    dclick='dclick',
    columns=[
        ObjectColumn(name='name',
            width=0.4,
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
    editable=False,
) 

#def evaluate_int(value):
#    try:
#        return int(eval(value))
#    except:
#        raise TraitError()
    
moleculeConstants_table_editor = TableEditor(
    columns=[
        ObjectColumn(name='name',
            width=0.4,
            editable=False,
        ),
        ObjectColumn(name='value',
            width=0.2,
            editor=TextEditor(
#                evaluate=int,#evaluate_int,
                evaluate_name='evaluate', # see MoleculeConstant.evaluate(value)
            )
        ),
        ObjectColumn(name='description',
            width=0.4,
            editable=False,
        ),
    ],
    sortable=False,
) 

model_parameters_group = Group(
    VGroup(
        Item(label='Molecule constants:'),
        Item('moleculeConstants',
            show_label=False,
            editor=moleculeConstants_table_editor,
        ),
        visible_when='len(object.moleculeConstants) > 0',
    ),
    VGroup(
        Item(label='Rule constants:'),
        Item('ruleConstants',
            show_label=False,
            editor=ruleConstants_table_editor,
        ),
        visible_when='len(object.ruleConstants) > 0',
    ),
#    Item(label='Rewards:'),
#    Item('rewardConstant', show_label=False),
)


if __name__ == '__main__':
    execfile('pmodelchecker_params.py')
    
