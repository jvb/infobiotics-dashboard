from __future__ import with_statement
import os.path
from infobiotics.commons.api import read, write
from enthought.traits.api import (
    Trait, Range, Button, Str, Bool, Instance, DelegatesTo, on_trait_change
)
from enthought.traits.ui.api import View, Group, HGroup, Item, CodeEditor, Controller
from infobiotics.pmodelchecker.pmodelchecker_params_handler import PModelCheckerParamsHandler
from infobiotics.pmodelchecker.model_parameters import ModelParameters
from prism_params_group import prism_params_group

#import logging
#logger = logging.getLogger(__file__)
#logger.addHandler(logging.StreamHandler())
#logger.setLevel(logging.ERROR)
from infobiotics.commons.api import logging
logger = logging.getLogger(__name__)


class PRISMParamsHandler(PModelCheckerParamsHandler):

    def _params_group_default(self):
        return prism_params_group
    
    id = 'PRISMParamsHandler'

    help_urls = [
        ('Quick start', 'http://www.infobiotics.org/infobiotics-workbench/quickStart/modelProperties.html'),
        ('Tutorial', 'http://www.infobiotics.org/infobiotics-workbench/tutorial/modelChecking.html'),
        ('Introduction to PRISM', 'http://www.prismmodelchecker.org/manual/Main/Introduction'),
        ('The PRISM language', 'http://www.prismmodelchecker.org/manual/ThePRISMLanguage/Introduction'),
        ('Property specifiation', 'http://www.prismmodelchecker.org/manual/PropertySpecification/Introduction'),
        ('Tutorial for systems biologists', 'http://www.prismmodelchecker.org/tutorial/circadian.php'),
    ]

    default_temporal_formula = 'P = ? [ true U[T,T] ( molecule >= constant ) ]'

    _prism_model_str = Str

    @on_trait_change('model._translated')
    def load_translated_model(self, translated):
        if not translated:
            return
        self._prism_model_str = ''
        if self.model.PRISM_model != '':
            try:
                with read(self.model.PRISM_model_) as f:
                    self._prism_model_str = f.read()
#                    logger.debug(self._prism_model_str)
            except IOError, e:
                logger.error(e)
#            from infobiotics.commons.strings import shorten_path
#            self.status = "Translated '%s' to '%s'." % (shorten_path(self.model.model_specification, 30), shorten_path(self.model.PRISM_model, 30))
            self.status = "Translated '%s' to '%s'." % (self.model.model_specification, self.model.PRISM_model)
        else:
            self._prism_model_str = ''

    view_prism_model = Button
    def _view_prism_model_fired(self):
        class ViewPRISMModelHandler(Controller):
            _prism_model_str = Str
            PRISM_model = Str
        ViewPRISMModelHandler(model=self.model, _prism_model_str=self._prism_model_str).edit_traits(
            view=View(
                Group(
                    HGroup(
                        Item(label='PRISM model:'),
                        Item('PRISM_model_', show_label=False, style='readonly'),
                        Item(label='(Ctrl-F to find)'), #, Ctrl-D duplicates line)'), # not when "style = 'readonly'"
                    ),
                    Item('handler._prism_model_str',
                        show_label=False,
                        style='readonly', #TODO style = 'custom',
                        editor=CodeEditor(lexer='null'),
                    ),
                    show_border=True,
                ),
                buttons=['OK'], #,'Revert','Undo'], # not when "style = 'readonly'"
                width=640, height=480,
                resizable=True,
                id='view_prism_model_view',
            )
        )

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


    model_parameters = DelegatesTo('model_parameters_object') # i.e. self.model_parameters_object.model_parameters (model_parameters_object is defined in PModelCheckerHandler)
    @on_trait_change('model_parameters')
    def forward_changes_in_model_parameters_to_model(self):
        self.model.model_parameters = self.model_parameters

    def load(self, info):
        super(PRISMParamsHandler, self).load(info)
        if self.model_parameters_object is not None:
            self.model_parameters_object.model_parameters = self.model.model_parameters # the reverse of forward_changes_in_model_parameters_to_model


if __name__ == '__main__':
    execfile('prism_params.py')
    
