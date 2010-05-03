from bnf_editor import BNFEditor


class LPPEditor(BNFEditor):

#    key_bindings = Instance(KeyBindings) # The key bindings used by the editor
    wildcard = 'Lattice Population P system (*.lpp)'
    untitled_prefix='model '
    text = '''LPPsystem <modelName>

    SPsystems
        SPsystem <pSystem> from <pSystemFilename>.sps
    endSPsystems

    lattice <lattice> from <latticeFilename>.lat

    spatialDistribution
    
        positions for <pSystem>
            coordinates
                x = 0
                y = 0
            endCoordinates
        endPositions
    
    endSpatialDistribution

endLPPsystem
'''
    