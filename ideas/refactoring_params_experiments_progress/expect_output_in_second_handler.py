from __future__ import division

import platform
if platform.system() == 'Windows':
    import wexpect as expect #TODO test with and include wexpect in sys.path
else:
    import pexpect as expect

from threading import Thread

import sys

import os

from enthought.traits.api import HasTraits, Range, Button, Str, Property, property_depends_on

from enthought.traits.ui.api import Controller, ModelView, View

import time

from threading import Thread


class Experiment(HasTraits):
    
    progress = Range(0.0, 100.0)

    def __init__(self, **traits):
        super(Experiment, self).__init__(**traits)

    def perform(self, thread=False):
        def count_to_a_hundred():
            for i in range(100):
                time.sleep(0.1)
                self.progress += 1
            print 'finished'
        if thread:
            Thread(target=count_to_a_hundred).start()
        else:
            count_to_a_hundred()


class ExperimentHandler(Controller):
    
    perform = Button

    def _perform_fired(self):
        progress_handler = ExperimentProgressHandler(model=self.model)
        self.model.perform(thread=True)
        progress_handler.edit_traits(kind='live')
        
    view = View(
        'controller.perform',
        'progress',
        id='ExperimentHandler'
    )

class ExperimentProgressHandler(ModelView):
#    progress = Range(0.0, 100.0)
    
#    def model_progress_changed(self, info):
#        self.progress = self.model.progress

    progress = Property(Range(0.0, 100.0))
    
    @property_depends_on('model.progress')
    def _get_progress(self):
        return self.model.progress
    
    view = View(
        'model.progress',
        'progress',
        id='ExperimentProgressHandler'
    )
    def close(self, info, is_ok):
        if self.progress == 100:
            return True


if __name__ == '__main__':
    ExperimentHandler(model=Experiment()).configure_traits()
    