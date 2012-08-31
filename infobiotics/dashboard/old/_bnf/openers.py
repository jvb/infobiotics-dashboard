""" Some openers! """


from infobiotics.dashboard.plugins.unified_open_action.api import Opener

from infobiotics.dashboard.plugins.bnf.lat_editor import LATEditor

openers = [
    
    Opener(
        wildcard='Lattice (*.lat)',
        editor_class=LATEditor
    ),

    # ...
    
]
