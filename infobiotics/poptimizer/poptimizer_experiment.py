
from enthought.traits.ui.tabular_adapter \
    import TabularAdapter

class Module(HasTraits):
    '''PosReg(X=3,Y=1)''' 
    name = Str
    parameters = DictStrStr
    parameters_str = Str
    

        


from PyQt4.QtGui import QWidget, QSizePolicy
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.figure import SubplotParams
from enthought.traits.ui.qt4.editor import Editor
from enthought.traits.ui.basic_editor_factory import BasicEditorFactory

class _MPLFigureEditor(Editor):
    scrollable = True
    widget = Instance(QWidget)
    
    def init(self, parent):
        ''' self.value is the trait being edited. '''
        
#        # with additional widgets such as the Matplotlib navigation toolbar
#        widget = QWidget()
#        widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
#        layout = QGridLayout(widget)
#        mpl_control = FigureCanvas(self.value)
#        layout.addWidget(mpl_control)
#        toolbar = NavigationToolbar(mpl_control, widget)
#        layout.addWidget(toolbar)

        # without additional widgets
        widget = FigureCanvas(self.value)
        widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
#        widget.setMinimumSize(300,300)
        
        self.control = widget
#        self.set_tooltip('')
    
    def update_editor(self):
        pass
#        self.control.update()
    

class MPLFigureEditor(BasicEditorFactory):
    klass = _MPLFigureEditor



class POptimizerExperiment(Experiment):

    best_fitnesses = List(Float)
    figure = Instance(Figure, 
        Figure(
            (5.0, 3.0), 
            facecolor='#efebe7', 
            edgecolor='#efebe7',
            subplotpars=SubplotParams(
                left=0.15,
                bottom=0.15,                
            ),
        )
    )
    status = Str
    current_best_fitness = Float
    current_fittest_module_list = List(Module)
    zero = Constant(0)
    parameter_optimization_total = Int(1)
    parameter_optimization_subtotal = Range('zero', 'parameter_optimization_total')
    current_generation = Int # starting from 0
    generations = Constant(10) #TODO remove, get 'maxgeno' from 'parameters' instead
    overall_progress = Property(Range(0.0, 100.0), depends_on='parameter_optimization_subtotal, current_generation')
    
    params_program = 'poptimizer'
#    pattern_list = [
#        'initialization',
#        'parameter optimization [0-9]+/[0-9]+',
#        '[0-9]+ [0-9]+[.][0-9]+ .+\n',
#        'simulate final model',
#    ]
    def _pattern_list_default(self):
        return [
            'initialization',
            'parameter optimization [0-9]+/[0-9]+',
            '[0-9]+ [0-9]+[.][0-9]+ .+\n',
            'simulate final model',
        ]
    
    def _starting_fired(self):
        print '_starting_fired'
        self.axes = self.figure.add_subplot(111)
    
    def pattern_matched(self, pattern_index, match):
#        '''
#        initialization
#        parameter optimization 1/2
#        0 388.51 PosReg(X=3,Y=1) NegReg(X=1,Y=3) UnReg(X=3) UnReg(X=2) 
#        simulate final model
#        '''
#        print '>>>', match
        if pattern_index == 0:
            self.status = 'Initialising'
            self.axes = self.figure.add_subplot(111)
        elif pattern_index == 1:
            self.status = 'Optimizing parameters'
            split = match.split(' ')[2].split('/')
            self.parameter_optimization_subtotal = int(split[0]) 
            self.parameter_optimization_total = int(split[1])
        elif pattern_index == 2:
            split = match.split(' ')
            self.current_generation = int(split[0]) + 1 
            self.current_best_fitness = float(split[1])
            
            # should be POptimizerExpectWithPlo2.pattern_matched
            self.best_fitnesses.append(self.current_best_fitness)
            self.axes.clear()
            self.axes.set_xlabel('Generation')
            self.axes.set_ylabel('Fitness')
            self.axes.grid(True)
            self.axes.plot(
                self.best_fitnesses,
            )
            self.axes.set_xlim(0, self.generations - 1)
            self.axes.set_ylim(ymin=0)
            self.figure.canvas.draw()

            self.current_fittest_module_list = [Module(name=module.split('(')[0], parameters_str=module.split('(')[1].strip(')'), parameters=dict([parameter.split('=') for parameter in module.split('(')[1].strip(')').split(',')])) for module in split[2:-1]]
            self.parameter_optimization_subtotal= 0
        elif pattern_index == 3:
            self.status = 'Simulating final model'
#            self.overall_progress = 99
        elif pattern_index > 3:
            ParamsExpect.pattern_matched(self, pattern_index, match)
    
    def _finished_fired(self):
        self.status = 'Finished'
#        self.overall_progress = 100
    
    def _get_overall_progress(self):
        subtotal = ((self.parameter_optimization_subtotal/self.parameter_optimization_total)*100) + (100 * self.current_generation)
        total = 100 * self.generations
        return float((subtotal / total) * 100)
        
    traits_view = View(
        VGroup(
            VGroup(
                Item('overall_progress'),
                HGroup(
                    Item('status', show_label=False, style='readonly'),
                ),
                label='Progress',
            ),
            VGroup(
                Item('figure',
                    show_label=False, 
                    editor=MPLFigureEditor(),
                ),
                label='Population Fitness',
            ),
            VGroup(
                HGroup(
                    Item('current_best_fitness', style='readonly', label='Fitness'),
                ),
                Item('current_fittest_module_list', show_label=False,
                    editor=TabularEditor(
                        adapter=TabularAdapter(
                            columns=[
                                ('Module', 'name'),
    #                            ('Parameters', 'parameters'),
                                ('Parameters', 'parameters_str'),
                            ],
                        ),
                        editable=False,
                        operations=[],
                    ),
                ),
                label='Fittest individual',
            ),
            VGroup(
                HGroup(
                   Item('error_string', style='readonly', emphasized=True, show_label=False),
                ),
                visible_when='len(object.error_string) > 0',
                label='Error(s)',
            ),
        ),
        resizable=True,
        width=400, height=300,
        id='POptimizerExpect.view',
    )


    