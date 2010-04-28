from __future__ import with_statement
import os.path
from common.files import read, write
from infobiotics.shared.api import ParamsView, Trait, Range, Button, Str, Bool, Instance, DelegatesTo
from infobiotics.pmodelchecker.api import (
    prism_params_group, PModelCheckerParamsHandler, ModelParameters
)

prism_params_view = ParamsView(
    prism_params_group,
)

class PRISMParamsHandler(PModelCheckerParamsHandler):

    traits_view = prism_params_view
    id = 'PRISMParamsHandler'


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
        
    retranslate_prism_model = Button(desc='whether to translate the PRISM model from the P system model again.\nThis will overwrite any changes that have been made to the PRISM model file.')
    
    def _retranslate_prism_model_fired(self):
        self.model.translate_model_specification_to_PRISM_model()
        self._prism_model_str_changed = False


    model_parameters = DelegatesTo('_model_parameters')
    
    _model_parameters = Instance('ModelParameters')

    def init(self, info):
        # must create _model_parameters here rather than __model_parmeters_default() because DelegatesTo('_model_parameters') causes it to be created before _cwd.
        self._model_parameters = ModelParameters(_cwd=self.model._cwd)
        if info.object.model_parameters != '':
            self._model_parameters.model_parameters = info.object.model_parameters
        super(PRISMParamsHandler, self).init(info)

    def save(self, info):
        info.object.model_parameters = self.model_parameters
        super(PRISMParamsHandler, self).save(info)


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


if __name__ == '__main__':
    execfile('prism_params.py')
    