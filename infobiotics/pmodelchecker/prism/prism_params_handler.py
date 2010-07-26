from __future__ import with_statement
import os.path
from infobiotics.commons.api import read, write
from enthought.traits.api import (
    Trait, Range, Button, Str, Bool, Instance, DelegatesTo,
)
from enthought.traits.ui.api import View, Group, HGroup, Item, CodeEditor, Controller
from infobiotics.pmodelchecker.api import (
    PModelCheckerParamsHandler, ModelParameters,
)
from prism_params_group import prism_params_group

class PRISMParamsHandler(PModelCheckerParamsHandler):

    def _params_group_default(self):
        return prism_params_group
    
    id = 'PRISMParamsHandler'

    help_urls = [
        ('Introduction to PRISM','http://www.prismmodelchecker.org/manual/Main/Introduction'),
        ('The PRISM language','http://www.prismmodelchecker.org/manual/ThePRISMLanguage/Introduction'),
        ('Property specifiation','http://www.prismmodelchecker.org/manual/PropertySpecification/Introduction'),
        ('Tutorial for systems biologists','http://www.prismmodelchecker.org/tutorial/circadian.php'),
    ]

    _prism_model_str = Str

    def object__translated_fired(self, info):
        if info.object.PRISM_model != '':
            try:
                with read(info.object.PRISM_model_) as f:
                    print 'got here'
                    self._prism_model_str = f.read()
            except IOError, e:
                print e
        else:
            self._prism_model_str = ''

    view_prism_model = Button

    def _view_prism_model_fired(self):
        print '"%s"' % self._prism_model_str
        self.edit_traits(
            view=View(
                Group(
                    HGroup(
                        Item(label='PRISM model:'),
                        Item('PRISM_model_', show_label=False, style='readonly'),
                        Item(label='(Ctrl-F to find)'),#, Ctrl-D duplicates line)'), # not when "style = 'readonly'"
                    ),
                    Item('handler._prism_model_str',
                        show_label = False, 
                        style = 'readonly', #TODO style = 'custom',
                        editor = CodeEditor(lexer='null'),
                    ),
                    show_border = True,
                ),
                buttons = ['OK'],#,'Revert','Undo'], # not when "style = 'readonly'"
                width=640, height=480,
                resizable = True,
                id = 'view_prism_model_view',
            )
        )

    model_parameters = DelegatesTo('_model_parameters') # in PModelCheckerParamsHandler

    def init(self, info):
        super(PRISMParamsHandler, self).init(info)
        if info.object.model_parameters != '':
#            self._model_parameters.model_parameters = info.object.model_parameters
            self.model_parameters = info.object.model_parameters #FIXME this is bonkers

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
    