from __future__ import with_statement
import os.path
from common.files import read, write
from infobiotics.shared.api import ParamsView, Trait, Range, Button, Str, Bool, Property
from infobiotics.pmodelchecker.api import (
    prism_params_group, PModelCheckerParamsHandler
)

prism_params_view = ParamsView(
    prism_params_group,
)

class PRISMParamsHandler(PModelCheckerParamsHandler):

    traits_view = prism_params_view
    id = 'PRISMParamsHandler'


#    _model_parameters = Instance('ModelParameters')
##    def __model_parameters_default(self):
##        return ModelParameters(prism_experiment=self)
#    model_parameters = DelegatesTo('_model_parameters')


    _prism_model_str = Str

    def object_PRISM_model_changed(self, info):
        file = os.path.abspath(os.path.join(info.object._cwd, info.object.PRISM_model)) #TODO use shadow trait for abspath
        if os.path.exists(file) and not os.path.isdir(file): 
            try:
                with read(file) as f:
                    self._prism_model_str = f.read()
            except IOError, e:
                print e
        else:
            self._prism_model_str = ''

    edit_prism_model = Button

    def _edit_prism_model_fired(self):
        _prism_model_str = self._prism_model_str
        if self._prism_model_str == '':
            self.model.translate_model_specification_to_PRISM_model()
        from enthought.traits.ui.api import View, Group, HGroup, Item, CodeEditor
        edit_prism_model_view = View(
                Group(
                    HGroup(
                        Item(label='Editing PRISM model:'),
                        Item('PRISM_model', show_label=False, style='readonly'),
                    ),
                    Item('handler._prism_model_str',
                        show_label = False, 
                        style = 'custom',
                        editor = CodeEditor(lexer='null'),
                    ),
                    Item(label='Ctrl-F toggles Find, Ctrl-D duplicates line.'),
                    show_border = True,
                ),
                buttons = ['OK','Revert','Undo','Redo'],
                width=640, height=480,
                resizable = True,
                id = 'edit_prism_model_view',
            )
        if self.edit_traits(view = edit_prism_model_view, kind='livemodal').result: # if kind is not live no traits are updated! (translate has model_specification='')
            if self._prism_model_str != _prism_model_str:
                file = os.path.abspath(os.path.join(self.model._cwd, self.model.PRISM_model)) #TODO use shadow trait for abspath
                try:
                    with write(file) as f:
                        f.write(self._prism_model_str)
                except IOError, e:
                    print e
                self._prism_model_str_changed = True
                
    _prism_model_str_changed = Bool(False)
        
    retranslate_prism_model = Button
    
    def _retranslate_prism_model_fired(self):
        self.model.translate_model_specification_to_PRISM_model()
        self._prism_model_str_changed = False



    confidence = Trait(
        '90% (0.1)',
        {
            '90% (0.1)' : 0.1,
            '95% (0.05)' : 0.05,
            '99% (0.01)' : 0.01,
            'custom' : '_custom_confidence', #TODO this is never used, but that's not a problem
        },
        desc='the confidence level used when approximating the answer to a formula'
    )
    
    _custom_confidence = Range(0.0, 0.5, 0.1, mode='text')

    def _confidence_changed(self):
        if self.confidence == 'custom':
            self.sync_trait('confidence_', self.model, alias='confidence', mutual=False, remove=True)
            self.sync_trait('_custom_confidence', self.model, alias='confidence', mutual=False)
        else:
            self.sync_trait('_custom_confidence', self.model, alias='confidence', mutual=False, remove=True)
            self.sync_trait('confidence_', self.model, alias='confidence', mutual=False)



#    def object_model_specification_changed(self, info):
#        trait = info.object.base_trait('PRISM_model')
#        if info.object.model_specification != '':
#            trait.handler.writable = True
#            trait.handler.readable = None
#            trait.handler.exists = None
#        else:
#            trait.handler.writable = None
#            trait.handler.readable = True
#            trait.handler.exists = True
            



#    _open_in_new_window = Button('TODO') # open in new text editor syncing? #TODO add to view
    
#    def _temporal_formulas_changed(self):
#        print 'got here'
#        try:
#            with open(self.temporal_formulas, 'r') as f: 
#                _temporal_formulas_str = f.read()
#                #TODO create TemporalFormula objects by parsing temporal_formulas
#                
#        except IOError:
#            logger.error(e)


if __name__ == '__main__':
    execfile('prism_params.py')
    