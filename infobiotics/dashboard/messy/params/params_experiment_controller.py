from params_controller import ParamsController
from enthought.traits.api import implements, Instance
from enthought.traits.ui.api import Item, Group
from infobiotics.dashboard.interfaces import IExperimentHandler
from infobiotics.dashboard.params.api import error_string_group
from infobiotics.dashboard.params.api import load_save_perform_actions 
from ParamsExperimentControllerView import ParamsExperimentControllerView

class ParamsExperimentController(ParamsController):
    ''' Standard handler for ParamsExperiment actions.
    
    Required for TraitsUI action buttons, it simply calls the synonymous 
    functions on the experiment pointed to by 'info.object', i.e. it wraps the
    scripting interface.
    
    '''
    implements(IExperimentHandler)
        
#    content = Group(error_string_group)
    def _content_default(self):
        return error_string_group

#    def traits_view(self):
#        return ParamsExperimentControllerView(
#            Item('_cwd', label='Working directory'),
#            self.content,
#            title=self.title,
#            id=self.id,
#        )
        
    traits_view = ParamsExperimentControllerView(
        Item('_cwd', label='Working directory'),
        error_string_group,
        'controller.content',
        title='controller.title',
        id='controller.id'
    )

    def perform(self, info):
        info.object.perform()

from infobiotics.dashboard.mcss.api import mcss_params_controller_group
from infobiotics.dashboard.mcss.api import McssParamsController
class McssParamsExperimentController(ParamsExperimentController, McssParamsController):
    content = Group(mcss_params_controller_group)


if __name__ == '__main__':
    from infobiotics.dashboard.mcss.api import McssParams
#    McssParams().configure_traits(handler=McssParamsExperimentController())
    self = McssParamsExperimentController()
    print self.model
    print self.content
    self.configure_traits()