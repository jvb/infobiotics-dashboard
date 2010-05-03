# This file is part of the Infobiotics Dashboard. See LICENSE for copyright.
# $Id: experiment_handler.py 391 2010-01-22 16:53:37Z jvb $
# $HeadURL: https://psiren.cs.nott.ac.uk/repos/infobiotics/dashboard/trunk/infobiotics/dashboard/plugins/experiments/experiment_handler.py $
# $Author: jvb $
# $Revision: 391 $
# $Date: 2010-01-22 16:53:37 +0000 (Fri, 22 Jan 2010) $

from experiment_handler import ExperimentHandler 
from infobiotics.shared.traits_imports import *
from enthought.traits.ui.api import Include

class ParamsExperimentHandler(ExperimentHandler):
    ''' Standard handler for ParamsExperiment actions.
    
    Required for TraitsUI action buttons, it simply calls the synonymous 
    functions on the experiment pointed to by 'info.object', i.e. it wraps the 
    scripting interface.
    
    '''
    def load(self, info):
        ''' Load the traits of an experiment from a .params XML file. '''
        info.object.load()

    def save(self, info):
        ''' Saves the traits of experiment to a .params XML file. '''
        info.object.save()
        
    def perform(self, info):
        ''' Performs the experiment.
        
        Saves parameters first.
        
        '''
        
        if info.initialized:
            print 'initialized'
        else:
            info.object.perform()

#    _title = Str 
#    def init(self, info):
#        if info.initialized:
#            self._title = info.ui.title 
#    
#    def object__dirty_changed(self, info):
#        if info.initialized:
##            info.ui.title += '*'
#            info.ui.title = '%s*' % self._title
#    
#    def setattr(self, info, object, name, value):
#        ''' Intercept user changing traits via the interface.
#        
#        '''
#        super(McssExperimentHandler, self).setattr(info, object, name, value)
##        print object, name, value
#        info.object._dirty = True
        

    load_action = Action(name='Load', action='load', 
        tooltip='Load parameters from a file'
    ) 

    save_action = Action(name='Save', action='save', 
        tooltip='Save the current parameters to a file'
    )
    
    perform_action = Action(name='Perform', action='perform', 
        tooltip='Perform the experiment with the current parameters',
        enabled_when='object.has_valid_parameters()', #XXX calls has_valid_parameters which each UI change
    )

#    load_save_actions = List(Action, [load_action, save_action])
    load_save_actions = [load_action, save_action]
    # not traits, class fields
    load_save_perform_actions = List(Action, [load_action, save_action, perform_action])                                 
    
    # Used by traits_view() to react to action button clicks, and potentially more in subclasses.
#    handler = Instance(ParamsExperimentHandler, ParamsExperimentHandler())
    
     
    title = Str('Experiment', desc='the name of the experiment being performed') # Used by traits_view() as title of view. #TEST whether comment or desc appears with trait in Endo-generated documentation
    
    problem = Str('', desc="indicates which trait is preventing the 'Perform' button from being enabled") #FIXME use problem as tooltip?
    
    group = Instance(Group) # Used by traits_view() as an Include object without using Include (see http://code.enthought.com/projects/traits/docs/html/TUIUG/advanced_view.html#id16).
#    def _group_default(self):
#        raise NotImplementedError(
#            '_group_default(self) must be implemented in subclasses of ParamsExperimentHandler.'
#        )

    header_group = Instance(Group)
    parameters_group = Instance(Group)
    footer_group = Instance(Group)

    def traits_view(self):
        return View(
            'file',
            Include('handler.header_group'),
            self.group,
            self.parameters_group,
            Include('handler.parameters_group'),
            Include('parameters_group'),
            Include('handler.footer_group'),
            Item('handler.problem', style='readonly', emphasized=True, visible_when='handler.problem != ""'),
            buttons=['Cancel', 'Undo', 'Revert'] + self.load_save_perform_actions,
#            handler=self.handler,
#            width=800, height=600,
            resizable=True,
#            scrollable=True, #FIXME
            title=self.title,
        )          
          