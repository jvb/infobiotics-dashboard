from enthought.traits.api import HasTraits, Str, DelegatesTo, Instance, self
from enthought.traits.ui.api import Handler, View, Item, Group

class Model(HasTraits):
    string = Str
    view = View(
        Item('string', style='simple'),
        title='Model',
    )
#    handler = Controller
    
    
class Controller(Handler):
    pass

view = View(
    Item('string', style='custom'),
    handler=Controller(),
    title='Handler',
)



class Parameters(HasTraits):
    parameters = self
    a = Str('billy')
    b = Str('silly')

class Experiment(HasTraits):
    parameters = Parameters
#    parameters = Instance(Parameters, ())
#    a = DelegatesTo('parameters')
    c = Str('willy')

parameters_group = Group(
    'parameters.a', 'parameters.b',
    'a',
)

class ParametersHandler(Handler):
    view = View(
        parameters_group,
        buttons=['Load', 'save'],
    )
    
    def save(self, info):
        print 'save clicked'

class ExperimentHandler(Handler):
    view = View(
        'experiment.c',
        parameters_group,
        buttons = ['Load', 'Save', 'Perform'],
    )
    


if __name__ == '__main__':
#    Model().configure_traits()
#    Model().configure_traits(view=view)

    parameters = Parameters()
    print parameters, parameters.parameters

#    print parameters.b, parameters.a

#    parameters.configure_traits()

#    ParametersHandler().configure_traits(
#        context={
#            'parameters':parameters,
#            'object':parameters,
#        },
#    )

#    parameters.configure_traits(view=View('a','b', handler=ExperimentHandler()))
        
#    e = Experiment(parameters=parameters)
#
#    ExperimentHandler().configure_traits(
#        context={
#            'experiment':e,
#            'parameters':e.parameters,
#        }
#    )