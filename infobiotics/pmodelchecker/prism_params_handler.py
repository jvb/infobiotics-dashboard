from __future__ import with_statement
import os.path
from common.files import read
from infobiotics.shared.api import ParamsView, Trait, Range, Button, Str, Bool
from infobiotics.pmodelchecker.api import (
    prism_params_group, PModelCheckerParamsHandler,
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


    generate_prism_model = Button
    
    def _generate_prism_model_fired(self):
        #TODO do some validation
#            path = self.path
        from tempfile import NamedTemporaryFile
        tmp = NamedTemporaryFile().name

        generate_experiment = PRISMExperiment(model_specification=self.model_specification, PRISM_model=self.PRISM_model, task='Translate')
        generate_experiment.save(tmp)
        generate_experiment.perform()


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
            
    _prism_model_str = Str
    _prism_model_dirty = Bool(False)

    def _prism_model_str_changed(self, value):
        self._prism_model_dirty = True
    
    def object_PRISM_model_changed(self, info):
        file = os.path.abspath(os.path.join(info.object._cwd, info.object.PRISM_model)) 
        if os.path.exists(file) and not os.path.isdir(file): 
            try:
                with read(file) as f:
                    self._prism_model_str = f.read()
                    self._prism_model_dirty = False
            except IOError, e:
                print e
        else:
            self._prism_model_str = ''
            self._prism_model_dirty = False

    _show_prism_model = Bool(False)
    
    edit_prism_model = Button

    def _edit_prism_model_fired(self):
        from enthought.traits.ui.api import View, Item, CodeEditor, TextEditor
        self.edit_traits(
            kind='nonmodal', 
            view=View(
                Item('_prism_model_str', 
                     style='custom',
                     editor=TextEditor()), 
                buttons=['OK','Revert','Undo','Redo'],
                resizable=True,
            ),
        )

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
    