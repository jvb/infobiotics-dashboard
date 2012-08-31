from enthought.pyface.workbench.api import Perspective, PerspectiveItem

class ExamplePerspective(Perspective):
    ''' An example perspective for a workbench application plugin.

    Perspectives contribute collections of views to a Workbench application.
    
    '''
    id='infobiotics.dashboard.plugins.example.perspectives.ExamplePerspective', 
    name = 'ExamplePerspective'
    show_editor_area = True
    contents = [
        PerspectiveItem(id='ExampleTraitsUIView', position='left'),
        PerspectiveItem(
            id='ExamplePyFaceView', 
            position='bottom',
            height=0.1,
        ),
    ]
    