from enthought.traits.ui.api import Controller, View, Group, Item
from enthought.traits.ui.ui_traits import Buttons
from enthought.pyface.api import FileDialog, OK #from enthought.pyface.constant import *
from enthought.traits.api import List, Str, Instance
from infobiotics.dashboard.params.api import *
from infobiotics.dashboard.params.ParamsControllerView import ParamsControllerView

class ParamsController(Controller):
    '''
    
    self.model == info.object == Instance(Params)
    
    '''
    
    id = Str('params_controller')
    title = Str('Edit parameters')
#    content = Instance(Group, None)
        
    def traits_view(self):
        return ParamsControllerView(
            Item('_cwd', label='Working directory'),
            self.content,
            title=self.title,
            id=self.id,
        )
    
    def load(self, info):
        ''' Load the traits of an experiment from a .params XML file. '''
        fd = FileDialog(
            wildcard=self.wildcard, 
            title='Load %s experiment parameters' % self.model._parameter_set_name,
        )
        if fd.open() == OK:
            self.model.load(fd.path)

    def save(self, info):
        ''' Saves the traits of experiment to a .params XML file. '''
        fd = FileDialog(
            action='save as', 
            wildcard=self.wildcard,
            title='Save parameters',
        )
        if fd.open() == OK:
            self.model.save(fd.path)

    wildcard = Str(desc='an appropriate wildcard string for a WX or Qt open and save dialog looking for params files.')
        
    def _wildcard_default(self):
        wildcards = [
            ('Experiment parameters', ['*.params']), 
            ('All files', ['*']),
        ] 
        try:
            import os
            toolkit = os.environ['ETS_TOOLKIT']
        except KeyError:
            toolkit = 'wx'
        wildcard = ''
        if toolkit == 'qt4':
            for i, w in enumerate(wildcards):
                # qt4: 'py and test (*.py *.test)||\ntest (*.test)||\npy (*.py)'
                wildcard += '%s (%s)' % (w[0], ' '.join(w[1])) 
                if i < len(wildcards) - 1:
                    wildcard += '||'#\n'
        else: # assume os.environ['ETS_TOOLKIT'] == ('wx' and not 'null')
            for i, w in enumerate(wildcards):
                # wx: 'py and test (*.py *.test)|*.py;*.test|\ntest (*.test)|*.test|\npy (*.py)|*.py'#|
                w2 = ';'.join(w[1])
                wildcard += '%s (%s)|%s' % (w[0], w2, w2)
                if i < len(wildcards) - 1:
                    wildcard += '|'#\n'
        return wildcard

    
#    # set _dirty on model and * on title ---  
#    # self.model._dirty == info.object._dirty == Params()._dirty
#    # http://code.enthought.com/projects/traits/docs/html/TUIUG/handler.html
#
#    def setattr(self, info, object, name, value):
#        super(ParamsController, self).setattr(info, object, name, value)
#        self.model._dirty = True
##        if name in self.model.parameter_names():
##            self.model._dirty = True
#        
#    def object__dirty_changed(self, info):
#        if info.initialized:
#            info.ui.title += '*'
#        else:
#            self.model._dirty = False


if __name__ == '__main__':
    from infobiotics.dashboard.mcss.api import McssParamsController
    McssParamsController().configure_traits()