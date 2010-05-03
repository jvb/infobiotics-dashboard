# This file is part of the Infobiotics Dashboard. See LICENSE for copyright.
# $Id: ui_plugin.py 411 2010-01-25 18:03:26Z jvb $
# $HeadURL: https://psiren.cs.nott.ac.uk/repos/infobiotics/dashboard/trunk/infobiotics/dashboard/plugins/bnf/ui_plugin.py $
# $Author: jvb $
# $Revision: 411 $
# $Date: 2010-01-25 18:03:26 +0000 (Mon, 25 Jan 2010) $


import os; os.environ['ETS_TOOLKIT']='qt4'
from enthought.pyface.workbench.api import Perspective, PerspectiveItem
from enthought.envisage.api import Plugin
from enthought.traits.api import List
from bnf_action_set import BNFActionSet
from views import LPPView, SPSView, LATView, PLBView



class BNFPerspective(Perspective):
    name = 'BNF' # The perspective's name
    show_editor_area = True # Should the editor area be shown in this perspective?
    contents = [
        PerspectiveItem(id='LPPView', position='right'),
        PerspectiveItem(id='SPSView', position='right'),
        PerspectiveItem(id='LATView', position='right'),
        PerspectiveItem(id='PLBView', position='right'),
    ]


class BNFUIPlugin(Plugin):

    # 'IPlugin' interface
    id = 'infobiotics.bnf_ui_plugin' # The plugin's unique identifier
    name = 'BNF' # The plugin's name (suitable for displaying to the user)

    ACTION_SETS       = 'enthought.envisage.ui.workbench.action_sets'
    PERSPECTIVES      = 'enthought.envisage.ui.workbench.perspectives'
    PREFERENCES_PAGES = 'enthought.envisage.ui.workbench.preferences_pages'
    VIEWS             = 'enthought.envisage.ui.workbench.views'
    # Contributions to extension points made by this plugin
    action_sets = List(contributes_to=ACTION_SETS)
    perspectives = List(contributes_to=PERSPECTIVES)
    preferences_pages = List(contributes_to=PREFERENCES_PAGES)
    views = List(contributes_to=VIEWS)

    def _action_sets_default(self):
        return [BNFActionSet]

    def _perspectives_default(self):
        return [BNFPerspective]

    def _views_default(self):
        return [LPPView, SPSView, LATView, PLBView]

    def _preferences_pages_default(self):
        return []

    openers = List(contributes_to='infobiotics.dashboard.plugins.unified_open_action.unified_open_action_plugin.openers')

    def _openers_default(self):
        from openers import openers
        return openers



if __name__ == '__main__':
    execfile('/home/jvb/phd/eclipse/infobiotics/Infobiotics Dashboard/infobiotics/workbench/run.py')        
