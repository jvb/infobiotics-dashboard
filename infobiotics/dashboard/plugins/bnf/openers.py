# This file is part of the Infobiotics Dashboard. See LICENSE for copyright.
# $Id: openers.py 366 2010-01-13 20:16:01Z jvb $
# $HeadURL: https://psiren.cs.nott.ac.uk/repos/infobiotics/dashboard/trunk/infobiotics/dashboard/plugins/bnf/openers.py $
# $Author: jvb $
# $Revision: 366 $
# $Date: 2010-01-13 20:16:01 +0000 (Wed, 13 Jan 2010) $


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
